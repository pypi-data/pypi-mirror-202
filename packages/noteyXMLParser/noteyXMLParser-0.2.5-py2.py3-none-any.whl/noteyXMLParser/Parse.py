

import xml.etree.ElementTree as ET
from .Objects import *
import json
from collections import deque
from .CreateDict import *
'''
    class to parse the xml file and then create the json file

'''
class XMLParser:
    def __init__(self, score_path, fileData = False) -> None:
        if fileData:
            self.root = ET.fromstring(score_path)
        else:
            self.tree = ET.parse(score_path)
            self.root = self.tree.getroot()
        self.final_string = ""
 
     
        self.fingerDict = createfingerDict()
        self.chroma_to_chord = createChromaToChord()

    def parse(self):
        playString = self.getNotes()
        beatBase, beat_type = self.getTimeSignature()
        beat_unit, bpm = self.getBPMCounter()
        return playString, beatBase, bpm

    def getTimeSignature(self):
        beats = None
        beat_type = None
        for value in self.root.iter("time"):
            beats = value.find('beats').text
            beat_type = value.find('beat-type').text

        if beats is None:
            beats = "no beats found"
        if beat_type is None:
            beat_type = "no beat type found"
        return [beats, beat_type]

    def getBPMCounter(self):
        beat_unit = None
        bpm = None
        for value in self.root.iter("metronome"):
            beat_unit = value.find('beat-unit').text
            bpm = value.find('per-minute').text

        if beat_unit is None:
            beat_unit = "no beat unit found"
        if bpm is None:
            bpm = "no bpm found"
        return beat_unit, bpm

    def getNotes(self):
        note_list = []
        chord_end = False
        chord_note_queue = deque()
        for neighbor in self.root.iter('note'):
            if (neighbor.find('chord') != None):
                for pitch in neighbor.iter('pitch'):
                    pitch = str(pitch.find('step').text) + "_" + str(int(pitch.find('octave').text)  -1 )
                    duration = int(neighbor.find('duration').text)
                    type = str(neighbor.find('type').text)
                    print(self.fingerDict[pitch])
                    chord_note_queue.append(PlayedNote(pitch, duration, NoteDuration[type], self.fingerDict[pitch]))
                chord_end = True
                
            elif(neighbor.find('chord') == None and chord_end == True):
                note_list.append(PlayedChord(chord_note_queue, self.chroma_to_chord))
                chord_end = False
                chord_note_queue = deque()

            else:
                for pitch in neighbor.iter('pitch'):
                    pitch = str(pitch.find('step').text) + "_" + str(int(pitch.find('octave').text) - 1)
                    duration = int(neighbor.find('duration').text)
                    type = str(neighbor.find('type').text)
                    note_list.append(PlayedNote(pitch,  duration, NoteDuration[type], self.fingerDict[pitch]))
        
        final_string = ""
        for i in note_list:
            final_string += i.createString()  + " "
        return final_string
