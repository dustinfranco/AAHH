import os
import time
import copy
import GPIOSetup
from pinMeta import activePins;
from pinMeta import hardwareNumberTable;
from subprocess import Popen, PIPE
import pprint

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
                    #print("temp")
                    #print(tempTempNote)
                    #print(activePins[tempTempNote])
                    tempTempNote = hardwareNumberTable[activePins[tempTempNote]];
                    noteArrayOutput[subindex] = [tempTempNote] + noteArrayOutput[subindex];
                    noteArrayOutput[subindex + 1] = [tempTempNote] + noteArrayOutput[subindex + 1];
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


def saveNoteArrayToFileTwo(inputNoteArray, songName, sectionName = "temp", timeSignature = 4):
    newFile = basePath + songName + "/compiledSections/" + sectionName
    #lol
    maxNotes = 25;
    currentNotes = 0
    noteCount = 0;
    noteMax = 1 + timeSignature * 8;
    if(not os.path.exists(basePath + songName + "/compiledSections/" )):
        print("creating that shit")
        os.makedirs(basePath + songName + "/compiledSections/" );
    else:
        print("shit created")
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


def mainLoop():
    userInput = input("(C)reate a new song (P)lay a song");
    if(userInput == "c" or userInput == "C"):
        newSongName = input("What would you like to name the song?");
        createNewSong(newSongName)
    elif (userInput == "p" or userInput == "P"):
        songName = input("Which song would you like to play?");
        secondInput = input("Would you like to recompile the song?")
        hardwareInput = input("Attempt hardware optimization?") 
        playAgain = "";
        while(playAgain == "y" or playAgain == "Y" or playAgain == ""):
            songPath = basePath + songName + "/compiledSections/temp" 
            if(secondInput == "y"):
                songAsMeasures = createArrayFromStructure(songName)
                uniqueMeasures = findUniqueMeasures(songAsMeasures)
                songAsNoteArray = []
                for measure in uniqueMeasures:
                    uniqueMeasures[measure] = compileMeasure(songName, measure);
                for measure in songAsMeasures:
                    z = uniqueMeasures[measure];
                    b = copy.deepcopy(z)
                    b = optomizeMeasure(b, 20);
                    songAsNoteArray = concatMeasure(songAsNoteArray, b)
                #pprint.pprint(songAsNoteArray)
                if(hardwareInput == "y" or hardwareInput == "Y"):
                    songAsNoteArray =  optomizeHardwareTimingTwo(songAsNoteArray)
                    #songAsNoteArray =  optomizeHardwareTimingTwo(songAsNoteArray)
                #pprint.pprint(songAsNoteArray)     
                saveNoteArrayToFile(songAsNoteArray, songName)
            cmd = ["/home/pi/Desktop/AAHH/dmx/src/play_song", songPath]
            print(cmd)
            print(songPath)
            #return
            #Popen(cmd, stdout = PIPE);
            playAgain = input("play again?")
    mainLoop();



mainLoop()
    
    
