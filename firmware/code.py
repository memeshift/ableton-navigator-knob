"""Navigator Knob firmware for Raspberry Pi Pico (CircuitPython).

Sends the MIDI protocol documented in the project README over USB MIDI.
The modifier button is resolved here: Live only ever sees four messages.

Wiring (KY-040 module -> Pico):
    CLK -> GP2      DT  -> GP3      SW -> GP4
    +   -> 3V3      GND -> GND
Modifier button: one leg -> GP5, other leg -> GND
"""
import digitalio
import rotaryio
import usb_midi
import board
import keypad

CHANNEL = 0
CC_SCENE_SCROLL = 20
CC_TRACK_SCROLL = 21
NOTE_SCENE_FIRE = 60
NOTE_CLIP_FIRE = 61

midi_out = usb_midi.ports[1]

encoder = rotaryio.IncrementalEncoder(board.GP2, board.GP3, divisor=4)
last_position = encoder.position

# keypad handles debouncing; both buttons are active-low with internal pull-ups
buttons = keypad.Keys((board.GP4, board.GP5), value_when_pressed=False, pull=True)
KEY_CLICK = 0
KEY_MODIFIER = 1

modifier_held = False
active_note = None  # note currently held down, so release always matches press


def send_cc(cc, delta):
    # relative two's complement, one message per step
    value = 1 if delta > 0 else 127
    for _ in range(abs(delta)):
        midi_out.write(bytes([0xB0 | CHANNEL, cc, value]))


def send_note(note, on):
    status = 0x90 if on else 0x80
    midi_out.write(bytes([status | CHANNEL, note, 127 if on else 0]))


while True:
    position = encoder.position
    if position != last_position:
        delta = position - last_position
        last_position = position
        send_cc(CC_TRACK_SCROLL if modifier_held else CC_SCENE_SCROLL, delta)

    event = buttons.events.get()
    if event:
        if event.key_number == KEY_MODIFIER:
            modifier_held = event.pressed
        elif event.key_number == KEY_CLICK:
            if event.pressed:
                active_note = NOTE_CLIP_FIRE if modifier_held else NOTE_SCENE_FIRE
                send_note(active_note, True)
            elif active_note is not None:
                send_note(active_note, False)
                active_note = None
