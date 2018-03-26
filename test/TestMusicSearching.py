import os
import unittest
import music21
from src.operator import FileOperator
from src.operator import DistanceCalculator
from src.operator import Seperator
from src.operator import Translator
from src.model import Note


ABSPATH = os.path.abspath('.')

class TestFileOperator(unittest.TestCase):

    def test_ReadFile(self):
        print('Testing ReadFile() ... ')
        fo = FileOperator.FileOperator()
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
        fo = FileOperator.FileOperator()
        file1 = 'not_exist.xml'
        self.assertTrue((fo.ReadFileXML(file1)==None))
        file2 = ABSPATH + r'\data\JosquinResearchProject\Josquin\xml\Masses\Jos0301.xml'
        self.assertTrue((fo.ReadFileXML(file2)!=None))

    def test_ReadFileMEI(self):
        print('Testing ReadFileMEI() ... ')
        fo = FileOperator.FileOperator()
        file1 = ABSPATH + r'\data\CRIM\mei\not_exist.mei'
        self.assertTrue((fo.ReadFileXML(file1)==None))
        file2 = ABSPATH + r'\data\CRIM\mei\CRIM_Mass_0002_Gloria.mei'
        self.assertTrue((fo.ReadFileXML(file2)!=None))

    def test_SaveNoteList(self):
        print('Testing SaveNoteList() ... ')
        fo = FileOperator.FileOperator()
        note1 = Note.Note(1,2,3,4)
        note2 = Note.Note(4,3,2,1)
        noteList = [note1, note2]
        filename = ABSPATH + r'\tmpData\test\test.csv'
        fo.SaveNoteList(filename, noteList)
        self.assertTrue(os.path.exists(filename))
        lineList = []
        if(os.path.exists(filename)):
            f = open(filename, 'r')
            for line in f.readlines():
                lineList.append(line.strip('\n'))
            f.close()
            os.remove(filename)
            string1 = lineList[0].split(',')
            self.assertEqual(len(string1), 4)
            self.assertEqual(string1[0], '1')
            self.assertEqual(string1[1], '2')
            self.assertEqual(string1[2], '3')
            self.assertEqual(string1[3], '4')
            string2 = lineList[1].split(',')
            self.assertEqual(len(string2), 4)
            self.assertEqual(string2[0], '4')
            self.assertEqual(string2[1], '3')
            self.assertEqual(string2[2], '2')
            self.assertEqual(string2[3], '1')

class TestSeperator(unittest.TestCase):

    def test_SeperateByPart(self):
        print('Testing SeperateByPart() ... ')
        filename = r'D:\PROJECTS\PRD\PRD\data\JosquinResearchProject\Josquin\xml\Masses\Jos0301.xml'
        f = music21.converter.parse(filename)
        sp = Seperator.Seperator()
        length, parts = sp.SeperateByPart(f)
        # parts[0].show()
        self.assertEqual(length, 4)

    def test_SeperateByMeasure(self):
        print('Testing SeperateByMeasure() ... ')
        filename = r'D:\PROJECTS\PRD\PRD\data\JosquinResearchProject\Josquin\xml\Masses\Jos0301.xml'
        f = music21.converter.parse(filename)
        sp = Seperator.Seperator()
        stream = f.parts[0]
        length, measureList = sp.SeperateByMeasure(stream)
        self.assertEqual(length, 51)
        self.assertEqual(measureList[0][0].name, 'rest')
        self.assertEqual(measureList[1][3].name, 'D')
        self.assertEqual(measureList[7][3].name, 'F')

    def test_SeperateByNMeasure(self):
        print('Testing SeperateByNMeasure() ... ')
        filename = r'D:\PROJECTS\PRD\PRD\data\JosquinResearchProject\Josquin\xml\Masses\Jos0301.xml'
        f = music21.converter.parse(filename)
        sp = Seperator.Seperator()
        stream = f.parts[0]
        length, measureList = sp.SeperateByNMeasure(stream, 4)
        self.assertEqual(length, 48)
        self.assertEqual(measureList[0][0].name, 'rest')
        self.assertEqual(measureList[1][8].name, 'D')
        self.assertEqual(measureList[7][10].name, 'D')

    def test_SeperateByMorceau(self):
        print('Testing SeperateByMorceau() ... ')
        filename = r'D:\PROJECTS\PRD\PRD\data\JosquinResearchProject\Josquin\xml\Masses\Jos0301.xml'
        f = music21.converter.parse(filename)
        sp = Seperator.Seperator()
        morceau = sp.SeperateByMorceau(f, 2, [3,4,5,6])
        self.assertEqual(len(morceau), 21)
        self.assertEqual(morceau[0].name, 'C')
        self.assertEqual(morceau[3].name, 'D')
        self.assertEqual(morceau[10].name, 'C')

class TestTranslator(unittest.TestCase):
    def test_TranslateToNote(self):
        tl = Translator.Translator()
        note1 = music21.note.Note('C4')
        note2 = music21.note.Note('F5')
        n1 = tl.TranslateToNote(note1, 1)
        n2 = tl.TranslateToNote(note2, 1)
        self.assertEqual(n1.valeur, 0)
        self.assertEqual(n1.duree, 1.0)
        self.assertEqual(n1.gamme, 4)
        self.assertEqual(n2.valeur, 5)
        self.assertEqual(n2.gamme, 5)

    def test_TranslateToNoteList(self):
        tl = Translator.Translator()
        note1 = music21.note.Note('C4')
        note2 = music21.note.Note('F5')
        note3 = music21.note.Note('D#4')
        noteList = [note1, note2, note3]
        nList = tl.TranslateToNoteList(noteList, 1)
        self.assertEqual(nList[0].valeur, 0)
        self.assertEqual(nList[0].gamme, 4)
        self.assertEqual(nList[1].valeur, 5)
        self.assertEqual(nList[1].gamme, 5)
        self.assertEqual(nList[2].valeur, 3)
        self.assertEqual(nList[2].gamme, 4)

class TestDistanceCalculator(unittest.TestCase):
    def test_Distance(self):
        # TODO
        return 0

if __name__ == '__main__':
    unittest.main()
