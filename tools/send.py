"""Simulate the Navigator Knob hardware by sending its MIDI protocol
into the IAC bus. Usage:

    send.py <action> [count]

Actions mirror the physical gestures:
    cw / ccw            turn the knob (scene scroll)
    click               press the knob (fire scene)
    mod-cw / mod-ccw    modifier held + turn (track scroll)
    mod-click           modifier held + press (fire clip)
"""
import sys
import time

import mido

PORT_NAME = "IAC Driver Bus 1"
CHANNEL = 0
CC_SCENE_SCROLL = 20
CC_TRACK_SCROLL = 21
NOTE_SCENE_FIRE = 60
NOTE_CLIP_FIRE = 61

CW = 1    # relative two's complement: +1
CCW = 127  # -1

ACTIONS = {
    "cw": ("cc", CC_SCENE_SCROLL, CW),
    "ccw": ("cc", CC_SCENE_SCROLL, CCW),
    "mod-cw": ("cc", CC_TRACK_SCROLL, CW),
    "mod-ccw": ("cc", CC_TRACK_SCROLL, CCW),
    "click": ("note", NOTE_SCENE_FIRE, None),
    "mod-click": ("note", NOTE_CLIP_FIRE, None),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ACTIONS:
        print(__doc__)
        sys.exit(1)
    kind, number, value = ACTIONS[sys.argv[1]]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    mido.set_backend("mido.backends.rtmidi")
    with mido.open_output(PORT_NAME) as port:
        for _ in range(count):
            if kind == "cc":
                port.send(mido.Message(
                    "control_change", channel=CHANNEL,
                    control=number, value=value))
            else:
                port.send(mido.Message(
                    "note_on", channel=CHANNEL, note=number, velocity=127))
                time.sleep(0.05)
                port.send(mido.Message(
                    "note_off", channel=CHANNEL, note=number, velocity=0))
            time.sleep(0.05)
    print(f"sent {sys.argv[1]} x{count}")


if __name__ == "__main__":
    main()
