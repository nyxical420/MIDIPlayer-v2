import keyboard
import threading
import colorama
import re
import os

global isPlaying
global infoTuple
global roblox

isPlaying = False
roblox    = False
index     = 0
conversionCases = {'!': '1', '@': '2', '£': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0'}
fontColor = colorama.Fore
fontBG = colorama.Back

def processMIDI():
	global playback_speed
	with open("song.txt","r") as macro_file:
		lines = macro_file.read().split("\n")
		tOffsetSet = False
		tOffset = 0
		playback_speed = float(lines[0].split("=")[1])
		tempo = 60/float(lines[1].split("=")[1])
		
		processedNotes = []
		
		for l in lines[1:]:
			l = l.split(" ")
			if(len(l) < 2):
				continue
			
			waitToPress = float(l[0])
			notes = l[1]
			processedNotes.append([waitToPress,notes])
			if(not tOffsetSet):
				tOffset = waitToPress
				tOffsetSet = True

	return [tempo,tOffset,processedNotes]

def parseInfo():
	tempo = infoTuple[0]
	notes = infoTuple[2][1:]
	i = 0
	while i < len(notes)-1:
		note = notes[i]
		nextNote = notes[i+1]
		if "tempo" in note[1]:
			tempo = 60/float(note[1].split("=")[1])
			notes.pop(i)

			note = notes[i]
			if i < len(notes)-1:
				nextNote = notes[i+1]
		else:
			note[0] = (nextNote[0] - note[0]) * tempo
			i += 1

	notes[len(notes)-1][0] = 1.00
	return notes

def ftz(n):
	if(n > 0):
		return n
	else:
		return 0

def playNextNote():
	global isPlaying
	global index
	global playback_speed
	global roblox

	notes = infoTuple[2]
	if isPlaying and index < len(infoTuple[2]):
		noteInfo = notes[index]
		delay = ftz(noteInfo[0])

		if roblox == True:
			if noteInfo[1][0] == "~":
				delay = delay
			else:
				if delay == 0:
					delay = 0.03
			if len(noteInfo[1]) >= 11:
				index += 1
				return playNextNote()

		white = '+'.join(c for c in noteInfo[1] if c.islower())
		black = '+'.join(c for c in noteInfo[1] if c.isupper()).lower()
		symbl = '+'.join(re.sub('[a-z]+', '', f"{noteInfo[1]}".lower())).replace("~", "")
		numbr = '+'.join(c for c in noteInfo[1] if c.isdigit())

		if noteInfo[1][0] == "~":
			notes = noteInfo[1][1:]
			white = '+'.join(c for c in notes if c.islower())
			black = '+'.join(c for c in notes if c.isupper()).lower()
			symbl = '+'.join(re.sub('[a-z]+', '', f"{notes}".lower()))
			numbr = '+'.join(c for c in notes if c.isdigit())


			if symbl != "":
				keyboard.release(f"{symbl}")

			if black != "":
				keyboard.release(f"{black}")

			if numbr != "":
				keyboard.release(f"{numbr}")

			if white != "":
				keyboard.release(f"{white}")
				
			if len(noteInfo[1]) - 1 == 1:
				note = noteInfo[1] + "         "
			if len(noteInfo[1]) - 1 == 2:
				note = noteInfo[1] + "        "
			if len(noteInfo[1]) - 1 == 3:
				note = noteInfo[1] + "       "
			if len(noteInfo[1]) - 1 == 4:
				note = noteInfo[1] + "      "
			if len(noteInfo[1]) - 1 == 5:
				note = noteInfo[1] + "     "
			if len(noteInfo[1]) - 1 == 6:
				note = noteInfo[1] + "    "
			if len(noteInfo[1]) - 1 == 7:
				note = noteInfo[1] + "   "
			if len(noteInfo[1]) - 1 == 8:
				note = noteInfo[1] + "  "
			if len(noteInfo[1]) - 1 == 9:
				note = noteInfo[1] + " "
			if len(noteInfo[1]) - 1 == 10:
				note = noteInfo[1]
			if len(noteInfo[1]) - 1 >= 11:
				note = colorama.Back.LIGHTRED_EX + " 10+ Keys " + colorama.Back.RESET

			print(colorama.Fore.LIGHTRED_EX + f"{index:06} ↑ {note[1:]} | {delay}")
		
		if "~" not in noteInfo[1]:
			keyboard.press("shift")
			if symbl != "":
				keyboard.press(f"{symbl}")

			if black != "":
				keyboard.press(f"{black}")

			keyboard.release("shift")
			keyboard.release("shift")

			if numbr != "":
				keyboard.press(f"{numbr}")

			if white != "":
				keyboard.press(f"{white}")
			if len(noteInfo[1]) == 1:
				note = noteInfo[1] + "         "
			if len(noteInfo[1]) == 2:
				note = noteInfo[1] + "        "
			if len(noteInfo[1]) == 3:
				note = noteInfo[1] + "       "
			if len(noteInfo[1]) == 4:
				note = noteInfo[1] + "      "
			if len(noteInfo[1]) == 5:
				note = noteInfo[1] + "     "
			if len(noteInfo[1]) == 6:
				note = noteInfo[1] + "    "
			if len(noteInfo[1]) == 7:
				note = noteInfo[1] + "   "
			if len(noteInfo[1]) == 8:
				note = noteInfo[1] + "  "
			if len(noteInfo[1]) == 9:
				note = noteInfo[1] + " "
			if len(noteInfo[1]) == 10:
				note = noteInfo[1]
			if len(noteInfo[1]) >= 11:
				note = colorama.Back.LIGHTRED_EX + " 10+ Keys " + colorama.Back.RESET

			print(colorama.Fore.LIGHTYELLOW_EX + f"{index:06} ↓ {note} | {delay}")

		index += 1
		if(delay == 0):
			playNextNote()
		else:
			threading.Timer(delay/playback_speed, playNextNote).start()

	elif index > len(infoTuple[2])-1:
		print(colorama.Fore.LIGHTGREEN_EX + f"[MIDI Player] MIDI Finished Playing")
		os.system("title MIDI Player")
		isPlaying = False
		index = 0

def playerAction(event):
	global isPlaying
	isPlaying = not isPlaying

	if isPlaying:
		os.system(f"title MIDI Player - Playing")
		print(colorama.Fore.LIGHTGREEN_EX + "[MIDI Player] Playing MIDI")
		playNextNote()
	else:
		os.system("title MIDI Player - Paused")
		print(colorama.Fore.LIGHTRED_EX + "[MIDI Player] Player Paused")

	return True

def rewind(KeyboardEvent):
	global index
	if index - 10 < 0:
		index = 0
		
	else:
		index -= 10
	print(colorama.Fore.LIGHTGREEN_EX + f"[MIDI Player] Rewinded to {index}")

def skip(KeyboardEvent):
	global index
	if index + 10 > len(infoTuple[2]):
		isPlaying = False
		index = 0
	else:
		index += 10
	print(colorama.Fore.LIGHTGREEN_EX + f"[MIDI Player] Skipped to {index}")

def robloxMode(KeyboardEvent):
	global roblox
	if roblox == False:
		roblox = True
		print(colorama.Fore.LIGHTGREEN_EX + f"[MIDI Player] Enabled Roblox Mode")
	else:
		print(colorama.Fore.LIGHTGREEN_EX + f"[MIDI Player] Disabled Roblox Mode")
		roblox = False

def read(event):
	global isPlaying
	if isPlaying == True:
		print(colorama.Fore.LIGHTRED_EX + "[MIDI Player] Cannot refresh MIDI while playing!")
	
	else:
		global infoTuple
		global index
		infoTuple = processMIDI()
		infoTuple[2] = parseInfo()
		index = 0
		print(colorama.Fore.LIGHTGREEN_EX + "[MIDI Player] Refreshed MIDI!")

def main():
	global isPlaying
	global infoTuple
	global playback_speed
	infoTuple = processMIDI()
	infoTuple[2] = parseInfo()

	home = (36,)
	insert = (82,)
	delete = (83,)
	end = (79,)
	pagedown = (81,)


	keyboard.on_press_key(delete, playerAction) # Play / Pause MIDI Player
	keyboard.on_press_key(insert, read)         # Process MIDI (Refresh)
	keyboard.on_press_key(end, rewind)          # Rewind
	keyboard.on_press_key(pagedown, skip)       # Skip

	os.system("cls")

	print("MIDI Player v2 | xacvwe/MIDIPlayer-v2")
	print("Controls - - - - - - - - - - - - - - -")
	print("[HOME] Refresh Player Song            ")
	print("[DELETE] Play / Pause Player          ")
	print("[END / PGDWN] Rewind / Skip           ")
	print()

	while True:
	    input("")


if __name__ == "__main__":
    main()
