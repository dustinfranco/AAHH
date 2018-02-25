import os
import time
import copy
from pinMeta import activePins;
from pinMeta import hardwareNumberTable;
from subprocess import Popen, PIPE

basePath = "/home/pi/Desktop/Songs/"
print (activePins)
#basePath = "/Users/dustinfranco/Desktop/Songs/"
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
    return z

def findUniqueMeasures(inputSongStructureArray):
    uniqueMeasures = {};
    for measureName in inputSongStructureArray:
        if(measureName not in uniqueMeasures):
            uniqueMeasures[measureName] = [];
    return uniqueMeasures


def compileSong(songName):
    print("compile song not complete");

def compileAllMeasures(songName):
    print("compile all mesures not complete")

def compileMeasure(songName, measureName):
    print("compiling " + songName + " measure " + measureName)
    measureString = open(basePath + songName + "/" + measureName)
    string = -1;
    noteArrayOutput = [];
    stringOffset = [0,5,10,15,20,25];
    for line in measureString:
        if(string == -1):
            noteArrayOutput.append([int(line)]);
            noteArrayOutput[0].append(0);
        else:
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
                    tempTempNote = hardwareNumberTable[activePins[tempTempNote]];
                    noteArrayOutput[subindex] = [tempTempNote] + noteArrayOutput[subindex];
                    noteArrayOutput[subindex + 1] = [tempTempNote] + noteArrayOutput[subindex + 1];
                if(tempNote != "||"):
                    subindex += 2
        string += 1;
    return noteArrayOutput;

def optomizeMeasure(inputMeasure, optomize = 1):
    optomizeNotes = []
    for subArray in inputMeasure:
        for note in subArray:
            if(len(optomizeNotes) == optomize):
                return inputMeasure
            if(note):
                if(note not in optomizeNotes):
                    subArray.remove(note);
                    optomizeNotes.append(note);
                    inputMeasure[0] = [note] + inputMeasure[0]
    return inputMeasure

def concatMeasure(inputMeasureA, inputMeasureB):
    for noteArray in inputMeasureB:
        inputMeasureA.append(noteArray);
    return inputMeasureA

def saveNoteArrayToFile(inputNoteArray, songName, sectionName = "temp", timeSignature = 4):
    newFile = basePath + songName + "/compiledSections/" + sectionName
    #lol
    noteCount = 0;
    noteMax = 1 + timeSignature * 8;
    if(not os.path.exists(basePath + songName + "/compiledSections/" )):
        print("creating that shit")
        os.makedirs(basePath + songName + "/compiledSections/" );
    else:
        print("shit created")
    x = open(newFile, "w+");
    for subArray in inputNoteArray:
        for note in subArray:
            if(note != 0):
                x.write(str(note) + " ")
            else:
                noteCount +=1
                x.write("0" + "\n")
                if(noteCount == noteMax):
                    noteCount = 0;
                    x.write("\r\n")




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
createNewSong("efgh")

while(1):
    q = createArrayFromStructure("efgh")
    w = findUniqueMeasures(q)
    m = []
    v = []
    for measure in w:
        w[measure] = compileMeasure("efgh", measure);
        if(measure == "ia"):
            print(w[measure])
    for measure in q:
        z = w[measure];
        #v = concatMeasure(v, z)
        #m = concatMeasure(m, z)
        b = copy.deepcopy(z)
        if(measure == "ia" or measure == "ib"):
            print(b)
        b = optomizeMeasure(b, 20);
        v = concatMeasure(v, b)
    m = concatMeasure(m,v)
    
    saveNoteArrayToFile(m, "efgh")
    cmd = ["/home/pi/Desktop/AAHHgit/rpi_gpio_example", "efgh"]

    
    Popen(cmd, stdout = PIPE);
    input("play again?")
    
