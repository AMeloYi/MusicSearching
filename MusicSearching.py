from music21 import *
from music21.exceptions21 import *
import win32api
import os

ABSPATH = os.path.abspath('.')

class Note:
    def __init__(self, voix, gamme, valeur, duree):
        self.voix = voix
        self.gamme = gamme
        self.valeur = valeur
        self.duree = duree

class Accord:
    def __init__(self, notes):
        self.notes = []
        for note in notes:
            self.notes.append(note)

    def AddNote(note):
        self.notes.append(note)

class Morceau:
    def __init__(self, list):
        self.morceau = []
        for n in list:
            self.morceau.append(n)

    def AddElement(e):
        self.morceau.append(e)


# --------------------------------------------------------------------
# class fileOperator
# fonction:
#     - ReadFile
#     - ReadFileXML
#     - ReadFileMEI
#     - SaveNoteList
#     - InitFiles
# --------------------------------------------------------------------
class FileOperator:
    def ReadFile(self, filename):
        if os.path.exists(filename):
            fileType = filename[-4:]
            if (fileType == '.xml') | (fileType == '.mxl'):
                return self.ReadFileXML(filename)
            elif fileType == '.mei':
                return self.ReadFileMEI(filename)
            else:
                print('Can not open file ' + filename)
                return None
        else:
            try:
                f = corpus.parse(filename)
            except CorpusException:
                f = None
                print('Can not open file ' + filename)
            return f

    def ReadFileXML(self, filename):
        if os.path.exists(filename):
            f = converter.parse(filename)
        else:
            f = None
        return f

    def ReadFileMEI(self, filename):
        if os.path.exists(filename):
            f = open(filename, 'r')
            meiString = f.read()
            f.close()
            outputStream = mei.MeiToM21Converter(meiString)
            return outputStream.run()
        else:
            return None

    def SaveNoteList(self, filename, list):
        # filename = ABSPATH + r'\tmp\tmp_' + str(id) + '.csv'
        f = open(filename, 'a')
        for note in list:
            string = str(note.voix) + ',' + str(note.gamme) + ',' +  str(note.valeur) + ',' + str(note.duree)
            f.write(string + '\n')
        f.close()

    def InitFiles(self):
        dirpath = ABSPATH + r'\tmp\target'
        for (root, dirs, files) in os.walk(dirpath):
            for file in files:
                filename = os.path.join(root, file)
                if os.path.exists(filename):
                    os.remove(filename)

# --------------------------------------------------------------------
# class Seperator:
# fonction:
#     - SeperateByPart
#     - SeperateByMeasure
#     - SeperateByNMeasure
#     - SeperateByMorceau
# --------------------------------------------------------------------
class Seperator:
    def SeperateByPart(self, inputStream):
        list = []
        for i in range(len(inputStream.parts)):
            nStream = inputStream.parts[i]
            list.append(nStream)
        return len(inputStream.parts), list

    def SeperateByMeasure(self, inputStream):
        nstream = inputStream.recurse().notes.stream()
        list = []
        for n in nstream:
            if (n.measureNumber >= len(list)):
                for i in range(len(list), n.measureNumber + 1):
                    list.append([])
            list[n.measureNumber].append(n)
        return len(list), list

    def SeperateByNMeasure(self, inputStream, N):
        nstream = inputStream.recurse().notes.stream()
        lengthMeasure = 0
        list = []
        for n in nstream:
            print(n.measureNumber)
            if (n.measureNumber + 1 > lengthMeasure):
                lengthMeasure = n.measureNumber + 1
        for i in range(lengthMeasure - N + 1):
            list.append([])
        for n in nstream:
            for i in range(N):
                index = n.measureNumber - i
                if(index >= 0) & (index < len(list)):
                    list[index].append(n)
        return lengthMeasure, list

    def SeperateByMorceau(self, inputStream, voix, meausreList):
        length = len(meausreList)
        startMeasure = meausreList[0]
        lengthPart, parts = self.SeperateByPart(inputStream)
        nstream = parts[voix-1].recurse().notes.stream()
        morceau = []
        for n in nstream:
            if (n.measureNumber in meausreList):
                morceau.append(n)
        return morceau

# --------------------------------------------------------------------
# class Translator
# fonction:
#     - TranslateToNote
#     - TranslateToNoteList
# --------------------------------------------------------------------
class Translator:
    def TranslateToNote(self, n, voix):
        if n.isRest:
            return Note(voix, -1, -1, 0)
        elif n.isChord:
            if n.pitches:
                return chr(n.pitches[0].midi)
            else:
                return chr(127)
        else:
            return Note(voix, n.pitch.midi // 12, n.pitch.midi % 12, 0)

    def TranslateToNoteList(self, inputList, voix):
        noteList = []
        for n in inputList:
            note = self.TranslateToNote(n, voix)
            noteList.append(note)
        return noteList

# --------------------------------------------------------------------
# class DistanceCalculator
# fonction:
#     - Distance
# --------------------------------------------------------------------
class DistanceCalculator:
    def Distance(self, target, ref, method):
        param = '-sequences ' + target + ' ' + ref + ' -method ' + method + ' -result results -type character -parser csv'
        win32api.ShellExecute(0, 'open', 'MatchingToolBox.exe', param, '', 0)

# --------------------------------------------------------------------
# class Controller
# fonction:
#     - PreprocessMusicFile
#     - SearchMorceau
# --------------------------------------------------------------------
class Controller:
    def PreprocessMusicFile(self, srcFile, destFolder, N=1):
        # mode :
        #   - 1. seperateByMeasure
        #   - 2. seperateByNMeasure
        fo = FileOperator()
        sp = Seperator()
        tl = Translator()
        stream = fo.ReadFile(srcFile)
        nbParts, parts = sp.SeperateByPart(stream)
        for i in range(nbParts):
            voix = i + 1
            startMeasure = 1
            nbFile = 1
            if (N == 1):
                length, nList = sp.SeperateByMeasure(parts[i])
            elif(N > 1):
                length, nList = sp.SeperateByNMeasure(parts[i], N)
            for list in nList:
                noteList = tl.TranslateToNoteList(list, voix)
                filename = ABSPATH + '\\tmp\\target\\' + 'target_' + str(voix) + '_' + str(startMeasure) + '_' + str(nbFile) + '.csv'
                startMeasure += 1
                nbFile += 1
                fo.SaveNoteList(filename, noteList)

    def SearchMorceau(self, srcFile, voix, measureList, distFile):
        fo = FileOperator()
        sp = Seperator()
        tl = Translator()
        stream = fo.ReadFile(srcFile)
        noteList = sp.SeperateByMorceau(stream, voix, measureList)
        morceau = tl.TranslateToNoteList(noteList, voix)
        filename = ABSPATH + r'\tmp\ref\ref_' + distFile + '.csv'
        fo.SaveNoteList(filename, morceau)


if __name__ == '__main__':
    ctl = Controller()
    STOP = False
    FileOperator().InitFiles()
    while(not STOP):
        print('-------- Choose the function --------')
        print('1.Create morceau')
        print('2.Preprocess the muisic file')
        print('3.Calculate the distance between file and morceau')
        print('0.Exit')
        command = input('Please choose your fuction : ')
        print('you have choosed :', command)
        if command == '1':
            srcFile = input('Please input src file path : ')
            voix = int(input('Please input the voix : '))
            measureString = input('Please input measures(ex. 3,4,5) : ')
            measureList = measureString.split(',')
            for e in measureList:
                e = int(e)
            destFile = input('Please input desi file name : ')
            ctl.SearchMorceau(srcFile, voix, measureList, destFile)
            print('Morceau created!')
        elif command == '2':
            srcFile = input('Please input src file path : ')
            destFolder = input('Please input the dest floder : ')
            N = int(input('Please input nb of measures you want to group up : '))
            ctl.PreprocessMusicFile(srcFile, destFloder, N)
            print('File analysed!')
        elif command == '3':
            targetFolder = input('Please input the target folder : ')
            targetFolderPath = ABSPATH + '\\tmp\\target\\'
            method = input('Please input the method : ')
        elif command == '0':
            break
