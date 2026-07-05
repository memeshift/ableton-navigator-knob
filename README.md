# Ableton Navigator Knob

A one-knob hardware controller for Ableton Live's Session view: a detented
rotary encoder with push switch plus a modifier button.

| Action | Result in Live |
|---|---|
| Turn CW / CCW | Select next / previous scene |
| Click | Fire selected scene |
| Modifier + turn | Select track right / left |
| Modifier + click | Fire clip at selected track x scene |

## MIDI protocol

The firmware handles the modifier; Live only sees four messages (channel 1):

| Message | Meaning |
|---|---|
| CC 20, relative two's complement (1 = +1, 127 = -1) | Scene scroll |
| CC 21, relative two's complement | Track scroll |
| Note 60 on | Fire selected scene |
| Note 61 on | Fire selected clip |

## Layout

- `remote-script/AbletonNavigatorKnob/` — MIDI Remote Script, symlinked into
  `~/Music/Ableton/User Library/Remote Scripts/`
- `firmware/` — CircuitPython code for the Raspberry Pi Pico (pending hardware)
- `tools/` — virtual-MIDI test sender for developing without hardware

## Development loop

1. Edit the script in `remote-script/AbletonNavigatorKnob/`
2. In Live: Preferences > Link/Tempo/MIDI, toggle the AbletonNavigatorKnob
   control surface off and on to reload (or restart Live)
3. Logs: `~/Library/Preferences/Ableton/Live 12.4.2/Log.txt` (grep for "NavKnob")

Until the Pico arrives, MIDI input comes from the macOS IAC Driver bus via the
sender in `tools/`.
