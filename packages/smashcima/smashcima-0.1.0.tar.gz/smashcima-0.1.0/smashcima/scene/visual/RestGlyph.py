from dataclasses import dataclass
from ..semantic.Rest import Rest
from ..semantic.MeasureRest import MeasureRest
from ..semantic.TypeDuration import TypeDuration
from ..semantic.Pitch import Pitch
from ..semantic.Clef import Clef
from .Glyph import Glyph


# Display Pitch
# -------------
# MusicXML defines so-called display pitch for rests. By default, this value
# is missing and it's up to the rendering software to position the rest properly.
# When present, this position is overriden. The pitch depends on the active clef
# and for the percussion clef, the G2 treble is assumed.
#
# However there is little specification on how the display pitch translates
# to a position on the staff, especially for all the different glyphs of
# varous rest types.
#
# MuseScore assumes the default display pitch to be B4 (for the trebble clef,
# or rather, the pitch of the center staffline). This is the case even for
# the whole rest, which could be argued is either in the upper space (
# which is what the MXL user manual example suggests), or hangs from the
# line above that.
#
# For consistency, we decided to follow the MuseScore approach
# (because it treats all the rests the same way in the semantic domain)
# and we introduce pitch_position offsets. These offsets are a global constant
# that could be changed in case you want to interpret display pitches for
# rests differently. Alternatively, you can monkey patch the two static
# method that perform the conversion (default pitch and pitch to pitch position).
#
# Info from W3C:
# https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/display-step/
#
# Info from MXL:
# https://usermanuals.musicxml.com/MusicXML/Content/EL-MusicXML-rest.htm
# https://usermanuals.musicxml.com/MusicXML/Content/EL-MusicXML-display-step.htm


@dataclass
class RestGlyph(Glyph):
    """Glyph of a rest symbol"""

    rest: Rest | MeasureRest | None = None
    "The semantic rest that this glyph represents"

    @staticmethod
    def default_display_pitch(clef: Clef, type_duration: TypeDuration) -> Pitch:
        """Reurns the default pitch position for rests in the given clef"""
        # NOTE: type_duration is ignored, this is to that an advanced user
        # can monkey patch this method and have different defaults
        # for different rest types

        # as does MuseScore, we assume the center line
        # to be the default display pitch for rests
        return clef.pitch_position_to_pitch(pitch_position=0)

    @staticmethod
    def display_pitch_to_glyph_pitch_position(
        clef: Clef,
        display_pitch: Pitch,
        type_duration: TypeDuration
    ) -> int:
        """Converts a display pitch of a rest, in a clef, of rest type given
        by type duration, into the pitch position of the rest's glyph
        (where on the staff to put the glyph's origin vertically)"""
        pitch_position = clef.pitch_to_pitch_position(display_pitch)

        # whole note is the only exception, where its origin is rendered
        # one line above the center line
        if type_duration == TypeDuration.whole:
            return pitch_position + 2 # one line up
        
        return pitch_position
