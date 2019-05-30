from misc_config import songs_dir as sd
from note_config import note_config as nc
import os

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
          section_out += nc[strings[x] + temp_note]
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
  print USD
  complete_song = create_song(SSA, USD)
  print complete_song
  save_song(target_dir, complete_song)

if __name__ == "__main__":
  compile_song("allnotes_2")
  compile_song("beardscalp_conv")
