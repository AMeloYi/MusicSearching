from music21 import *
from music21.exceptions21 import *

from src.model import Note


class Translator:
    '''Operator of the translation of the notes
    Translate the note into a list(vector) of number.
    Functions:
        TranslateToNote:
        TranslateToNoteList:
    '''

    def TranslateToNote(self, n, voix):
        '''Translate a note into a list(vector) of number

        This function can Translate a note (format stream.note) into a note (format
        Node).

        Args:
            n: A node in the musc21.stream
            voix: The part in which exists the note

        Returns:
            A note in format Note.
        '''
        duration = n.duration.quarterLength
        # if the note is a rest
        if n.isRest:
            return Note.Note(voix, -1, -1, duration)
        # if the note has different pitches
        elif n.isChord:
            if n.pitches:
                return Note.Note(voix, n.octave, n.pitches[0].midi % 12, duration)
        # if the note is a normal note
        else:
            return Note.Note(voix, n.octave, n.pitch.midi % 12, duration)

    def TranslateToNoteList(self, inputList, voix):
        '''Translate a list of notes(in music21.stream) into a list of Notes(format
        Note)

        This function can Translate a list of notes (format stream.note) into a list
        of notes (format Node). It will use the function TranslateToNote to translate
        every note in stream and add them into the same list according to the order.

        Args:
            inputList: A list of nodes in the musc21.stream
            voix: The part in which exists the notes

        Returns:
            A list of notes in format music21.Note.
        '''
        noteList = []
        for n in inputList:
            note = self.TranslateToNote(n, voix)
            noteList.append(note)
        return noteList
