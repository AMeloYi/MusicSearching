import os
from music21 import *
from music21.exceptions21 import *

class FileOperator:
    '''Operators with files
    Functions:
        ReadFile: Read music file and return a stream of music21
        ReadFileXML: Read music file 'xml' and return a stream of music21
        ReadFileMEI: Read music file 'mei' and return a stream of music21
        SaveNoteList: Save the list of nodes into file
    '''

    def ReadFile(self, filename):
        '''Read music file and return a stream of music21

        This function can read the text file which representes the music and return
        a stream (type of music21). It will judge the format of the file and call
        ReadFileXML or ReadFileMEI according to the format.

        Args:
            filename: full path of the file in format 'xml', 'mxl' or 'mei'

        Returns:
            A stream of music21 (music21.stream) which contains all the musical
            elements in the file. If the file cannot be opened, the function will
            return None and print the error information in the console.
        '''
        # if the filepath exists
        if os.path.exists(filename):
            # get the file type
            fileType = os.path.splitext(filename)[1]
            if (fileType == '.xml') | (fileType == '.mxl'):
                return self.ReadFileXML(filename)
            elif fileType == '.mei':
                return self.ReadFileMEI(filename)
            else:
                print('Can not open file ' + filename)
                return None
        # if the filepath does not exist
        else:
            # try to verify that if the file is in corpus
            try:
                f = corpus.parse(filename)
            except CorpusException:
                f = None
                print('Can not open file ' + filename)
            return f


    def ReadFileXML(self, filename):
        '''Read music file 'xml' and return a stream of music21

        This function can read the text file in format 'xml' or 'mxl' which
        representes the music and return a stream (type of music21).

        Args:
            filename: full path of the file in format 'xml' or 'mxl'

        Returns:
            A stream of music21 (music21.stream) which contains all the musical
            elements in the file. If the file doesn't exist, the function will
            return None.
        '''
        if os.path.exists(filename):
            f = converter.parse(filename)
        else:
            f = None
        return f

    def ReadFileMEI(self, filename):
        '''Read music file 'mei' and return a stream of music21

        This function can read the text file in format 'mei' which representes
        the music and return a stream (type of music21).

        Args:
            filename: full path of the file in format 'mei'

        Returns:
            A stream of music21 (music21.stream) which contains all the musical
            elements in the file. If the file doesn't exist, the function will
            return None.
        '''
        if os.path.exists(filename):
            f = open(filename, 'r')
            meiString = f.read()
            f.close()
            outputStream = mei.MeiToM21Converter(meiString)
            return outputStream.run()
        else:
            return None

    def SaveNoteList(self, filename, list):
        '''Save the list of nodes into file

        This function can save the list of nodes into file. Each line representes
        a node. The information of each line is (voix,gamme,valeur,duree). Between
        two parameters exists a ',' and there is no space.

        Args:
            filename: full path of the file where user wants to save the notes
            list: a list of nodes (in format Node)

        Returns:
            There is no return in this function. The file will append the nodes
            everytime. If the file does not exist, it will create the file.
        '''
        f = open(filename, 'a')
        for note in list:
            string = str(note.voix) + ',' + str(note.gamme) + ',' + str(note.valeur) + ',' + str(note.duree)
            f.write(string + '\n')
        f.close()
