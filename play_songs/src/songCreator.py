import os
import time
import copy
from pinMeta import activePins;
from pinMeta import hardwareNumberTable;
from subprocess import Popen, PIPE
import pprint
from sys import argv
import logging as log
logger = log.getLogger(__name__)
if("-debug_song" in argv):
    logger.setLevel(log.DEBUG)
else:
    logger.setLevel(log.WARN)
    

basePath = "../../Songs/"
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
    #print("compiling " + songName + " measure " + measureName)
    measurePath = basePath + songName + "/" + measureName
    #print("measure path")
    #print(measurePath)
    measureString = open(basePath + songName + "/" + measureName)
    string = -1;
    noteArrayOutput = [];
    stringOffset = [0,5,10,15,20,25];
    for line in measureString:
        if(string == -1):
            #print(line)
            noteArrayOutput.append([int(line)]);
            noteArrayOutput[0].append(0);
        else:
            subindex = 0;
            for x in range(0,len(line)-1,2):
                tempNote = line[x] + line[x+1];
                #print(tempNote)
                if(string == 0):
                    if(tempNote != "||"):
                        noteArrayOutput.append([0]);
                        noteArrayOutput.append([0]);
                if(tempNote != "||" and tempNote != "--"):
                    #thebest
                    tempTempNote = int(tempNote);
                    tempTempNote = string + tempTempNote * 6;
                    #print("temp")
                    #print(tempTempNote)
                    #print(activePins[tempTempNote])
                    tempTempNote = hardwareNumberTable[activePins[tempTempNote]];
                    noteArrayOutput[subindex] = [tempTempNote] + noteArrayOutput[subindex];
                    noteArrayOutput[subindex + 1] = [tempTempNote] + noteArrayOutput[subindex + 1];
                    #print(noteArrayOutput)
                if(tempNote != "||"):
                    subindex += 2
        string += 1;
    return noteArrayOutput;

def optomizeMeasure(inputMeasure, optomize = 1):
    optomizeNotes = copy.deepcopy(inputMeasure[0]);
    outputMeasure = copy.deepcopy(inputMeasure);
    skip = True;
    for subArray in inputMeasure:
        if(skip):
            skip = False;
        else:
            for note in subArray:
                if(len(optomizeNotes) == optomize):
                    inputMeasure[0] = [note] + inputMeasure[0]
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
    print("saving to " + newFile)
    noteCount = 0;
    noteMax = 1 + timeSignature * 8;
    if(not os.path.exists(basePath + songName + "/compiledSections/" )):
        os.makedirs(basePath + songName + "/compiledSections/" );
    else:
        print("song created")
    x = open(newFile, "w+");
    for subArray in inputNoteArray:
        for note in subArray:
            if(note != 0):
                x.write(str(note) + " ")
            else:
                x.write("0" + "\n")

def saveNoteArrayToFileTwo(inputNoteArray, songName, sectionName = "temp", timeSignature = 4):
    newFile = basePath + songName + "/compiledSections/" + sectionName
    #lol
    maxNotes = 25;
    currentNotes = 0
    noteCount = 0;
    noteMax = 1 + timeSignature * 8;
    if(not os.path.exists(basePath + songName + "/compiledSections/" )):
        print("directory created")
        os.makedirs(basePath + songName + "/compiledSections/" );
    x = open(newFile, "w+");
    for subArray in inputNoteArray:
        for q in range (len(subArray), maxNotes):
            subArray.insert(-1, 60);
        for k in range(0,len(subArray)):
            if(subArray[k] < 0):
                subArray.insert(k + 1,60);
                print(subArray)
                print(len(subArray))
                
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

def optomizeDoubleNotes(inputNoteArray):
    return
def optomizeHardwareTiming(inputNoteArray):
  #pprint.pprint(inputNoteArray[0::40])
  inputNoteArray.insert(1,[0])
  everyOther = []
  for x in range(1, len(inputNoteArray)):
    currentSubArray = inputNoteArray[x]
    for note in range (len(currentSubArray)-1, -1, -1):
      #print(note)
      currentNote = currentSubArray[note]
      if currentNote > 0:
        if not currentNote in inputNoteArray[x-1]:
          if not currentNote in everyOther:
            inputNoteArray[x-1].insert(0, currentNote)
            currentSubArray.remove(currentNote)
            everyOther.append(currentNote)
            #print("measure " + str(x))
            #print("moving " + str(note))
          else:
            everyOther.remove(currentNote)
          
  return inputNoteArray

def optomizeHardwareTimingTwo(inputNoteArray):
  #pprint.pprint(inputNoteArray[0::40])
  inputNoteArray.insert(1,[0])
  everyOther = []
  for x in range(1, len(inputNoteArray)):
    currentSubArray = inputNoteArray[x]
    for note in range (len(currentSubArray)-1, -1, -1):
      #print(note)
      currentNote = currentSubArray[note]
      if currentNote > 0:
        if not currentNote in inputNoteArray[x-1]:
          if not currentNote in everyOther:
            #print(inputNoteArray[x-1])
            inputNoteArray[x-1].insert(0, currentNote);
            currentSubArray.remove(currentNote)
            everyOther.append(currentNote)
            #print("measure " + str(x))
            #print("moving " + str(currentNote))
          else:
            everyOther.remove(currentNote)
          
  return inputNoteArray


def singleFret(directory, fret):
    print("temporary folder");
    fileList = os.listdir(directory)
    for f in fileList:
        if(f != "songSequence" and 
           f!=".DS_store" and 
           f!= "compiledSections" and
	       f!= "clicks"):
            openFile = open(directory + "/" + f, "r")
            tempText = openFile.read()
            tempText = tempText.replace(fret, "zz")
            tempText = tempText.replace("00", "--")
            tempText = tempText.replace("01", "--")
            tempText = tempText.replace("02", "--")
            tempText = tempText.replace("03", "--")
            tempText = tempText.replace("zz", "00")
            openFile.close()
            print(directory + "/" + f )
            print(tempText)
            openFile = open(directory + "/" + f , "w+")
            openFile.write(tempText)
            openFile.close()

def singleFretAttemptTwo(fret):
    off = 0
    if(fret == "01"):
        off = 6
    elif(fret == "02"):
        off = 12
    elif(fret == "03"):
        off = 18

    activePinsTemp = copy.deepcopy(activePins)
    for m in range (0,6):
        activePins[m] = activePins[m+off]
    for m in range (0,6):
        activePins[m+off] = activePinsTemp[m]
    print("before:")
    print(activePinsTemp)
    print("after:")
    print(activePins)

def compileSong():
    debug = "-debug_song" in argv
    newSongName = argv[1]
    fullPath = basePath + newSongName
    if not os.path.exists(fullPath + "/"):
        print("creating song folder");
        createNewSong(newSongName)
    songName = newSongName #lol lazy
    hardwareInput = not "-dhw" in argv

    #split input is just not going to happen right now
    splitInput = False
    if(splitInput):
        splitInput = input("are you sure you want to permanently change " + songName + "?")
        if(splitInput[0] == "y"):
            splitInput = input("which fret?")
            if(len(splitInput) == 2):
                singleFretAttemptTwo(splitInput)

    songPath = fullPath + "/compiledSections/temp" 
    songAsMeasures = createArrayFromStructure(songName)
    #print "song as measures"
    #print(songAsMeasures)
    uniqueMeasures = findUniqueMeasures(songAsMeasures)
    #print(uniqueMeasures)
    songAsNoteArray = []
    for measure in uniqueMeasures:
        #print(uniqueMeasures[measure])
        uniqueMeasures[measure] = compileMeasure(songName, measure);
    for measure in songAsMeasures:
        z = uniqueMeasures[measure];
        b = copy.deepcopy(z)
        b = optomizeMeasure(b, 20);
        songAsNoteArray = concatMeasure(songAsNoteArray, b)
    #pprint.pprint(songAsNoteArray)
    if(hardwareInput):
        print("making hardware optimization")
        songAsNoteArray =  optomizeHardwareTimingTwo(songAsNoteArray)
        #songAsNoteArray =  optomizeHardwareTimingTwo(songAsNoteArray)
    #pprint.pprint(songAsNoteArray)     
    saveNoteArrayToFile(songAsNoteArray, songName)

compileSong()
    
    
