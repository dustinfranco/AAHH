import os
#basePath = "/home/pi/Desktop/Songs/"
basePath = "/Users/dustinfranco/Desktop/Songs/"
if not os.path.exists(basePath):
    print("creating songs folder");
    os.makedirs(basePath);
def compileSong(songName):
    print("compile song not complete");

def editSong(songName):
        print("editSong not comlete");

def playSong(songName):
    print("playSong not complete");

def createNewSong(songName, timeSignature = 4):
    genericSections = ["a", "b", "c", "d", "e", "f", "g", "h"]
    genericSongStructure = ["i", "m", "c", "b", "o"]
    if(not os.path.exists(basePath + songName)):
        os.makedirs(basePath + songName);
        for structure in genericSongStructure:
            for section in genericSections:
                newFile = basePath + songName + "/" + structure + section
                x = open(newFile, "w")
                os.utime(newFile, None)
                for m in range(0,6):
                    for i in range (0,timeSignature):
                        for j in range (0,4):
                            x.write("--");
                        if(i < timeSignature - 1):
                            x.write("||");
                    x.write("\n");
                songSequence = basePath + songName + "/" + "songSequence";
                x = open(songSequence, "w")
                os.utime(newFile, None)
                x.write("ia,ia,ib,ic\nma,mb,mc,md\n")
               
