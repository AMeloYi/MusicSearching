import os
import shutil

import DistanceCalculator
import FileOperator
import Translator

from src.operator import Seperator

ABSPATH = os.path.abspath('.')

class Controller:
    '''Operators with files
    Attributes:
        fo: A FileOperator instance
        sp: A Seperator instance
        tl: A Translator instance
    Functions:
        PreprocessMusicFile:
        PreprocessWholeMusicFile:
        PreprocessSpecifiedMusicFile:
        CalculateDistance:
    '''

    def __init__(self):
        '''Constructor of the class Controller
        Init three instances: FileOperator, Seperator, Translator
        '''
        self.fo = FileOperator.FileOperator()
        self.sp = Seperator.Seperator()
        self.tl = Translator.Translator()
        self.dc = DistanceCalculator.DistanceCalculator()

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

    def PreprocessSpecifiedMusicFile(self, srcFile, voix, measureList, destFolder):
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

    def CalculateDistanceBetweenTwoFolders(self, targetFolder, refFolder, resFolder, method):
        targetFileList = []
        refFileList = []
        for (targetRoot,targetDirs,targetFiles) in os.walk(targetFolder):
            for targetFile in targetFiles:
                target = os.path.join(targetRoot, targetFile)
                targetFileList.append(target)
        for (refRoot,refDirs,refFiles) in os.walk(refFolder):
            for refFile in refFiles:
                ref = os.path.join(refRoot, refFile)
                refFileList.append(ref)
        for i in range(len(targetFileList)):
            for j in range(len(refFileList)):
                res = 'results\\' + str(i+1) + '_' + str(j+1)
                self.dc.Distance(targetFileList[i], refFileList[j], method, res)

    def CalculateDistanceWithinFile(self, srcFile, resFolder, method):
        # TODO:
        return None

    def CalculateDistanceBetweenTwoFiles(self, srcFile, refFile, resFolder, method):
        # TODO:
        return None

    def AnalyseResults(self, resFolder):
        # TODO:
        return None
