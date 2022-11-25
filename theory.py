
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

MAJOR_SCALE_INTERVALS = [2,2,1,2,2,2,1]


class Mode(Enum):
    ionian = 0
    dorian = 1
    phrygian = 2
    lydian = 3
    mixolydian = 4
    aeolian = 5
    locarian  = 6


    def get_scale(self,root: MidiNote) -> Scale:
        offset = self.value
        notes = [root]
        _last_note = root

        for i in range(7):
            interval = MAJOR_SCALE_INTERVALS[(i+offset) % 7]
            _last_note = _last_note.next_by_interval(interval)
            notes.append(_last_note)

        return Scale(notes,self)

class Note(Enum):
    # value is base midi note value
    C = 0
    C_sharp = 1
    D = 2 
    D_sharp = 3
    E = 4
    F = 5
    F_sharp = 6 
    G = 7
    G_sharp = 8
    A = 9
    A_sharp = 10 
    B = 11

    def get_midi(self, octave: int):
        return MidiNote(note=self,octave=octave)

@dataclass
class MidiNote:
    note : Note
    octave: int = 0

    @property
    def midi(self) -> int:
        return self.note.value + (12*self.octave)

    def next_by_interval(self, interval :int):
        next_note = Note((self.note.value+interval )%12)
        next_note_octave = self.octave + ((self.note.value+interval )//12)

        return MidiNote(next_note,next_note_octave)

    def duplicate(self) -> MidiNote:
        return MidiNote(self.note,self.octave)

@dataclass
class Scale:
    notes : list[MidiNote]
    mode: Mode


    def get_note_by_distance(self,start: int, distance: int) -> MidiNote:
        position = start + distance

        note = self.notes[position%7]
        if position // 7 > 0:
            note = note.duplicate()
            note.octave += position // 7

        return note


    def get_diatonic_chord(self,degree: int):
        notes = [
            self.get_note_by_distance(degree,0),
            self.get_note_by_distance(degree,2),
            self.get_note_by_distance(degree,4),
            self.get_note_by_distance(degree,6),
        ]
        return Chord(degree,notes,self)

@dataclass
class Chord:
    degree : int
    notes : list[MidiNote]
    scale : Scale


if __name__ == "__main__":
    pass
