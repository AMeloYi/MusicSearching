from music21 import *
from music21.exceptions21 import *
import Note

# --------------------------------------------------------------------
# class Translator
# fonction:
#     - TranslateToNote
#     - TranslateToNoteList
# --------------------------------------------------------------------
class Translator:
    def TranslateToNote(self, n, voix):
        duration = n.duration.quarterLength
        if n.isRest:
            return Note.Note(voix, -1, -1, duration)
        elif n.isChord:
            if n.pitches:
                return Note.Note(voix, n.pitches[0].midi // 12, n.pitches[0].midi % 12, duration)
        else:
            return Note.Note(voix, n.pitch.midi // 12, n.pitch.midi % 12, duration)

    def TranslateToNoteList(self, inputList, voix):
        noteList = []
        for n in inputList:
            note = self.TranslateToNote(n, voix)
            noteList.append(note)
        return noteList
