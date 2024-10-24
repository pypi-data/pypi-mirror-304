# Author: Scott Woods <scott.18.ansar@gmail.com>
# MIT License
#
# Copyright (c) 2017-2023 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
__docformat__ = 'restructuredtext'

import uuid
import datetime

import ansar.create as ar
from .socketry import *
from .transporting import *
from .plumbing import *
from .directory_if import *
from .directory import *
from .networking_if import *

__all__ = [
	'roll_call',
	'connected_to',
	'not_connected',
	'connected_origin',
	'ApiUpdate',
	'ApiSample',
	'ApiRequested',
	'ApiShow',
	'ApiReport',
	'ApiTuning',
	'ApiMetering',
	'ConnectToAddress',
	'ListenAtAddress',
	'SubscribeToListing',
	'PublishAListing',
	'SubscribeToSearch',
]

def roll_call(*args, **kw):
	if len(args) == 1:
		kv = args[0].__dict__
	else:
		kv = kw

	awol = [k for k, v in kv.items() if v is None]
	if awol:
		return ar.TemporarilyUnavailable(awol)
	return None

def connected_to(self, address, message, console=True):
	r = address[-1]
	self.connection[r] = message
	if not console:
		return

	if isinstance(message, Accepted):
		self.console(f'Accepted <{r:08x}> ({message.accepted_ipp} on {message.listening_ipp})')
	elif isinstance(message, Connected):
		self.console(f'Connected <{r:08x}> ({message.connected_ipp} on {message.requested_ipp})')
	elif isinstance(message, Delivered):
		self.console(f'Delivered <{r:08x}> ({message.matched_name} on {message.matched_search})')
	elif isinstance(message, Available):
		self.console(f'Available <{r:08x}> ({message.matched_name} on {message.matched_search})')

def not_connected(self, address, console=True):
	r = address[-1]
	p = self.connection.pop(r, None)
	if not p or not console:
		return

	if isinstance(p, Accepted):
		self.console(f'Closed/Abandoned <{r:08x}> ({p.accepted_ipp} on {p.listening_ipp})')
	elif isinstance(p, Connected):
		self.console(f'Closed/Abandoned <{r:08x}> ({p.connected_ipp} on {p.requested_ipp})')
	elif isinstance(p, Delivered):
		self.console(f'Cleared/Dropped <{r:08x}> ({p.matched_name} on {p.matched_search})')
	elif isinstance(p, Available):
		self.console(f'Cleared/Dropped <{r:08x}> ({p.matched_name} on {p.matched_search})')

def connected_origin(self, address):
	r = address[-1]
	p = self.connection.get(r, None)
	return p

#
#
SLOT_COUNT = 16
API_STAND_DOWN = (5.0 * 60)

class INITIAL: pass
class PENDING: pass
class CONNECTED: pass
class GLARING: pass
class CLOSING: pass
class ACCEPTING: pass
class READY: pass

#
class ApiUpdate(object):
	def __init__(self, api=None, request_type=None, enabled=None, responsiveness=None):
		self.api = api
		self.request_type = request_type
		self.enabled = enabled
		self.responsiveness = responsiveness

class ApiSample(object):
	def __init__(self, started_at=None, measured=None, average=None):
		self.started_at = started_at
		self.measured = measured
		self.average = average

class ApiRequested(object):
	def __init__(self, enabled=None, responsiveness=None, average=None, started_at=None, stopped_at=None, total_span=None, metering=None):
		self.enabled = enabled
		self.responsiveness = responsiveness
		self.average = average
		self.started_at = started_at
		self.stopped_at = stopped_at
		self.total_span = total_span
		self.metering = metering

class ApiShow(object):
	def __init__(self, api=None, request_type=None):
		self.api = api
		self.request_type = request_type

API_SCHEMA = {
	'api': ar.Unicode(),
	'request_type': ar.Type(),
	'responsiveness': ar.TimeSpan(),
	'enabled': ar.Boolean(),
	'started_at': ar.WorldTime(),
	'stopped_at': ar.WorldTime(),
	'total_span': ar.TimeSpan(),
	'measured': ar.TimeSpan(),
	'average': ar.TimeSpan(),
	'metering': ar.DequeOf(ar.UserDefined(ApiSample)),
}

ar.bind(ApiSample, object_schema=API_SCHEMA)
ar.bind(ApiUpdate, object_schema=API_SCHEMA)
ar.bind(ApiRequested, object_schema=API_SCHEMA)
ar.bind(ApiShow, object_schema=API_SCHEMA)

class ApiReport(object):
	def __init__(self, enabled=None, responsiveness=None, report=None):
		self.enabled = enabled
		self.responsiveness = responsiveness
		self.report = report or ar.default_map()

REPORT_SCHEMA = {
	'enabled': ar.Boolean(),
	'responsiveness': ar.TimeSpan(),
	'report': ar.MapOf(ar.Type(), ar.UserDefined(ApiRequested)),
}

ar.bind(ApiReport, object_schema=REPORT_SCHEMA)

#
class ApiTuning(object):
	def __init__(self, enabled=True, responsiveness=3.0):
		self.enabled = enabled
		self.responsiveness = responsiveness

class ApiMetering(ApiTuning):
	def __init__(self, enabled=True, responsiveness=3.0, tunings=None):
		ApiTuning.__init__(self, enabled, responsiveness)
		self.tunings = tunings or {}		# Map of ApiTunings.

		self.started = ar.default_map()		# Map of starts.
		self.stopped = ar.default_map()		# Move to map of deques on completion.

		self.counter = 0

	def update(self, message):
		if message.request_type:
			try:
				tuning = self.tunings[message.request_type]
			except KeyError:
				tuning = ApiTuning()
				self.tunings[message.request_type] = tuning
		else:
			tuning = self
	
		changed = False
		if message.enabled is not None:
			changed = tuning.enabled != message.enabled
			tuning.enabled = message.enabled

		if message.responsiveness is not None:
			changed = changed or tuning.responsiveness != message.responsiveness
			tuning.responsiveness = message.responsiveness

			slot = self.stopped.get(message.request_type, None)
			if slot is not None:
				slot[2] = tuning.responsiveness * 0.75
				slot[3] = tuning.responsiveness * 0.9
				slot[4] = tuning.responsiveness

		return changed

	def out_of_service(self, request):
		# Determine the operational parameters.
		request_type = type(request)

		tuning = self.tunings.get(request_type, None)
		if tuning is None:
			if self.enabled:
				return None
			return ar.OutOfService(f'API is out of service')

		if tuning.enabled:
			return None
		path = request_type.__art__.path
		return ar.OutOfService(f'API ({path}) is out of service')

	def start_meter(self, request):
		# Determine the operational parameters.
		request_type = type(request)
		tuning = self.tunings.get(request_type, None) or self

		# Bump the number
		self.counter += 1

		# Find the records for this request type.
		slot = self.stopped.get(request_type, None)
		if slot is None:		# New slot, no records.
			d = ar.deque()
			slot = [d, 0.0, tuning.responsiveness * 0.75, tuning.responsiveness * 0.9, tuning.responsiveness]
			self.stopped[request_type] = slot
		else:
			d = slot[0]			# Records of completed transactions.
			if len(d) == 0:		# None yet (first not complete).
				pass
			else:					# At least one completed transaction.
				mr = d[-1]			# Most recent record.
				average = mr[2]
				path = request_type.__art__.path
				if average < slot[2]:			# Less than 0.75.
					pass
				elif average < slot[3]:			# Between 0.75 and 0.9.
					if self.counter % 10 == 0:
						return ar.Overloaded(f'API ({path}) is currently overloaded (shedding 10%)')
				elif average < slot[4]:			# Between 0.9 and 1.0.
					if self.counter % 4 == 0:
						return ar.Overloaded(f'API ({path}) is currently overloaded (shedding 25%)')
				else:
					# started_at = mr[0]
					# since = ar.clock_now() - started_at
					# if since < API_STAND_DOWN:
					#	return ar.Overloaded(f'API ({path}) is currently overloaded (standing down)')

					if self.counter % 2 == 0:
						return ar.Overloaded(f'API ({path}) is currently overloaded (shedding 50%)')

		# Create a new, incomplete record.
		number = uuid.uuid4()
		started_at = ar.clock_now()
		m = [request_type, started_at]
		self.started[number] = m
		return number

	def stop_meter(self, number, log=None):
		# Find the starting point.
		m = self.started.pop(number, None)
		if m is None:
			if log:
				log.warning(f'Unknown meter "{number}"')
			return
		request_type, started_at = m

		# Create the row.
		stopped_at = ar.clock_now()				# End of span.
		measured = stopped_at - started_at		# Duration.
		row = [started_at, measured, 0.0]

		# Find the slot.
		slot = self.stopped.get(request_type, None)
		if slot is None:
			if log:
				log.warning(f'Unknown metering request "{request_type}", not started?')
			return
		d = slot[0]

		# Append the row.
		d.append(row)
		total = slot[1]
		count = len(d)

		# Slide the window.
		total += measured
		while count > SLOT_COUNT:
			f = d.popleft()
			total -= f[1]
			count -= 1
		slot[1] = total

		average = total / count
		row[2] = average

		if log:
			dt = datetime.datetime.fromtimestamp(started_at, tz=ar.UTC)
			log.sample(request=request_type.__art__.path, started_at=(ar.WorldTime(), dt), measured=(ar.TimeSpan(), measured))

	def report(self, request_type):
		def convert(request_type, slot):
			tuning = self.tunings.get(request_type, None) or self
			sma = slot[0]
			metering = ar.deque()
			for s in sma:
				started_at = datetime.datetime.fromtimestamp(s[0], tz=ar.UTC)
				a = ApiSample(started_at=started_at, measured=s[1], average=s[2])
				metering.append(a)
			if len(metering) == 0:
				return ApiRequested(enabled=tuning.enabled, responsiveness=tuning.responsiveness, metering=metering)
			started_at = metering[0].started_at
			stopped_at = metering[-1].started_at + datetime.timedelta(seconds=metering[-1].measured)
			delta = stopped_at - started_at
			total_span = delta.total_seconds()
			return ApiRequested(enabled=tuning.enabled, responsiveness=tuning.responsiveness, average=metering[-1].average,
				started_at=started_at, stopped_at=stopped_at,
				total_span=total_span, metering=metering)
		if request_type:
			slot = self.stopped.get(request_type, None)
			if not slot:
				return ar.Nak()
			return convert(request_type, slot)
		d = {k: convert(k, v) for k, v in self.stopped.items()}
		return ApiReport(enabled=self.enabled, responsiveness=self.responsiveness, report=d)

#
#
class ConnectToAddress(ar.Point, ar.StateMachine):
	"""Maintain a connection to an IP address and port, perform retries.

	:param ipp: IP address and port to connect to
	:type ipp: HostPort
	:param keep_connected: restart retry sequence after successful connect
	:type keep_connected: bool
	:param session: object to be created on connection, or None
	:type session: CreateFrame
	:param group_address: where to forward session messages, or None
	:type group_address: async address
	"""
	def __init__(self, ipp, keep_connected=True, session=None, group_address=None, encrypted=False, api_client=None, ansar_server=False):
		ar.Point.__init__(self)
		ar.StateMachine.__init__(self, INITIAL)
		self.ipp = ipp
		self.keep_connected = keep_connected
		self.session = session
		self.group_address = group_address
		self.encrypted = encrypted
		self.api_client = api_client
		self.ansar_server = ansar_server

		self.started = None
		self.attempts = 0

		self.connected = None
		self.remote = None

		self.closing = None
		self.intervals = None
		self.retry = None

	def reschedule(self):
		if self.intervals is None:
			s = local_private_public(self.ipp.host)
			r = ip_retry(s)
			self.intervals = r
		
		if self.retry is None:
			self.retry = ar.smart_intervals(self.intervals)

		try:
			p = next(self.retry)
		except StopIteration:
			self.retry = None
			return False
	
		self.start(GlareTimer, p)
		return True

# INITIAL
# Launch this object.
def ConnectToAddress_INITIAL_Start(self, message):
	self.group_address = self.group_address or self.parent_address

	# Start from nothing.
	self.started = ar.world_now()
	connect(self, self.ipp, session=self.session,
		encrypted=self.encrypted,
		api_client=self.api_client, ansar_server=self.ansar_server)
	self.attempts = 1
	return PENDING

# PENDING
# Waiting for results of connect.
# Transport established.
def ConnectToAddress_PENDING_Connected(self, message):
	self.connected = message
	self.remote = self.return_address

	# Remote object is ready.
	self.send(UseAddress(self.return_address), self.parent_address)
	return CONNECTED

def ConnectToAddress_PENDING_NotConnected(self, message):
	# Attempt failed.
	# No session and no change of status for owner.
	# Schedule another or perhaps end of attempts.
	if self.reschedule():
		return GLARING

	x = ar.Exhausted(message, attempts=self.attempts, started=self.started)
	self.complete(x)

def ConnectToAddress_PENDING_Stop(self, message):
	# Local termination.
	# Connected could be orphaned here.
	self.complete(ar.Aborted())

# CONNECTED
# Caretaker role. Pass app messages on to owner
# and wait for further control messages.
def ConnectToAddress_CONNECTED_Unknown(self, message):
	# Normal operation.	Forward app message on to proper target.
	self.forward(message, self.group_address, self.return_address)
	return CONNECTED

def ConnectToAddress_CONNECTED_Abandoned(self, message):
	# Normal end of a session.
	# Are there intended to be others?
	if self.keep_connected:
		# Start the retries up again.
		self.started = ar.world_now()
		self.attempts = 0
		self.retry = None
		if self.reschedule():
			# Update the owner that the current session
			# is over.
			self.send(NoAddress(), self.parent_address)
			return GLARING
		# Will only happen on a retry value that
		# allows no retries.
		x = ar.Exhausted(message, attempts=self.attempts, started=self.started)
		self.complete(x)

	# End of session and only wanted 1.
	self.complete(message)

def ConnectToAddress_CONNECTED_Stop(self, message):
	# This object ended by app. Take that as
	# signal to end this session and not activate retries.

	e = ar.Stop() if self.session else Close(ar.Aborted())

	self.send(e, self.remote)
	return CLOSING

def ConnectToAddress_CONNECTED_Closed(self, message):
	# Local end has sent close to the proxy. Treat this
	# as a short-circuit version of above.
	self.complete(message.value)

# GLARING
# After a failed attempt or after abandoned.
def ConnectToAddress_GLARING_Unknown(self, message):
	# Non-control message sneaking through.
	self.forward(message, self.group_address, self.return_address)
	return GLARING

def ConnectToAddress_GLARING_GlareTimer(self, message):
	connect(self, self.ipp, session=self.session,
		encrypted=self.encrypted,
		api_client=self.api_client, ansar_server=self.ansar_server)
	self.attempts += 1
	return PENDING

def ConnectToAddress_GLARING_Stop(self, message):
	# Drop GlareTimer
	self.complete(ar.Aborted())

# CLOSING
def ConnectToAddress_CLOSING_Unknown(self, message):
	# Normal operation.	Forward app message on to proper target.
	self.forward(message, self.group_address, self.return_address)
	return CLOSING

def ConnectToAddress_CLOSING_Abandoned(self, message):
	# Terminated by remote before close could get through.
	self.complete(message)

def ConnectToAddress_CLOSING_Closed(self, message):
	# Completion of CONNECTED-Stop.
	self.complete(message.value)

CONNECT_TO_ADDRESS_DISPATCH = {
	INITIAL: (
		(ar.Start,), ()
	),
	PENDING: (
		(Connected, NotConnected, ar.Stop), ()
	),
	CONNECTED: (
		(ar.Unknown, Abandoned, ar.Stop, Closed), ()
	),
	GLARING: (
		(ar.Unknown, GlareTimer, ar.Stop), ()
	),
	CLOSING: (
		(ar.Unknown, Abandoned, Closed), ()
	),
}

ar.bind(ConnectToAddress, CONNECT_TO_ADDRESS_DISPATCH, thread='networking-session')

#
#
LISTEN_RETRY = ar.RetryIntervals(first_steps=[], regular_steps=4.0, randomized=0.25)

class ListenAtAddress(ar.Point, ar.StateMachine):
	"""Maintain a network presence at an IP address and port.

	:param ipp: IP address and port to listen at
	:type ipp: HostPort
	:param session: object to be created on accept, or None
	:type session: CreateFrame
	:param group_address: where to forward session messages, or None
	:type group_address: async address
	"""
	def __init__(self, ipp, session=None, group_address=None, encrypted=False, api_server=None, ansar_client=False):
		ar.Point.__init__(self)
		ar.StateMachine.__init__(self, INITIAL)
		self.ipp = ipp
		self.session = session
		self.group_address = group_address
		self.encrypted = encrypted
		self.api_server = api_server
		self.ansar_client = ansar_client

		self.started = None
		self.attempts = 0

		self.listening = None
		self.accepted = {}

		self.closing = None
		self.retry = None

	def reschedule(self):
		if self.retry is None:
			self.retry = ar.smart_intervals(LISTEN_RETRY)

		try:
			p = next(self.retry)
		except StopIteration:
			self.retry = None
			return False
	
		self.start(GlareTimer, p)
		return True

# INITIAL
# Launch this object.
def ListenAtAddress_INITIAL_Start(self, message):
	self.group_address = self.group_address or self.parent_address

	# Start from nothing.
	self.started = ar.world_now()
	listen(self, self.ipp, session=self.session,
		encrypted=self.encrypted,
		api_server=self.api_server, ansar_client=self.ansar_client)
	self.attempts = 1
	return PENDING

# PENDING
# Waiting for results of connect.
# Transport established.
def ListenAtAddress_PENDING_Listening(self, message):
	self.listening = message
	self.remote = self.return_address

	# Ready to accept
	self.send(UseAddress(self.address), self.parent_address)
	return ACCEPTING

def ListenAtAddress_PENDING_NotListening(self, message):
	# Attempt failed.
	# No session and no change of status for owner.
	# Schedule another or perhaps end of attempts.
	if self.reschedule():
		return GLARING

	x = ar.Exhausted(message, attempts=self.attempts, started=self.started)
	self.complete(x)

def ListenAtAddress_PENDING_Stop(self, message):
	# Local termination.
	# Listening could be orphaned here.
	self.complete(ar.Aborted())

# ACCEPTING
# Caretaker role. Pass app messages on to owner
# and wait for further control messages.
def ListenAtAddress_ACCEPTING_Accepted(self, message):
	# Start of a session.
	# Are there intended to be others?
	self.accepted[self.return_address] = message

	self.forward(message, self.parent_address, self.return_address)
	return ACCEPTING

def ListenAtAddress_ACCEPTING_Unknown(self, message):
	# Normal operation.	Forward app message on to proper target.
	self.forward(message, self.group_address, self.return_address)
	return ACCEPTING

def ListenAtAddress_ACCEPTING_Abandoned(self, message):
	a = self.accepted.pop(self.return_address, None)
	if a:
		self.forward(message, self.parent_address, self.return_address)
	return ACCEPTING

def ListenAtAddress_ACCEPTING_Closed(self, message):
	a = self.accepted.pop(self.return_address, None)
	if a:
		self.forward(message, self.parent_address, self.return_address)
	return ACCEPTING

def ListenAtAddress_ACCEPTING_Stop(self, message):
	if len(self.accepted) == 0:
		self.complete(ar.Aborted())

	e = ar.Stop() if self.session else Close(ar.Aborted())

	for k, v in self.accepted.items():
		self.send(e, k)
	return CLOSING

# GLARING
# After a failed attempt or after abandoned.
def ListenAtAddress_GLARING_Unknown(self, message):
	# Non-control message sneaking through.
	self.forward(message, self.group_address, self.return_address)
	return GLARING

def ListenAtAddress_GLARING_GlareTimer(self, message):
	listen(self, self.ipp, session=self.session,
		encrypted=self.encrypted,
		api_server=self.api_server, ansar_client=self.ansar_client)
	self.attempts += 1
	return PENDING

def ListenAtAddress_GLARING_Stop(self, message):
	# Drop GlareTimer
	self.complete(ar.Aborted())

# CLOSING
def ListenAtAddress_CLOSING_Abandoned(self, message):
	a = self.accepted.pop(self.return_address, None)
	if a and len(self.accepted) > 0:
		return CLOSING
	self.complete(message)

def ListenAtAddress_CLOSING_Closed(self, message):
	a = self.accepted.pop(self.return_address, None)
	if a and len(self.accepted) > 0:
		return CLOSING
	self.complete(message)

LISTEN_AT_ADDRESS_DISPATCH = {
	INITIAL: (
		(ar.Start,), ()
	),
	PENDING: (
		(Listening, NotListening, ar.Stop), ()
	),
	ACCEPTING: (
		(Accepted, ar.Unknown, Abandoned, Closed, ar.Stop), ()
	),
	GLARING: (
		(ar.Unknown, GlareTimer, ar.Stop), ()
	),
	CLOSING: (
		(Abandoned, Closed), ()
	),
}

ar.bind(ListenAtAddress, LISTEN_AT_ADDRESS_DISPATCH, thread='networking-session')

#
# Subscribe/Publish
class SubscribeToListing(ar.Point, ar.StateMachine):
	"""Maintain a connection to a published name.

	:param listing: the name of interest (not a regular expression)
	:type listing: str
	:param scope: highest level to look for a match
	:type scope: enumeration
	:param keep_connected: allow for multiple sessions
	:type keep_connected: bool
	:param session: object to be created on connection, or None
	:type session: CreateFrame
	:param group_address: where to forward session messages, or None
	:type group_address: async address
	"""
	def __init__(self, listing, scope=ScopeOfService.WAN, keep_connected=True, session=None, group_address=None):
		ar.Point.__init__(self)
		ar.StateMachine.__init__(self, INITIAL)
		self.listing = listing
		self.scope = scope
		self.keep_connected = keep_connected
		self.session = session
		self.group_address = group_address

		self.started = None
		self.attempts = 0

		self.subscribed = None
		self.available = None
		self.remote = None

		self.closing = None
		self.intervals = None
		self.retry = None

	def reschedule(self):
		if self.intervals is None:
			s = local_private_public(self.ipp.host)
			r = ip_retry(s)
			self.intervals = r
		
		if self.retry is None:
			self.retry = ar.smart_intervals(self.intervals)

		try:
			p = next(self.retry)
		except StopIteration:
			self.retry = None
			return False
	
		self.start(GlareTimer, p)
		return True

# INITIAL
# Launch this object.
def SubscribeToListing_INITIAL_Start(self, message):
	self.group_address = self.group_address or self.parent_address

	# Start from nothing.
	self.started = ar.world_now()
	subscribe(self, self.listing, create_session=self.session, requested_scope=self.scope)
	self.attempts = 1
	return PENDING

# PENDING
# Waiting for results of subscibe.
# Subscription acknowledged.
def SubscribeToListing_PENDING_Subscribed(self, message):
	self.subscribed = message
	return READY

def SubscribeToListing_PENDING_NotSubscribed(self, message):
	self.complete(message)

def SubscribeToListing_PENDING_Stop(self, message):
	# Local termination.
	# Subscribed could be orphaned here.
	self.complete(ar.Aborted())

# READY
# Waiting for availability.
# Subscription acknowledged.
def SubscribeToListing_READY_Available(self, message):
	self.available = message
	self.remote = self.return_address

	# Remote object is ready.
	self.send(UseAddress(self.return_address), self.parent_address)
	return CONNECTED

def SubscribeToListing_READY_Stop(self, message):
	retract(self)
	self.complete(ar.Aborted())

# CONNECTED
# Caretaker role. Pass app messages on to owner
# and wait for further control messages.
def SubscribeToListing_CONNECTED_Unknown(self, message):
	# Normal operation.	Forward app message on to proper target.
	self.forward(message, self.group_address, self.return_address)
	return CONNECTED

def SubscribeToListing_CONNECTED_Dropped(self, message):
	# Normal end of a session.
	# Are there intended to be others?
	self.send(NoAddress(), self.parent_address)
	if self.keep_connected:
		return READY

	# End of session and only wanted 1.
	self.complete(message)

def SubscribeToListing_CONNECTED_Cleared(self, message):
	# Normal end of a session.
	# Are there intended to be others?
	self.send(NoAddress(), self.parent_address)
	if self.keep_connected:
		return READY

	# End of session and only wanted 1.
	self.complete(message.value)

def SubscribeToListing_CONNECTED_Stop(self, message):
	# This object ended by app. Take that as
	# signal to end this session and not activate retries.

	self.complete(ar.Aborted())

	#e = ar.Stop() if self.session else Close(ar.Aborted())

	#self.send(e, self.remote)
	#return CLOSING

# CLOSING
def SubscribeToListing_CLOSING_Unknown(self, message):
	# Normal operation.	Forward app message on to proper target.
	self.forward(message, self.group_address, self.return_address)
	return CLOSING

def SubscribeToListing_CLOSING_Abandoned(self, message):
	# Terminated by remote before close could get through.
	retract(self)
	self.complete(message)

def SubscribeToListing_CLOSING_Closed(self, message):
	# Completion of CONNECTED-Stop.
	retract(self)
	self.complete(message.value)

SUBSCRIBE_TO_LISTING_DISPATCH = {
	INITIAL: (
		(ar.Start,), ()
	),
	PENDING: (
		(Subscribed, ar.Stop), ()
	),
	READY: (
		(Available, ar.Stop), ()
	),
	CONNECTED: (
		(ar.Unknown, Dropped, Cleared, ar.Stop), ()
	),
	CLOSING: (
		(ar.Unknown, Abandoned, Closed), ()
	),
}

ar.bind(SubscribeToListing, SUBSCRIBE_TO_LISTING_DISPATCH, thread='networking-session')

#
#
class PublishAListing(ar.Point, ar.StateMachine):
	"""Maintain a network presence at a name.

	:param listing: the name this object will be known by
	:type listing: str
	:param session: object to be created on delivery, or None
	:type session: CreateFrame
	:param group_address: where to forward session messages, or None
	:type group_address: async address
	"""
	def __init__(self, listing, scope=ScopeOfService.WAN, session=None, group_address=None):
		ar.Point.__init__(self)
		ar.StateMachine.__init__(self, INITIAL)
		self.listing = listing
		self.scope = scope
		self.session = session
		self.group_address = group_address

		self.started = None
		self.attempts = 0

		self.published = None
		self.delivered = {}

		self.closing = None
		self.retry = None

	def reschedule(self):
		if self.retry is None:
			self.retry = ar.smart_intervals(LISTEN_RETRY)

		try:
			p = next(self.retry)
		except StopIteration:
			self.retry = None
			return False
	
		self.start(GlareTimer, p)
		return True

# INITIAL
# Launch this object.
def PublishAListing_INITIAL_Start(self, message):
	self.group_address = self.group_address or self.parent_address

	# Start from nothing.
	self.started = ar.world_now()
	publish(self, self.listing, create_session=self.session, requested_scope=self.scope)
	self.attempts = 1
	return PENDING

# PENDING
# Waiting for results of publish.
# Listing established.
def PublishAListing_PENDING_Published(self, message):
	self.published = message

	# Ready to accept
	self.send(UseAddress(self.address), self.parent_address)
	return ACCEPTING

def PublishAListing_PENDING_NotPublished(self, message):
	self.complete(message)

def PublishAListing_PENDING_Stop(self, message):
	# Local termination.
	retract(self)
	self.complete(ar.Aborted())

# ACCEPTING
# Caretaker role. Pass app messages on to owner
# and wait for further control messages.
def PublishAListing_ACCEPTING_Delivered(self, message):
	# Start of a session.
	# Are there intended to be others?
	self.delivered[self.return_address] = message

	self.forward(message, self.parent_address, self.return_address)
	return ACCEPTING

def PublishAListing_ACCEPTING_Unknown(self, message):
	# Normal operation.	Forward app message on to proper target.
	self.forward(message, self.group_address, self.return_address)
	return ACCEPTING

def PublishAListing_ACCEPTING_Dropped(self, message):
	a = self.delivered.pop(self.return_address, None)
	if a:
		self.forward(message, self.parent_address, self.return_address)
	return ACCEPTING

def PublishAListing_ACCEPTING_Cleared(self, message):
	a = self.delivered.pop(self.return_address, None)
	if a:
		self.forward(message, self.parent_address, self.return_address)
	return ACCEPTING

def PublishAListing_ACCEPTING_Stop(self, message):
	retract(self)
	self.complete(ar.Aborted())
	#if len(self.delivered) == 0:
	#	retract(self)
	#	self.complete(ar.Aborted())
	#
	#e = ar.Stop() if self.session else Close(ar.Aborted())
	#
	#for k, v in self.delivered.items():
	#	self.send(e, k)
	#return CLOSING

# CLOSING
def PublishAListing_CLOSING_Dropped(self, message):
	a = self.delivered.pop(self.return_address, None)
	if a and len(self.delivered) > 0:
		return CLOSING
	retract(self)
	self.complete(message)

def PublishAListing_CLOSING_Cleared(self, message):
	a = self.delivered.pop(self.return_address, None)
	if a and len(self.delivered) > 0:
		return CLOSING
	retract(self)
	self.complete(message)

PUBLISH_A_LISTING_DISPATCH = {
	INITIAL: (
		(ar.Start,), ()
	),
	PENDING: (
		(Published, NotPublished, ar.Stop), ()
	),
	ACCEPTING: (
		(Delivered, ar.Unknown, Dropped, Cleared, ar.Stop), ()
	),
	CLOSING: (
		(Dropped, Cleared), ()
	),
}

ar.bind(PublishAListing, PUBLISH_A_LISTING_DISPATCH, thread='networking-session')

#
#
class SubscribeToSearch(ar.Point, ar.StateMachine):
	"""Maintain connections with multiple published names.

	:param listing: the names to search for (regular expression)
	:type listing: str
	:param scope: highest level to look for a match
	:type scope: enumeration
	:param session: object to be created on connection, or None
	:type session: CreateFrame
	:param group_address: where to forward session messages, or None
	:type group_address: async address
	"""
	def __init__(self, search, scope=ScopeOfService.WAN, session=None, group_address=None):
		ar.Point.__init__(self)
		ar.StateMachine.__init__(self, INITIAL)
		self.search = search
		self.scope = scope
		self.session = session
		self.group_address = group_address

		self.started = None
		self.attempts = 0

		self.subscribed = None
		self.available = {}

		self.closing = None
		self.retry = None

	def reschedule(self):
		if self.retry is None:
			self.retry = ar.smart_intervals(LISTEN_RETRY)

		try:
			p = next(self.retry)
		except StopIteration:
			self.retry = None
			return False
	
		self.start(GlareTimer, p)
		return True

# INITIAL
# Launch this object.
def SubscribeToSearch_INITIAL_Start(self, message):
	self.group_address = self.group_address or self.parent_address

	# Start from nothing.
	self.started = ar.world_now()
	subscribe(self, self.search, create_session=self.session, requested_scope=self.scope)
	self.attempts = 1
	return PENDING

# PENDING
# Waiting for results of publish.
# Listing established.
def SubscribeToSearch_PENDING_Subscribed(self, message):
	self.subscribed = message

	# Ready to accept
	self.send(UseAddress(self.address), self.parent_address)
	return ACCEPTING

def SubscribeToSearch_PENDING_NotSubscribed(self, message):
	self.complete(message)

def SubscribeToSearch_PENDING_Stop(self, message):
	# Local termination.
	retract(self)
	self.complete(ar.Aborted())

# ACCEPTING
# Caretaker role. Pass app messages on to owner
# and wait for further control messages.
def SubscribeToSearch_ACCEPTING_Available(self, message):
	# Start of a session.
	# Are there intended to be others?
	self.available[self.return_address] = message

	self.forward(message, self.parent_address, self.return_address)
	return ACCEPTING

def SubscribeToSearch_ACCEPTING_Unknown(self, message):
	# Normal operation.	Forward app message on to proper target.
	self.forward(message, self.group_address, self.return_address)
	return ACCEPTING

def SubscribeToSearch_ACCEPTING_Dropped(self, message):
	a = self.available.pop(self.return_address, None)
	if a:
		self.forward(message, self.parent_address, self.return_address)
	return ACCEPTING

def SubscribeToSearch_ACCEPTING_Cleared(self, message):
	a = self.available.pop(self.return_address, None)
	if a:
		self.forward(message, self.parent_address, self.return_address)
	return ACCEPTING

def SubscribeToSearch_ACCEPTING_Stop(self, message):
	retract(self)
	self.complete(ar.Aborted())
	#if len(self.available) == 0:
	#	retract(self)
	#	self.complete(ar.Aborted())
	#
	#e = ar.Stop() if self.session else Close(ar.Aborted())
	#
	#for k, v in self.available.items():
	#	self.send(e, k)
	#return CLOSING

# CLOSING
def SubscribeToSearch_CLOSING_Dropped(self, message):
	a = self.available.pop(self.return_address, None)
	if a and len(self.available) > 0:
		return CLOSING
	retract(self)
	self.complete(message)

def SubscribeToSearch_CLOSING_Cleared(self, message):
	a = self.available.pop(self.return_address, None)
	if a and len(self.available) > 0:
		return CLOSING
	retract(self)
	self.complete(message)

SUBSCRIBE_TO_SEARCH_DISPATCH = {
	INITIAL: (
		(ar.Start,), ()
	),
	PENDING: (
		(Subscribed, ar.Stop), ()	# NotSubscribed?!
	),
	ACCEPTING: (
		(Available, ar.Unknown, Dropped, Cleared, ar.Stop), ()
	),
	CLOSING: (
		(Dropped, Cleared), ()
	),
}

ar.bind(SubscribeToSearch, SUBSCRIBE_TO_SEARCH_DISPATCH, thread='networking-session')
