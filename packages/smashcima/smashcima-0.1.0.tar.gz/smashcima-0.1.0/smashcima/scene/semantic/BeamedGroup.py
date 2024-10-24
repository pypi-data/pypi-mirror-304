from dataclasses import dataclass, field
from ..SceneObject import SceneObject
from typing import List, Optional, Dict, Tuple, Generator, Any
from .Note import Note
from .Chord import Chord
from .BeamValue import BeamValue
from smashcima.nameof_via_dummy import nameof_via_dummy


@dataclass
class BeamedGroup(SceneObject):
    """A group of notes that share at least one beam. Rests cannot be present
    in a beamed group, because rests lack stems and beam attaches to stems.
    Although a rest can be in the middle of a beamed group optically, it is not
    present here semantically."""
    
    chords: List[Chord] = field(default_factory=list)
    """Chords in this beamed group, in chronological order
    (chord is a group of notes that share a stem)"""

    beam_values: List[Dict[int, BeamValue]] = field(default_factory=list)
    """For each chord there is a dictionary, mapping beam numbers to beam values"""

    @staticmethod
    def of_chord(
        chord: Chord,
        fail_if_none=False
    ) -> Optional["BeamedGroup"] | "BeamedGroup":
        return chord.get_inlinked(
            BeamedGroup,
            nameof_via_dummy(BeamedGroup, lambda g: g.chords),
            at_most_one=True,
            fail_if_none=fail_if_none
        )

    def add_chord(self, chord: Chord, beam_values: Dict[int, BeamValue]):
        """Adds a new chord into the beamed group"""
        assert chord not in self.chords, \
            "Cannot add a chord twice into a beamed group."
        
        self.chords = [*self.chords, chord]
        self.beam_values.append(beam_values)
    
    @property
    def is_complete(self) -> bool:
        """Returns true if the beamed group has been terminated on the last chord."""
        if len(self.chords) == 0:
            return False
        return self.beam_values[-1].get(1, None) == BeamValue.end
    
    def iterate_beams(self) -> Generator[Tuple[int, List[Chord]], Any, Any]:
        """Return all beams to be drawn"""
        open_beams: Dict[int, List[Chord]] = dict()
        for chord, beam_values in zip(self.chords, self.beam_values):
            for beam_number, beam_value in beam_values.items():
                if beam_value == BeamValue.begin:
                    open_beams[beam_number] = [chord]
                elif beam_value == BeamValue.continue_beam:
                    open_beams[beam_number].append(chord)
                elif beam_value == BeamValue.end:
                    open_beams[beam_number].append(chord)
                    chords = open_beams[beam_number]
                    del open_beams[beam_number]
                    yield (beam_number, chords)
        assert len(open_beams) == 0
    
    def iterate_hooks(self) -> Generator[Tuple[int, Chord, BeamValue], Any, Any]:
        """Return all hooks to be drawn"""
        for chord, beam_values in zip(self.chords, self.beam_values):
            for beam_number, beam_value in beam_values.items():
                if beam_value in [BeamValue.forward_hook, BeamValue.backward_hook]:
                    yield (beam_number, chord, beam_value)
