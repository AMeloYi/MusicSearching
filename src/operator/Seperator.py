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
        '''Seperate the input stream by parts

        This function can seperate the music input stream into different
        parts.

        Args:
            inputStream: a music21.stream instance

        Returns:
            1. Nomber of the parts the music contains
            2. A list of music21.stream seperated by different parts
        '''
        list = []
        for i in range(len(inputStream.parts)):
            nStream = inputStream.parts[i]
            list.append(nStream)
        return len(inputStream.parts), list

    def SeperateByMeasure(self, inputStream):
        '''Seperate the input stream by measures

        This function can seperate the music input stream into different
        measures. The music input stream should be seperated into parts.

        Args:
            inputStream: a music21.stream instance contains only one part

        Returns:
            1. Nomber of the measures seperated
            2. A list who contains the lists of music21.Note seperated by 
            different measures
        '''
        nstream = inputStream.recurse().notesAndRests.stream()
        list = []
        for n in nstream:
            if (n.measureNumber >= len(list)):
                for i in range(len(list), n.measureNumber):
                    list.append([])
            list[n.measureNumber - 1].append(n)
        return len(list), list

    def SeperateByNMeasure(self, inputStream, N):
        '''Seperate the input stream by N measures

        This function can seperate the music input stream into several
        measures. The music input stream should be seperated into parts.

        Args:
            inputStream: a music21.stream instance contains only one part
            N: The number of measures user wants to seperate in a group

        Returns:
            1. Nomber of the measures seperated
            2. A list contains the lists of music21.Note seperated by 
            different N measures
        '''
        nstream = inputStream.recurse().notesAndRests.stream()
        lengthMeasure = 0
        list = []
        for n in nstream:
            if (n.measureNumber > lengthMeasure):
                lengthMeasure = n.measureNumber
        for i in range(lengthMeasure - N + 1):
            list.append([])
        for n in nstream:
            for i in range(N):
                index = n.measureNumber - i - 1
                if(index >= 0) & (index < len(list)):
                    list[index].append(n)
        return len(list), list

    def SeperateByMorceau(self, inputStream, voix, meausreList):
        '''Seperate the input stream by specified measures

        This function can seperate the music input stream into specified
        measures.

        Args:
            inputStream: a music21.stream instance contains all the music;
            voix: the part where exists the specified measures;
            measureList: the list of measure number user wants to seperate.
            It is recommended that the measures should be continuous.


        Returns:
            A list of music21.Note
        '''
        nbParts, parts = self.SeperateByPart(inputStream)
        nstream = parts[voix - 1].recurse().notesAndRests.stream()
        morceau = []
        print(meausreList)
        for n in nstream:
            if (n.measureNumber in meausreList):
                morceau.append(n)
        return morceau
