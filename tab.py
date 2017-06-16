#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:19:06 2017

@author: dustinfranco
"""

standardTuning = [0,5,10,15,20,25]

def openSong(songName):
    f = open(songName, "r")
    tempSong = []
    offset = 5
    for line in f:
        
        if(tempSong == []):
            songLength = len(line)
            for x in range (0, songLength):
                tempSong.append([])
        for x in range(0,len(line)/2):
            tempString = line[2 * x] + line[2 * x + 1]
            if(tempString != "--"):
                try:
                    tempSong [x].append(int(tempString) + standardTuning[offset])
                except:
                    print ("invalid! " + tempString)
        offset -= 1
    return tempSong
    
def playSong(inputSong, BPM):
    for note in inputSong:
        playNote(note, BPM)