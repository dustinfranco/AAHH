import os
from misc_config import songs_dir as sd

def convert_song(song_name):
  original_dir = sd + song_name
  convert_dir = sd + song_name + "_conv"
  if os.path.exists(convert_dir):
    print(convert_dir)
  else:
    os.mkdir(convert_dir)
  sections = os.listdir(original_dir)
  for old_sec in sections:
    if "song" not in old_sec and "compile" not in old_sec:
      x = original_dir + "/" + old_sec
      x = open(x,"r")
      x.readline()
      out_sec = ""
      for m in range(0, 6):
        z = x.readline()[1::2]
        out_sec += z + "\n"
      q = open(convert_dir + "/" + old_sec, "w+")
      q.write(out_sec)
      q.close()

if __name__ == "__main__":
  convert_song("beardscalp")