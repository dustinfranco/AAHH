from misc_config import songs_dir as sd
from note_config import note_config as nc
import pprint
import os

UNUSED_NOTE_TRACKER = [
  "E0","A0","G0","D0","B0","e0",
  "E1","A1","G1","D1","B1","e1",
  "E2","A2","G2","D2", "B2","e2",
  "E3","A3","G3","D3","B3","e3",
  "E4","A4","G4","D4","B4","e4",
]

NOTE_USES = {}
for note in UNUSED_NOTE_TRACKER:
  NOTE_USES[note] = 0



def create_song_sequence_array(song_dir):
  sequence_string = open(song_dir + "song_sequence", "r").read()
  sequence_string = sequence_string.replace("\n",",")
  sequence_array = sequence_string.split(",")
  while "" in sequence_array:
    sequence_array.remove("")
  return sequence_array

def file_to_section(target_dir, section_name):
  section_out = ""
  #section as tab:
  SAT = open(target_dir + section_name, "r")
  strings = ["E", "A", "D", "G", "B", "e"]
  lines = []
  #for old files
  for x in range (0,6):
    temp_line = SAT.readline()
    temp_line = temp_line.replace("\n","")
    temp_line = temp_line.replace("|","")
    lines.append(temp_line)
  for m in range(0,len(lines[0])):
    for q in range(0,2):
      for x in range(0,6):
        temp_note = lines[x][m]
        if(temp_note != '-'):
          temp_note = strings[x] + temp_note
          #print " NOTE : " + temp_note
          if (temp_note in UNUSED_NOTE_TRACKER):
            print "removing " + temp_note
            UNUSED_NOTE_TRACKER.remove(temp_note)
          NOTE_USES[temp_note] += 1
          section_out += nc[temp_note]
      section_out += "\n"
  return section_out

def create_unique_dictionary(target_dir, SSA):
  u_dict = {}
  for section in SSA:
    if section[0] != "-":
      if section not in u_dict:
        #print("unique section name " + section)
        u_dict[section] = file_to_section(target_dir, section)
  return u_dict

def create_song(SSA, USD):
  #song as string:
  SAS = ""
  for section in SSA:
    if section[0] == "-":
      #calculate BPM change
      SAS += str(30.0/int(section)) + "\n"
    else:
      SAS += USD[section]
  return SAS

def save_song(target_dir, song_as_string):
  compiled_song_file = open(target_dir + "compiled_song", "w+")
  compiled_song_file.write(song_as_string)

def compile_song(song_name = None):
  target_dir = sd + song_name + "/"
  SSA = create_song_sequence_array(target_dir)
  USD = create_unique_dictionary(target_dir, SSA)
  #print USD
  complete_song = create_song(SSA, USD)
  #print complete_song
  print "this is pretty?"
  pprint.pprint(UNUSED_NOTE_TRACKER)
  pprint.pprint(NOTE_USES)
  save_song(target_dir, complete_song)

if __name__ == "__main__":
  compile_song("beardscalp_conv")
  compile_song("allnotes_2")