newpath = '/home/pi/Desktop/Songs/' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

def compileSong(songName):
	print ("compile song not complete");

def editSong(songName):
	print ("editSong not complete");

def playSong(songName):
	print ("playSong not complete");

def createNewSong(songName):
	genericSections = ["a", "b", "c", "d", "e", "f", "g", "h"]
	genericSongStructure = ["i", "m", "c", "b", "o"]
	if not os.path.exists(newpath):
	    os.makedirs(newpath + songName)
	    for structure in genericSongStructure:
			for section in genericSections:
	    		os.makedirs(newpath + songName + "/" + structure + section + ".txt");
				
		print "creating new song"
	else :
		print "song already exists"
	print ("createNewSong not complete");
