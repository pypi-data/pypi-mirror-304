from dataclasses import dataclass, field
from ..SceneObject import SceneObject
from typing import List, Optional
from .Note import Note
from .Event import Event
from .StemValue import StemValue
from smashcima.nameof_via_dummy import nameof_via_dummy


@dataclass
class Chord(SceneObject):
    """Chord is a collection of notes that share one stem. Even a single note
    has a chord, since it needs to encode its stem information here. Musically
    a chord is a group of notes with the same onset and duration though.
    A whole note chord is also a chord, despite not having a stem - there the
    stem has value "none". (this is for consistency)"""
    
    notes: List[Note] = field(default_factory=list)
    "Links to all notes within this chord"

    stem_value: StemValue = StemValue.none
    "What orientation does the stem have. If none, infer when rendering."

    @staticmethod
    def of_note(
        note: Note,
        fail_if_none=False
    ) -> Optional["Chord"] | "Chord":
        return note.get_inlinked(
            Chord,
            nameof_via_dummy(Chord, lambda c: c.notes),
            at_most_one=True,
            fail_if_none=fail_if_none
        )
    
    def get_event(self) -> Event:
        """Returns the event that contains notes in this chord"""
        if len(self.notes) == 0:
            raise Exception("The chord is empty, there are no notes.")
        return Event.of_durable(self.notes[0], fail_if_none=True)
    
    def add_note(self, note: Note, stem_value: StemValue = None):
        """Adds a note into the chord with a stem value"""
        # store stem value if missing
        if self.stem_value == StemValue.none:
            self.stem_value = stem_value

        # validate stem value if present
        if self.stem_value != StemValue.none and stem_value != StemValue.none:
            assert self.stem_value == stem_value, \
                "All notes in a chord must have the same stem value"
        
        # validate that all the notes share the same event (have the same onset)
        if len(self.notes) > 0:
            event = Event.of_durable(self.notes[0], fail_if_none=True)
            inserted_event = Event.of_durable(note, fail_if_none=True)
            assert event is inserted_event, \
                "All notes in a chord must be in the same event (same onset)"
        
        # update the list of notes
        notes = [*self.notes, note]
        notes.sort(key=lambda n: n.pitch.get_linear_pitch()) # ascending by pitch
        self.notes = notes
