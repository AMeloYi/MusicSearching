from music21 import *
from music21.exceptions21 import *
import os
import Controller

ABSPATH = os.path.abspath('.')

if __name__ == '__main__':
    ctl = Controller.Controller()
    STOP = False
    # FileOperator.InitFiles()
    while(not STOP):
        print('-------- Choose the function --------')
        print('1.Create morceau ')
        print('2.Create whole morceau ')
        print('3.Preprocess the muisic file')
        print('4.Calculate the distance between file and morceau')
        print('0.Exit')
        command = input('Please choose your fuction : ')
        print('you have choosed :', command)
        if command == '1':
            srcFile = input('Please input src file path : ')
            voix = int(input('Please input the voix : '))
            measureString = input('Please input measures(ex. 3,4,5) : ')
            mString = measureString.split(',')
            measureList = []
            for e in mString:
                measureList.append(int(e))
            destFile = input('Please input dest file name : ')
            ctl.SearchMorceau(srcFile, voix, measureList, destFile)
            print('Morceau created!')
        elif command == '2':
            srcFile = input('Please input src file path : ')
            destFile = input('Please input dest file name : ')
            ctl.PreprocessWholeMusicFile(srcFile, destFile)
            print('Whole Morceau created!')
        elif command == '3':
            srcFile = input('Please input src file path : ')
            destFolder = input('Please input the dest floder : ')
            N = int(input('Please input nb of measures you want to group up : '))
            ctl.PreprocessMusicFile(srcFile, destFolder, N)
            print('File analysed!')
        elif command == '4':
            targetFolder = input('Please input the target folder : ')
            targetFolderPath = ABSPATH + '\\tmp\\target\\'
            method = input('Please input the method : ')
        elif command == '0':
            break
