import os
import shutil
import FileOperator
import Seperator
import Translator
import DistanceCalculator
import FileOperator

ABSPATH = os.path.abspath('.')

# --------------------------------------------------------------------
# class Controller
# fonction:
#     - PreprocessMusicFile
#     - SearchMorceau
# --------------------------------------------------------------------
class Controller:
    def __init__(self):
        self.fo = FileOperator.FileOperator()
        self.sp = Seperator.Seperator()
        self.tl = Translator.Translator()

    def PreprocessMusicFile(self, srcFile, destFolder, N=1):
        dirpath = ABSPATH + '\\tmp\\target\\' + destFolder
        if(os.path.exists(dirpath)):
            shutil.rmtree(dirpath)
        os.makedirs(dirpath)
        stream = self.fo.ReadFile(srcFile)
        nbParts, parts = self.sp.SeperateByPart(stream)
        for i in range(nbParts):
            voix = i + 1
            startMeasure = 1
            nbFile = 1
            if (N == 1):
                length, nList = self.sp.SeperateByMeasure(parts[i])
            elif(N > 1):
                length, nList = self.sp.SeperateByNMeasure(parts[i], N)
            for list in nList:
                noteList = self.tl.TranslateToNoteList(list, voix)
                filename = dirpath + '\\target_' + str(voix) + '_' + str(startMeasure) + '_' + str(nbFile) + '.csv'
                startMeasure += 1
                nbFile += 1
                self.fo.SaveNoteList(filename, noteList)

    def PreprocessWholeMusicFile(self, srcFile, destFolder):
        dirpath = ABSPATH + '\\tmp\\fullref\\' + destFolder
        if(os.path.exists(dirpath)):
            shutil.rmtree(dirpath)
        os.makedirs(dirpath)
        stream = self.fo.ReadFile(srcFile)
        nbParts, parts = self.sp.SeperateByPart(stream)
        for i in range(nbParts):
            length, nList = self.sp.SeperateByMeasure(parts[i])
            for list in nList:
                noteList = self.tl.TranslateToNoteList(list, i+1)
                filename = dirpath + '\\ref.csv'
                self.fo.SaveNoteList(filename, noteList)

    def SearchMorceau(self, srcFile, voix, measureList, destFolder):
        dirpath = ABSPATH + '\\tmp\\ref\\' + destFolder
        if(os.path.exists(dirpath)):
            shutil.rmtree(dirpath)
        os.makedirs(dirpath)
        stream = self.fo.ReadFile(srcFile)
        nbParts, parts = self.sp.SeperateByPart(stream)
        noteList = self.sp.SeperateByMorceau(parts[voix-1], voix, measureList)
        print(noteList)
        morceau = self.tl.TranslateToNoteList(noteList, voix)
        filename = dirpath + '\\ref_' + str(voix) + '_' + str(measureList[0]) + '_' + str(len(measureList)) + '.csv'
        self.fo.SaveNoteList(filename, morceau)
