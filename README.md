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
- `firmware/` — CircuitPython code for the Raspberry Pi Pico
- `tools/` — virtual-MIDI test sender for developing without hardware

## Development loop

1. Edit the script in `remote-script/AbletonNavigatorKnob/`
2. In Live: Preferences > Link/Tempo/MIDI, toggle the AbletonNavigatorKnob
   control surface off and on to reload (or restart Live)
3. Logs: `~/Library/Preferences/Ableton/Live 12.4.2/Log.txt` (grep for "NavKnob")

Until the Pico arrives, MIDI input comes from the macOS IAC Driver bus via the
sender in `tools/`.

## Flashing the Pico

1. Download the CircuitPython UF2 for "Raspberry Pi Pico" from circuitpython.org
2. Hold the BOOTSEL button on the Pico while plugging in USB; it mounts as a
   drive named RPI-RP2
3. Drag the UF2 onto that drive; it reboots and remounts as CIRCUITPY
4. Copy `firmware/code.py` to the root of CIRCUITPY (it must be named code.py)
5. Wire per the comment at the top of `firmware/code.py`, then switch the
   Navigator input in Live's MIDI settings from IAC Driver to the Pico

No libraries needed on the board — the firmware uses only built-in modules.

## Hardware arrival day — full checklist

Current status (2026-07-06): remote script and virtual-knob sender are tested
and working against Live 12.4.2. Firmware is written but has never touched
real hardware. Parts ordered from Berrybase (Pico H, KY-040 encoder module,
breadboard, jumpers, buttons).

1. Flash CircuitPython on the Pico (section above, steps 1-3)
2. Copy `firmware/code.py` to the CIRCUITPY drive root
3. Wire on the breadboard:
   - KY-040: CLK -> GP2, DT -> GP3, SW -> GP4, + -> 3V3 (NOT 5V/VBUS), GND -> GND
   - Modifier button: one leg -> GP5, other leg -> GND
4. In Live: Settings > Link/Tempo/MIDI, set the Navigator control surface
   Input from "IAC Driver (Bus 1)" to the Pico's MIDI port
5. Test in order: turn (scene selection moves), click (scene fires),
   hold modifier + turn (track selection moves), hold modifier + click
   (selected clip fires)

### Likely first-run fixes

- **Scroll direction reversed** — swap the CLK and DT jumpers, or swap
  GP2/GP3 in the IncrementalEncoder line
- **Two/half steps per detent** — adjust `divisor=4` in code.py (try 2 or 1);
  KY-040 clones vary
- **Pico not showing in Live** — check the USB cable is data-capable; confirm
  CIRCUITPY mounts and code.py is at its root; errors from code.py appear if
  you connect to the serial console (e.g. `screen /dev/tty.usbmodem* 115200`)
- **Script edits don't take effect** — Live only re-imports remote script
  code at startup; toggling the control surface slot is NOT enough, fully
  quit and relaunch Live

### Repo/session facts worth knowing

- The script Live loads is a symlink: `~/Music/Ableton/User Library/Remote
  Scripts/Navigator` -> `remote-script/AbletonNavigatorKnob/` in this repo
- Script log lines: `grep NavKnob ~/Library/Preferences/Ableton/Live\
  12.4.2/Log.txt` (path tracks the installed Live version)
- Virtual testing without hardware: `.venv/bin/python tools/send.py cw 3`
  etc., with Navigator's input set to IAC Driver (Bus 1)
