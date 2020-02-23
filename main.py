
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import mido as midi_io

import nmidi

root = tk.Tk()
root.width = 2000
root.height = 2000
#root.withdraw()
root.iconbitmap(r'resource/favicon.ico')
file_path = filedialog.askopenfilename()

try:
	midifile = midi_io.MidiFile(file_path)
except:
	tk.messagebox.showerror("MIDI NOPE!", "AVAST YE SCURVEY DOG; SELECT YE A VALID MIDI FILE!")
	quit()

song = nmidi.Song(midifile)

song.tracks[0].transpose(-8)
song.tracks[1].mute()
song.tracks[2].transpose(-1)


c = tk.Canvas(root, width=2000, height=1500, background="black")
c.pack()


color = ["red", "green", "blue", "yellow", "orange", "purple", "cyan", "magenta", "grey"]

numt = len(song.tracks)

note_height = 1500/128/numt

built_pipes = {38,40,43,45,47,48,49,50,51,52,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,71,72,73,74,75,76}

for yy in range(0,128,2):
	x = 0
	y = yy * note_height * numt
	w = 2000.0
	h = note_height * numt
	r = c.create_rectangle(x, y, x+w, y+h, fill="#050505", outline="")

for yy in range(0,128,1):
	x = 0
	y = yy * note_height * numt
	w = 10
	h = note_height * numt
	nncol = "#000000"
	if yy in built_pipes:
		nncol = "#FFFFFF"
	r = c.create_rectangle(x, y, x+w, y+h, fill=nncol, outline="")

for track_index, track in enumerate(song.tracks):
	for channel_number, channel in track.channels.items():
		for note_number, note_status in channel.note_statuses.items():
			for note_start_time, note_end_time in note_status.itter_onoffs():
				x = float(note_start_time) / float(song.total_time) * 2000.0
				y = (note_number * numt + track_index) * note_height
				w = float(note_end_time - note_start_time) / float(song.total_time) * 2000.0
				h = note_height
				nncol = "#202020"
				if note_number in built_pipes:
					nncol = color[track_index]
				r = c.create_rectangle(x, y, x+w, y+h, fill=nncol, outline="")

root.mainloop()






