from music21 import *
from music21.exceptions21 import *
import win32api
import os


ABSPATH = os.path.abspath('.')

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

    def SaveNoteList(self, id, list):
        string = ''
        for e in list:
            string += e
        filename = ABSPATH + r'\tmp\tmp_' + str(id) + '.csv'
        f = open(filename, 'a')
        f.write(string + '\n')
        f.close()

    def InitFiles(self):
        dirpath = ABSPATH + r'\tmp'
        for (root, dirs, files) in os.walk(dirpath):
            for file in files:
                filename = os.path.join(root, file)
                if os.path.exists(filename):
                    os.remove(filename)

class Seperator:
    def SeperateByPart(self):
        # TODO
        return 0

    def SeperateByMeasure(self):
        # TODO
        return 0

    def SeperateByNMeasure(self):
        # TODO
        return 0

class Translator:
    def TranslateToNote(self):
        # TODO
        return 0

    def TranslateToNoteList(self):
        # TODO
        return 0

class DistanceCalculator:
    def Distance_Note_Note(self, note1, note2):
        # TODO
        return 0

    def Distance_Note_Accord(self, note, accord):
        # TODO
        return 0

    def Distance_Accord_Accord(self, accord1, accord2):
        # TODO
        return 0

    def Distance_Morceau_Morceau(self, morceau1, morceau2):
        # TODO
        return 0

class Controller:
    def execute(self):
        fo = FileOperator()
        fileMei = ABSPATH + r'\data\CRIM\mei\CRIM_Mass_0002_Gloria0.mei'
        print(fo.ReadFileMEI(fileMei))
        return 0

if __name__ == '__main__':
    Controller().execute()
