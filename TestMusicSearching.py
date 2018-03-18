import unittest
import MusicSearching as ms
import os
from music21 import *


ABSPATH = os.path.abspath('.')

class TestFileOperator(unittest.TestCase):

    def test_ReadFile(self):
        print('Testing ReadFile() ... ')
        fo = ms.FileOperator()
        file1 = ABSPATH + r'\data\CRIM\mei\CRIM_Mass_0002_Gloria.mei'
        self.assertTrue((fo.ReadFile(file1)!=None))
        file2 = 'ddd'
        self.assertTrue((fo.ReadFile(file2)==None))
        file3 = 'bach/bwv65.2.xml'
        self.assertTrue((fo.ReadFile(file3)!=None))
        file4 = ABSPATH + r'\data\JosquinResearchProject\Josquin\xml\Masses\Jos0301.xml'
        self.assertTrue((fo.ReadFile(file4)!=None))


    def test_ReadFileXML(self):
        print('Testing ReadFileXML() ... ')
        fo = ms.FileOperator()
        file1 = 'not_exist.xml'
        self.assertTrue((fo.ReadFileXML(file1)==None))
        file2 = ABSPATH + r'\data\JosquinResearchProject\Josquin\xml\Masses\Jos0301.xml'
        self.assertTrue((fo.ReadFileXML(file2)!=None))

    def test_ReadFileMEI(self):
        print('Testing ReadFileMEI() ... ')
        fo = ms.FileOperator()
        file1 = ABSPATH + r'\data\CRIM\mei\not_exist.mei'
        self.assertTrue((fo.ReadFileXML(file1)==None))
        file2 = ABSPATH + r'\data\CRIM\mei\CRIM_Mass_0002_Gloria.mei'
        self.assertTrue((fo.ReadFileXML(file2)!=None))

    def test_SaveNoteList(self):
        print('Testing SaveNoteList() ... ')
        fo = ms.FileOperator()
        filename = ABSPATH + r'\tmp\tmp_test.csv'
        fo.SaveNoteList('test', ['a', 'b', 'c', 'd'])
        self.assertTrue(os.path.exists(filename))
        if(os.path.exists(filename)):
            f = open(filename, 'r')
            string = f.read()
            f.close()
            os.remove(filename)
            self.assertEqual(len(string), 5)
            self.assertEqual(string[0], 'a')
            self.assertEqual(string[1], 'b')
            self.assertEqual(string[2], 'c')
            self.assertEqual(string[3], 'd')


    def test_InitFiles(self):
        print('Testing InitFiles() ... ')
        fo = ms.FileOperator()
        file1 = ABSPATH + r'\tmp\tmp1.txt'
        file2 = ABSPATH + r'\tmp\tmp2.txt'
        file3 = ABSPATH + r'\tmp\tmp3.txt'
        f1 = open(file1, 'w')
        f1.close()
        f2 = open(file2, 'w')
        f2.close()
        f3 = open(file3, 'w')
        f3.close()
        fo.InitFiles()
        dirpath = ABSPATH + r'\tmp'
        self.assertEqual(len(os.listdir(dirpath)), 0)

class TestSeperator(unittest.TestCase):
    def test_SeperateByPart(self):
        # TODO
        return 0

    def test_SeperateByMeasure(self):
        # TODO
        return 0

    def test_SeperateByNMeasure(self):
        # TODO
        return 0

class TestTranslator(unittest.TestCase):
    def test_TranslateToNote(self):
        # TODO
        return 0

    def test_TranslateToNoteList(self):
        # TODO
        return 0

class TestDistanceCalculator(unittest.TestCase):
    def test_Distance_Note_Note(self):
        # TODO
        return 0

    def test_Distance_Note_Accord(self):
        # TODO
        return 0

    def test_Distance_Accord_Accord(self):
        # TODO
        return 0

    def test_Distance_Morceau_Morceau(self):
        # TODO
        return 0

if __name__ == '__main__':
    unittest.main()
