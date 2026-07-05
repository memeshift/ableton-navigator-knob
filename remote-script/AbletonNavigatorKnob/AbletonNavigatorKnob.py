import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonElement import ButtonElement

CHANNEL = 0  # MIDI channel 1
CC_SCENE_SCROLL = 20
CC_TRACK_SCROLL = 21
NOTE_SCENE_FIRE = 60
NOTE_CLIP_FIRE = 61


class AbletonNavigatorKnob(ControlSurface):

    def __init__(self, c_instance):
        super().__init__(c_instance)
        with self.component_guard():
            self._scene_encoder = EncoderElement(
                MIDI_CC_TYPE, CHANNEL, CC_SCENE_SCROLL,
                Live.MidiMap.MapMode.relative_two_compliment)
            self._track_encoder = EncoderElement(
                MIDI_CC_TYPE, CHANNEL, CC_TRACK_SCROLL,
                Live.MidiMap.MapMode.relative_two_compliment)
            self._scene_button = ButtonElement(
                True, MIDI_NOTE_TYPE, CHANNEL, NOTE_SCENE_FIRE)
            self._clip_button = ButtonElement(
                True, MIDI_NOTE_TYPE, CHANNEL, NOTE_CLIP_FIRE)

            self._scene_encoder.add_value_listener(self._on_scene_scroll)
            self._track_encoder.add_value_listener(self._on_track_scroll)
            self._scene_button.add_value_listener(self._on_scene_fire)
            self._clip_button.add_value_listener(self._on_clip_fire)
        self.log_message("NavKnob: loaded")

    @staticmethod
    def _delta(value):
        # relative two's complement: 1..63 = clockwise, 65..127 = counter-clockwise
        return value - 128 if value >= 64 else value

    def _on_scene_scroll(self, value):
        self.log_message("NavKnob: scene scroll %d" % self._delta(value))

    def _on_track_scroll(self, value):
        self.log_message("NavKnob: track scroll %d" % self._delta(value))

    def _on_scene_fire(self, value):
        if value:
            self.log_message("NavKnob: scene fire")

    def _on_clip_fire(self, value):
        if value:
            self.log_message("NavKnob: clip fire")
