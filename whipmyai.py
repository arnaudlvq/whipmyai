#!/usr/bin/env python3
"""
whipmyai — plays a whip crack every time you hit Enter in VS Code.
Shift+Enter is silently ignored.
"""

import os
import random
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_FILES = [
    os.path.join(DIR, "whip.mp3"),
    os.path.join(DIR, "whip2.mp3"),
    os.path.join(DIR, "whip3.mp3"),
]


# ── Active app detection ─────────────────────────────────────────────────────

def is_vscode_active():
    try:
        from AppKit import NSWorkspace  # pyobjc-framework-Cocoa
        app = NSWorkspace.sharedWorkspace().activeApplication()
        bundle = app.get("NSApplicationBundleIdentifier", "")
        name   = app.get("NSApplicationName", "")
        return (
            "com.microsoft.VSCode" in bundle
            or "VSCode" in name
            or "Visual Studio Code" in name
        )
    except Exception as exc:
        print(f"[whipmyai] AppKit error: {exc}", file=sys.stderr)
        return False


# ── Playback ──────────────────────────────────────────────────────────────────

def play_whip():
    subprocess.Popen(
        ["afplay", random.choice(SOUND_FILES)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


# ── Keyboard listener ─────────────────────────────────────────────────────────

def main():
    missing = [f for f in SOUND_FILES if not os.path.exists(f)]
    if missing:
        for f in missing:
            print(f"[whipmyai] ERROR: {f} not found.", file=sys.stderr)
        sys.exit(1)

    from pynput import keyboard

    MODIFIERS = {
        keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r,
        keyboard.Key.ctrl,  keyboard.Key.ctrl_l,  keyboard.Key.ctrl_r,
        keyboard.Key.alt,   keyboard.Key.alt_l,   keyboard.Key.alt_r,
        keyboard.Key.alt_gr,
        keyboard.Key.cmd,   keyboard.Key.cmd_l,   keyboard.Key.cmd_r,
    }

    pressed: set = set()

    def on_press(key):
        if key in MODIFIERS:
            pressed.add(key)
            return  # never play on a modifier keydown

        if key == keyboard.Key.enter:
            no_modifier_held = pressed.isdisjoint(MODIFIERS)
            if no_modifier_held and is_vscode_active():
                play_whip()

    def on_release(key):
        pressed.discard(key)

    print("[whipmyai] Listening… Enter in VS Code = CRACK  |  Shift+Enter = silence")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
