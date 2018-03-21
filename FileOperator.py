import os
from music21 import *
from music21.exceptions21 import *

ABSPATH = os.path.abspath('.')

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
