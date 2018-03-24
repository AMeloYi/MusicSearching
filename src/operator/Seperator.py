from music21 import *
from music21.exceptions21 import *

class Seperator:
    '''Seperate the music21.stream into different parts
    Translate the note into a list(vector) of number.
    Functions:
        SeperateByPart: Seperate the input stream by parts
        SeperateByMeasure: Seperate the input stream by mesures
        SeperateByNMeasure: Seperate the input stream by N mesures
        SeperateByMorceau: Seperate the input stream by specified position
    '''

    def SeperateByPart(self, inputStream):
        list = []
        for i in range(len(inputStream.parts)):
            nStream = inputStream.parts[i]
            list.append(nStream)
        return len(inputStream.parts), list

    def SeperateByMeasure(self, inputStream):
        nstream = inputStream.recurse().notesAndRests.stream()
        list = []
        for n in nstream:
            if (n.measureNumber >= len(list)):
                for i in range(len(list), n.measureNumber):
                    list.append([])
            list[n.measureNumber - 1].append(n)
        return len(list), list

    def SeperateByNMeasure(self, inputStream, N):
        nstream = inputStream.recurse().notesAndRests.stream()
        lengthMeasure = 0
        list = []
        for n in nstream:
            if (n.measureNumber + 1 > lengthMeasure):
                lengthMeasure = n.measureNumber + 1
        for i in range(lengthMeasure - N + 1):
            list.append([])
        for n in nstream:
            for i in range(N):
                index = n.measureNumber - i - 1
                if(index >= 0) & (index < len(list)):
                    list[index].append(n)
        return lengthMeasure, list

    def SeperateByMorceau(self, inputStream, voix, meausreList):
        nstream = inputStream.recurse().notesAndRests.stream()
        morceau = []
        print(meausreList)
        for n in nstream:
            if (n.measureNumber in meausreList):
                morceau.append(n)
        return morceau
