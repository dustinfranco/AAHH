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

def compileAllMeasures(songName):
    print("compile all mesures not complete")

def compileMeasure(songName, measureName):
    print("compiling " + songName + " measure " + measureName)
    measureString = open(basePath + songName + "/" + measureName)
    string = 0;
    noteArrayOutput = [];
    print ("THIS: " + str(len(activePins)))
    stringOffset = [0,5,10,15,20,25];
    for line in measureString:
        subindex = 0;
        for x in range(0,len(line)-1,2):
            tempNote = line[x] + line[x+1];
            if(string == 0):
                if(tempNote != "||"):
                    noteArrayOutput.append([0]);
                    noteArrayOutput.append([0]);
            if(tempNote != "||" and tempNote != "--"):
                #thebest
                tempTempNote = int(tempNote);
                tempTempNote = string + tempTempNote * 6;
                print("tempnote value " + str(tempTempNote))
                tempTempNote = activePins[tempTempNote];
                noteArrayOutput[subindex].append(tempTempNote);
                noteArrayOutput[subindex + 1].append(tempTempNote);
            if(tempNote != "||"):
                subindex += 2
        string += 1;
    return noteArrayOutput;

def concatMeasure(inputMeasureA, inputMeasureB):
    for noteArray in inputMeasureB:
        inputMeasureA.append(noteArray);
    return inputMeasureA

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
m = []
for measure in w:
    w[measure] = compileMeasure("abcd", measure);
for measure in q:
    z = w[measure];
    m = concatMeasure(m, z)

print(m)