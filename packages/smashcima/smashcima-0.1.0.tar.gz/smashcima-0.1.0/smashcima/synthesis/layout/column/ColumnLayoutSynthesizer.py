from smashcima.scene.visual.Stafflines import Stafflines
from smashcima.scene.semantic.Score import Score
from smashcima.scene.visual.System import System
from smashcima.scene.visual.Page import Page
from smashcima.synthesis.glyph.GlyphSynthesizer import GlyphSynthesizer
from ..BeamStemSynthesizer import BeamStemSynthesizer
from .Column import Column
from .ColumnBase import ColumnBase
from .BarlinesColumn import synthesize_barlines_column
from .ClefsColumn import synthesize_header_clefs
from .NotesColumn import NotesColumn, synthesize_notes_column
from typing import List, Optional, Dict
import random


class _SystemState:
    """Holds state while synthesizing a single system of music"""

    def __init__(self, minimal_column_spacing: float):
        self.minimal_column_spacing = minimal_column_spacing
        "Minimum spacing inserted in between columns"
        
        self.columns: List[Column] = []
        "List of columns in this system"

        self.total_width = 0
        "Total width of all the columns, if stacked most tightly"

        self.current_measure_index: Optional[int] = None
        "What measure are we currently in? None means no measure (header/footer)"

        self.measure_indices: List[int] = []
        "List of measures in the system, indicated by their score index"

        self.columns_per_measure: Dict[int, List[Column]] = {}
        "Columns attached to their measure by score measure index"
    
    def enter_measure(self, measure_index: int):
        assert measure_index not in self.measure_indices, \
            "You cannot enter a measure twice"
        self.current_measure_index = measure_index
        self.measure_indices.append(measure_index)
    
    def exit_measure(self):
        self.current_measure_index = None
    
    @property
    def measure_count(self) -> int:
        """How many measures are present in the system"""
        return len(self.measure_indices)
    
    def append_column(self, column: Column):
        column.position_glyphs()
        
        if len(self.columns) > 0:
            self.total_width += self.minimal_column_spacing

        self.total_width += column.width
        self.columns.append(column)

        if self.current_measure_index is not None:
            self.columns_per_measure.setdefault(self.current_measure_index, [])
            self.columns_per_measure[self.current_measure_index].append(column)
    
    def delete_measure(self, measure_index: int):
        assert measure_index in self.measure_indices
        assert measure_index in self.columns_per_measure

        columns = self.columns_per_measure[measure_index]
        del self.columns_per_measure[measure_index]
        self.measure_indices.remove(measure_index)

        for column in columns:
            self.total_width -= column.width + self.minimal_column_spacing
            self.columns.remove(column)
            column.detach()


def _place_columns_tightly(state: _SystemState, minimal_column_spacing: float):
    """Places columns from left to right with minimal spacing between them"""
    time_position = 0
    for column in state.columns:
        column.time_position = time_position + column.left_width
        column.position_glyphs()
        time_position += column.width + minimal_column_spacing


def _place_columns_flexbox(
    state: _SystemState,
    minimal_column_spacing: float,
    available_width: float
):
    """Places columns stretched out to fill the staff width, like CSS flexbox"""
    # can be negative when overflowing
    width_to_distribute = available_width - state.total_width
    if width_to_distribute >= 0:
        total_flex = sum(c.flex_grow for c in state.columns)
    else:
        total_flex = sum(c.flex_shrink for c in state.columns)
    width_unit = width_to_distribute / total_flex

    time_position = 0
    for column in state.columns:
        width_portion = width_unit * column.flex_grow
        time_position += width_portion / 2
        
        column.time_position = time_position + column.left_width
        column.position_glyphs()
        time_position += column.width + minimal_column_spacing
        
        time_position += width_portion / 2


# TODO: define a layout synthesizer interface and inherit
# IN -> semantic scene object graph
# OUT -> visual scene object graph
class ColumnLayoutSynthesizer:
    def __init__(
        self,
        glyph_synthesizer: GlyphSynthesizer,
        beam_stem_synthesizer: BeamStemSynthesizer,
        rng: random.Random
    ):
        self.glyph_synthesizer = glyph_synthesizer
        self.beam_stem_synthesizer = beam_stem_synthesizer
        self.rng = rng

        # The following values control the synthesizer.
        # The page-flowing options are set to respect explicit breaks
        # and ignore overflowing. This guarantees the same visual layout
        # as the one encoded in the input MusicXML.

        self.minimal_column_spacing = 1.2
        "Minimal spacing inserted between columns"

        self.stretch_out_columns = True
        "Whether to place columns tightly or to stretch them out to fill staff"

        self.place_debug_rectangles = False
        "Places column rectangles for debugging (to see the columns)"

        self.respect_line_and_page_breaks = True
        "If true, the layout respects the page formatting data of the score"

        self.disable_wrapping = True
        "When true, only linebreaks and page breaks control flow"

    def fill_page(
        self,
        page: Page,
        score: Score,
        start_on_measure: int
    ) -> List[System]:
        """Fills the page with music and returns the list of synthesized systems"""
        systems: List[System] = []
        
        # state
        remaining_staves = len(page.staves)
        completed_staves = 0
        current_measure = start_on_measure

        # synthesize systems until we have the space available
        while remaining_staves >= score.staff_count:

            # or until there are measures left to synthesize
            if current_measure >= score.measure_count:
                break

            # or until we hit a page break
            if self.respect_line_and_page_breaks \
                    and not current_measure == start_on_measure:
                if current_measure in score.new_page_measure_indices:
                    break

            # synthesize a single system
            system = self.synthesize_system(
                staves=page.staves[
                    completed_staves:
                    completed_staves+score.staff_count
                ],
                score=score,
                start_on_measure=current_measure
            )
            systems.append(system)

            # update state
            remaining_staves -= score.staff_count
            completed_staves += score.staff_count
            current_measure += system.measure_count
        
        return systems
    
    def synthesize_system(
        self,
        staves: List[Stafflines],
        score: Score,
        start_on_measure: int
    ) -> System:
        """Synthesizes a single system of music onto the provided staves"""
        assert start_on_measure < score.measure_count, \
            "There must be at least one measure left to be placed on the system"

        assert len(staves) == score.staff_count, \
            "Given staves do not match the required number of staves per system"

        # === phase 1: synthesizing columns ===

        state = _SystemState(
            minimal_column_spacing=self.minimal_column_spacing
        )
        available_width = min(sf.width for sf in staves)

        # synthesize header = start of the system signatures
        # TODO: extract this into a method
        state.append_column(
            synthesize_header_clefs(
                staves, self.rng, self.glyph_synthesizer,
                score, start_on_measure
            )
        )

        # synthesize measures...
        next_measure_index = start_on_measure
        while True:

            # until there is space left
            if not self.disable_wrapping:
                if state.total_width < available_width:
                    break

            # or until there are measures to synthesize
            if next_measure_index >= score.measure_count:
                break

            # or until we hit a line break
            if self.respect_line_and_page_breaks \
                    and not next_measure_index == start_on_measure:
                if next_measure_index in score.new_system_measure_indices \
                        or next_measure_index in score.new_page_measure_indices:
                    break

            state.enter_measure(next_measure_index)
            score_measure = score.get_score_measure(next_measure_index)
            next_measure_index += 1

            # TODO: extract this into a method, there's going to be a lot
            # of code here eventually (synthesize_measure)

            # construct a column for each event
            for score_event in score_measure.events:
                state.append_column(
                    synthesize_notes_column(
                        staves, self.rng, self.glyph_synthesizer,
                        score, score_event
                    )
                )
            
            # column for the barlines
            state.append_column(
                synthesize_barlines_column(
                    staves, self.rng, self.glyph_synthesizer
                )
            )

            state.exit_measure()

        # TODO: synthesize system footer (key and time changes)

        # remove measures from the end until we stop overflowing
        # (and we want at least one measure to reman no matter what)
        # (and only do that if we have wrapping enabled)
        if not self.disable_wrapping:
            while state.total_width >= available_width and state.measure_count > 1:
                state.delete_measure(state.measure_indices[-1])

        # === phase 2: placing columns ===

        # tight or flexbox stretch
        if self.stretch_out_columns:
            _place_columns_flexbox(
                state,
                self.minimal_column_spacing,
                available_width
            )
        else:
            _place_columns_tightly(state, self.minimal_column_spacing)

        # optionally place debugging boxes around columns
        if self.place_debug_rectangles:
            for column in state.columns:
                if isinstance(column, ColumnBase):
                    column.place_debug_boxes()

        # === phase 3: construct the system object ===

        # TODO: create layout bboxes and add them to the system

        system = System(
            first_measure_index=start_on_measure,
            measure_count=state.measure_count
        )

        # === phase 4: synthesizing beams and stems ===

        # TODO: get paper_space as an argument
        paper_space = staves[0].space.parent_space

        for i in range(system.measure_count):
            score_measure = score.get_score_measure(
                system.first_measure_index + i
            )
            self.beam_stem_synthesizer.synthesize_beams_and_stems_for_measure(
                paper_space,
                score_measure
            )

        return system
