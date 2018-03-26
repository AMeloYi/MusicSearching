import os

from src.controller import Controller

if __name__ == '__main__':
    ctl = Controller.Controller()
    STOP = False
    # FileOperator.InitFiles()
    while(not STOP):
        print('-------- Choose the function --------')
        print('1.Create morceau ')
        print('2.Create whole morceau ')
        print('3.Preprocess the muisic file ')
        print('4.Calculate the distance between file and morceau ')
        print('5.Calculate the distances within one music ')
        print('6.Calculate the distances between two files ')
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
            ctl.PreprocessSpecifiedMusicFile(srcFile, voix, measureList, destFile)
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
            refFolder = input('Please input the ref folder : ')
            resFolder = input('Please input the res folder name : ')
            method = input('Please input the method : ')
            ctl.CalculateDistanceBetweenTwoFolders(targetFolder, refFolder, resFolder, method)
            print('Distance calculated!')
        elif command == '5':
            srcFile = input('Please input src file path : ')
            method = input('Please input the method : ')
            ctl.CalculateDistanceWithinFile(srcFile, method)
        elif command == '6':
            srcFile = input('Please input src file path : ')
            refFile = input('Please input ref file path : ')
            method = input('Please input the method : ')
            ctl.CalculateDistanceBetweenTwoFiles(srcFile, refFile, method)
        elif command == '7':
            resFolder = input('Please input result folder name : ')
            ctl.AnalyseResults(resFolder)
        elif command == '0':
            break
