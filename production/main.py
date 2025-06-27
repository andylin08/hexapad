# hackpad_kmk.py – KMK firmware skeleton for your custom RP2040 keyboard
# 
# This file is meant to be copied to the CIRCUITPY drive of your Seeed Studio
# XIAO RP2040 (or other RP2040 board) once KMK is installed.
#
# ──────────────────────────────────────────────────────────────────────
# HOW TO USE
# 1. Install CircuitPython for the XIAO RP2040 and copy the KMK library
#    to the drive as per https://github.com/KMKfw/kmk_firmware/wiki/Install
# 2. Open this file in a text editor, fill in your actual row/column pin
#    lists (and encoder/RGB settings if used), then save it back to the
#    board. The keyboard should enumerate as a USB HID device.
#
# The schematic (hackpad.kicad_sch) did not contain explicit net names for
# the key matrix, so the pin lists below are PLACEHOLDERS. Consult your
# KiCad design to determine which MCU pins connect to the switch rows and
# columns, then replace the tuples accordingly (maintain their order).
# ──────────────────────────────────────────────────────────────────────

import board  # Pin definitions
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.modules.rgb import RGB

# ----------------------------------------------------------------------
# Keyboard object + hardware description
# ----------------------------------------------------------------------
keyboard = KMKKeyboard()

# TODO ✎✎✎  Replace these with the pins you actually wired.
# For XIAO‑RP2040 the usable GPIOs are D0–D9 plus A0/A1 (GP26/27).
# Order does not matter electrically, but must match the keymap layout.
keyboard.row_pins = (
    board.D0,
    board.D1,
    board.D2,
    board.D3,
)  # ← example: 4 rows

keyboard.col_pins = (
    board.D4,
    board.D5,
    board.D6,
    board.D7,
    board.D8,
)  # ← example: 5 columns

# If your diodes go from column ➜ row, keep COL2ROW; otherwise ROW2COL.
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# ----------------------------------------------------------------------
# Optional: RGB under‑glow / back‑light
# ----------------------------------------------------------------------
# The schematic shows an SK6812Mini RGB LED chain.  Replace the pin name
# and led_count with your actual data‑in pin and total LED count.
#
# If you don’t have LEDs, comment out this whole block.
try:
    rgb = RGB(
        pixel_pin=board.D9,     # DIN of first SK6812
        num_pixels=4,           # ← set to actual count
        hue_default=0,         # red on boot
        sat_default=255,
        val_default=50,        # moderate brightness (0‑255)
        val_limit=255,
        animation_speed=5,
    )
    keyboard.modules.append(rgb)
except ValueError:
    # If you picked a pin that isn’t available, the constructor raises.
    pass

# ----------------------------------------------------------------------
# Optional: Rotary encoder(s)
# ----------------------------------------------------------------------
# Example for one 3‑pin encoder (A, B, common). Comment out if unused.
# Replace with your pin names.
try:
    encoder_handler = EncoderHandler()
    encoder_handler.pins = ((board.A1, board.A0, None),)  # (A_pin, B_pin, button)
    encoder_handler.map = (
        (KC.VOLU, KC.VOLD, KC.MUTE),  # Layer 0: vol up, vol down, press = mute
    )
    keyboard.modules.append(encoder_handler)
except (AttributeError, ValueError):
    pass

# ----------------------------------------------------------------------
# Layers & keymap definition
# ----------------------------------------------------------------------
# Example 4×5 ortholinear layout (20 keys) with two layers.
layers = Layers()
keyboard.modules.append(layers)

keyboard.keymap = [
    # Layer 0 – alpha / base
    [
        KC.ESC,  KC.Q,    KC.W, KC.E,  KC.R,
        KC.A,    KC.S,    KC.D, KC.F,  KC.G,
        KC.Z,    KC.X,    KC.C, KC.V,  KC.B,
        KC.SPC,  KC.LCTL, KC.LALT, KC.LGUI, KC.ENT,
    ],

    # Layer 1 – symbols/function (hold LT or press MO to access)
    [
        KC.TILDE, KC.EXLM, KC.AT,   KC.HASH, KC.DLR,
        KC.PERC,  KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN,
        KC.RPRN,  KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR,
        KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
    ],
]

# ----------------------------------------------------------------------
# Combo keys, tap‑dance, or other advanced modules could be added here.
# ----------------------------------------------------------------------

if __name__ == '__main__':
    keyboard.go()

# End of hackpad_kmk.py
