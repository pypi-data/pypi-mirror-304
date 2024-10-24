from dataclasses import dataclass, field
from ..SceneObject import SceneObject
from fractions import Fraction
from .Durable import Durable
from .Attributes import Attributes
from .AttributesChange import AttributesChange
from typing import List, Optional
from smashcima.nameof_via_dummy import nameof_via_dummy


@dataclass
class Event(SceneObject):
    """A collection of notes (and other symbols) with the same musical onset"""
    
    fractional_measure_onset: Fraction
    """How many quarter notes from the beginning of the measure this event occus"""

    durables: List[Durable] = field(default_factory=list)
    "Links to all durables with this onset time"

    attributes: Optional[Attributes] = None
    """State of attributes (clefs, keys, time) at this event. Should be null
    only during the parsing of a score. This value is populated when a part
    is parsed by calling Part.compute_event_attributes()"""

    attributes_change: Optional[AttributesChange] = None
    """Change of attributes when entering this event. If None, there is no
    change on this event."""

    @staticmethod
    def of_durable(
        durable: Durable,
        fail_if_none=False
    ) -> Optional["Event"] | "Event":
        return durable.get_inlinked(
            Event,
            nameof_via_dummy(Event, lambda e: e.durables),
            at_most_one=True,
            fail_if_none=fail_if_none
        )
