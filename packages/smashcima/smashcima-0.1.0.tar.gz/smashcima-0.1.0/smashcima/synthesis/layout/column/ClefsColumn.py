from smashcima.scene.semantic.Clef import Clef
from smashcima.scene.semantic.Score import Score
from smashcima.scene.visual.Stafflines import Stafflines
from smashcima.scene.visual.Glyph import Glyph
from smashcima.synthesis.glyph.SmuflGlyphClass import SmuflGlyphClass
from smashcima.synthesis.glyph.GlyphSynthesizer import GlyphSynthesizer
from .ColumnBase import ColumnBase
from typing import List, Set
import random


class ClefsColumn(ColumnBase):
    def __post_init__(self):
        self.clefs: List[Clef] = []

    def add_clef(self, clef: Clef, clef_glyph: Glyph):
        self.clefs.append(clef)
        self.add_glyph(clef_glyph)

    def _position_glyphs(self):
        for clef, clef_glyph in zip(self.clefs, self.glyphs):
            sl = self.get_stafflines_of_glyph(clef_glyph)

            pitch_position = Clef.clef_line_to_pitch_position(clef.line)

            clef_glyph.space.transform = sl.staff_coordinate_system.get_transform(
                pitch_position=pitch_position,
                time_position=self.time_position
            )


def synthesize_header_clefs(
    staves: List[Stafflines],
    rng: random.Random,
    glyph_synthesizer: GlyphSynthesizer,
    score: Score,
    measure_index: int
) -> ClefsColumn:
    column = ClefsColumn(staves, rng.random())

    # verification logic
    handled_staves: Set[int] = set()

    # go through all the parts
    for part in score.parts:
        measure = part.measures[measure_index]
        event = measure.first_event

        # and all the clefs in the part
        # (applying to the first event of the measure we are rendering)
        for staff_number, clef in event.attributes.clefs.items():

            # get the proper stafflines instance
            stafflines_index = score.first_staff_index_of_part(part) \
                + (staff_number - 1)
            stafflines = staves[stafflines_index]

            # determine the glyph class
            glyph_class: str = SmuflGlyphClass.clef_from_clef_sign(
                clef_sign=clef.sign,
                small=False
            ).value

            # synthesize the glyph
            glyph = glyph_synthesizer.synthesize_glyph(glyph_class)
            glyph.space.parent_space = stafflines.space
            column.add_clef(clef, glyph)

            # verification logic
            if stafflines_index in handled_staves:
                raise Exception(
                    f"The staff {stafflines_index} had a clef be created twice!"
                )
            handled_staves.add(stafflines_index)
    
    # verify there is one clef for each staff
    assert len(handled_staves) == len(staves), \
        "All staves must get a clef when synthesizing the header clefs."
    
    return column


def synthesize_change_clefs() -> ClefsColumn:
    # TODO: synthesize clef changes (small clefs)
    pass
