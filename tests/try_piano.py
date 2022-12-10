import script_include  # noqa F401

from motzart.harmony import ChordCategory, ChordProgressionGenerator
from motzart.piano import PianoChordArticulator
from motzart.player import Clip, Player
from motzart.primitives import Mode, Note, TimeSignature


def dummy_play_progession():
    # random.seed(100)

    generator = ChordProgressionGenerator(Note.C, Mode.lydian, lenght=6, octave=4)
    progression = generator.generate_v2(resolution_strenght=5, start_with=ChordCategory.TONIC)
    player = Player(bpm=120)

    clip = Clip()
    art = PianoChordArticulator(time_signature=TimeSignature(7, 4), intensity=4)
    for i in range(len(progression.chords)):
        chord = progression.chords[i]
        chord.extend_many(["7", "9"])
        clip.concat(art.articulate_arp_with_bass(chord, sloppyness=0))

    print(clip.starts_at, clip.ends_at)
    player.render(clip.played_notes)
    player.play()


dummy_play_progession()
