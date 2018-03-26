import os
import shutil

from src.operator import DistanceCalculator
from src.operator import FileOperator
from src.operator import Translator
from src.operator import Seperator

class Controller:
    '''Operators with files
    Attributes:
        fo: A FileOperator instance
        sp: A Seperator instance
        tl: A Translator instance
        dc: A DistanceCalculator instance
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

    def PreprocessMusicFile(self, srcFile, N=1):
        '''Preprocess of the music file by N measuress

        This function can seperate the music by N measures and save them into the
        destFolder.

        Args:
            srcFile: full path of the source file
            destFolder: folder name to save the results
            N: the number of measures user wants to seperate in a group

        Returns:
            This function has no return. All the results will be saved in a file in 
            the folder entered by user. If the folder does not exist, il will create 
            this folder automatically.
        '''
        destFolder = os.path.splitext(os.path.split(srcFile)[1])[0]
        dirpath = '..\\tmpData\\ref\\' + destFolder + '_' + str(N)
        if(os.path.exists(dirpath)):
            shutil.rmtree(dirpath)
        os.makedirs(dirpath)
        stream = self.fo.ReadFile(srcFile)
        nbParts, parts = self.sp.SeperateByPart(stream)
        nbFile = 1
        for i in range(nbParts):
            voix = i + 1
            startMeasure = 1
            if (N == 1):
                length, nList = self.sp.SeperateByMeasure(parts[i])
            elif(N > 1):
                length, nList = self.sp.SeperateByNMeasure(parts[i], N)
            for list in nList:
                noteList = self.tl.TranslateToNoteList(list, voix)
                filename = dirpath + '\\' + str(voix) + '_' + str(startMeasure) + '_' + str(nbFile) + '.csv'
                startMeasure += 1
                nbFile += 1
                if os.path.exists(filename):
                    os.remove(filename)
                self.fo.SaveNoteList(filename, noteList)

    def PreprocessWholeMusicFile(self, srcFile):
        '''Preprocess of the whole music file

        This function can translate the whole music by N measures and save them into the
        destFolder.

        Args:
            srcFile: full path of the source file
            destFolder: folder name to save the results

        Returns:
            This function has no return. The result will be saved in the folder entered by 
            user. If the folder does not exist, il will create this folder automatically. 
            This function only create one file.
        '''
        destFolder = os.path.splitext(os.path.split(srcFile)[1])[0]
        dirpath = '..\\tmpData\\ref\\' + destFolder + '_whole'
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


    def PreprocessSpecifiedMusicFile(self, srcFile, voix, measureList):
        '''Preprocess of the specified part of the music file

        This function can translate the specified music measures by inserting the specified 
        part and specified measures and save them into the destFolder. This function is used
        to translate the repeat measures found by users.

        Args:
            srcFile: full path of the source file
            voix: the specified part of the music
            measureList: the list of measure numbers
            destFolder: folder name to save the results

        Returns:
            This function has no return. The result will be saved in the folder entered by 
            user. If the folder does not exist, il will create this folder automatically. 
            This function only create one file.
        '''
        destFolder = os.path.splitext(os.path.split(srcFile)[1])[0]
        dirpath = '..\\tmpData\\ref\\' + destFolder + '_specified'
        if(not os.path.exists(dirpath)):
            os.makedirs(dirpath)
        stream = self.fo.ReadFile(srcFile)

        noteList = self.sp.SeperateByMorceau(stream, voix, measureList)
        morceau = self.tl.TranslateToNoteList(noteList, voix)
        filename = dirpath + '\\' + str(voix) + '_' + str(measureList[0]) + '_' + str(len(measureList)) + '.csv'
        if os.path.exists(filename):
            os.remove(filename)
        self.fo.SaveNoteList(filename, morceau)


    def CalculateDistanceBetweenTwoFolders(self, targetFolder, refFolder, method):
        '''Calculate distances between all the files in two folders

        This function can calculate all the distances between the files in target 
        folder and the files in reference folder.

        Args:
            srcFile: full path of the source file
            destFolder: folder name to save the results
            N: the number of measures user wants to seperate in a group

        Returns:
            This function has no return. All the results will be saved in a file in 
            the folder entered by user. If the folder does not exist, il will create 
            this folder automatically.
        '''
        resFolder = targetFolder + '_' + refFolder
        targetFolderPath = '..\\tmpData\\ref\\' + targetFolder
        refFolderPath = '..\\tmpData\\ref\\' + refFolder
        resFolderPath = '..\\results\\' + resFolder
        if not os.path.exists(resFolderPath):
            os.mkdir(resFolderPath)
        targetFileList = []
        refFileList = []
        for (targetRoot,targetDirs,targetFiles) in os.walk(targetFolderPath):
            for targetFile in targetFiles:
                target = os.path.join(targetRoot, targetFile)
                targetFileList.append(target)
        for (refRoot,refDirs,refFiles) in os.walk(refFolderPath):
            for refFile in refFiles:
                ref = os.path.join(refRoot, refFile)
                refFileList.append(ref)
        for i in range(len(targetFileList)):
            idTar = os.path.splitext(os.path.split(targetFileList[i])[1])[0]
            for j in range(len(refFileList)):
                idRef = os.path.splitext(os.path.split(refFileList[j])[1])[0]
                res = resFolderPath + '\\' + str(idTar) + '_' + str(idRef)
                if not os.path.exists(res):
                    os.mkdir(res)
                self.dc.Distance(targetFileList[i], refFileList[j], method, res)


    def CalculateDistanceWithinFile(self, srcFile, method):
        srcFileName = os.path.splitext(os.path.split(srcFile)[1])[0]
        self.PreprocessWholeMusicFile(srcFile)
        targetFolder = srcFileName + '_whole'
        self.CalculateDistanceBetweenTwoFolders(targetFolder, targetFolder, method)


    def CalculateDistanceBetweenTwoFiles(self, srcFile, refFile, method):
        tarFileName = os.path.splitext(os.path.split(srcFile)[1])[0]
        refFileName = os.path.splitext(os.path.split(refFile)[1])[0]
        self.PreprocessWholeMusicFile(srcFile)
        self.PreprocessWholeMusicFile(refFile)
        targetFolder = tarFileName + '_whole'
        refFolder = refFileName + '_whole'
        self.CalculateDistanceBetweenTwoFolders(targetFolder, refFolder, method)

    def AnalyseResults(self, resPath):
        # targetFile, refFile = resFolder.split('_')
        # resPath = '..\\results\\' + resFolder
        matrix_dis = []
        for (root,dirs,files) in os.walk(resPath):
            for file in files:
                filePath = os.path.join(root, file)
                filename = os.path.splitext(file)[0]
                idFile = int(filename)
                if(len(matrix_dis) < idFile):
                    for i in range(len(matrix_dis), idFile):
                        matrix_dis.append([])
                f = open(filePath, 'r')
                dis = []
                for line in f.readlines():
                    line = line.strip('\n')
                    split = line.split(' = ')
                    if split[0] == 'Distance':
                        dis.append(int(split[1]))
                matrix_dis[idFile - 1] = dis
        return matrix_dis
