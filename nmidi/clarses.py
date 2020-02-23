from itertools import accumulate
import mido as midi_io
MIN_NOTE_OFF_TIME = 4


class Note_Status:
	def __init__(self, match_note:int, channel):
		self.channel = channel
		self.note_number = match_note
		self.is_on = False
		self.events = []

	def on(self,_time):
		if not self.is_on:
			self.events.append(("on", _time))
			self.is_on = True
		else:
			print("error: not is already on")
	def off(self,_time):
		if self.is_on:
			self.events.append(("off", _time))
			self.is_on = False
		else:
			print("error: not is already off")
	
	def itter_onoffs(self):
		is_on = False
		on_time = -1
		if self.channel.track.is_muted:
			return
		for item in self.events:
			if item[0]=="on" and not is_on:
				on_time = item[1]
				is_on = True
			if item[0]=="on" and is_on:
				print("fk me",item[1]-on_time)
				
			if item[0]=="off":
				if is_on:
					yield on_time,item[1]
					is_on = False
				else:
					print("fuuuuck")


class Port:
	def __init__():
		self._chann els = [Channel(i) for i in range(16)]


class Channel:
	def __init__(self,track):
		self.track = track
		self._status = [Note_Status(i) for i in range(128)]
		
	def on(self,note,_time):
		if note not in self.note_statuses:
			self.note_statuses[note] = Note_Status(note,self)
		self.note_statuses[note].on(_time)
	def off(self,note,_time):
		if note not in self.note_statuses:
			print("error: note_off is first event added to channel")
			self.note_statuses[note] = Note_Status(note)
		self.note_statuses[note].off(_time)

class Track:
	def __init__(self, track):
		self.channels = {}
		self.is_muted = False
		self.transposed_by = 0
		_time = 0
		for event in track:
			_e = event.dict()
			_time += _e['time']
			if _e["type"] not in ("note_on","note_off"):
				continue
			# TODO: handel any change of tempo here somewheres
			if _e['channel'] not in self.channels:
				self.channels[_e['channel']] = Channel(self)

			if _e["type"] == "note_on" and _e["velocity"]>0:
				self.channels[_e['channel']].on(_e["note"],_time)
			elif (_e["type"] == "note_on" and _e["velocity"]==0) or _e["type"] == "note_off":
				self.channels[_e['channel']].off(_e["note"],_time)
		self.total_time = _time
	def transpose(self, num_notes):
		self.transposed_by += num_notes
	def un_mute(self):
		self.is_muted = False
	def mute(self):
		self.is_muted = True
	

class Song:
	def __init__(self, midi:midi_io.MidiFile):
		 
		self.tracks = []
		self.total_time = 0
		for index, track in enumerate(midi.tracks):
			new_track = Track(track)
			if new_track.channels:
				self.tracks.append(new_track)
				if new_track.total_time>self.total_time:
					self.total_time = new_track.total_time