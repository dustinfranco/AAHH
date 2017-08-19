import os
from pinMeta import activePins;
#basePath = "/home/pi/Desktop/Songs/"
print (activePins)
basePath = "/Users/dustinfranco/Desktop/Songs/"
if not os.path.exists(basePath):
    print("creating songs folder");
    os.makedirs(basePath);

def createArrayFromStructure(songName):
    songSequencePath = basePath + songName + "/songSequence";
    if(not os.path.exists(songSequencePath)):
        return "empty song sequence"
    else:
        x = open(songSequencePath, "r");
        z = [];

        for line in x:
            y = "";
            for char in line:
                if(char == "," or char == "\n"):
                    z.append(y);
                    y = "";
                else:
                    y += char


            print(line + "\n");
        print("z");
        print(z);
    return z
def findUniqueMeasures(inputSongStructureArray):
    uniqueMeasures = {};
    for measureName in inputSongStructureArray:
        if(measureName not in uniqueMeasures):
            print("here")
            uniqueMeasures[measureName] = [];
    return uniqueMeasures


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
createNewSong("abcd")
q = createArrayFromStructure("abcd")
w = findUniqueMeasures(q)
print(w)