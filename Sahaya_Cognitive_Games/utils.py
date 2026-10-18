"""
Sahaya - Cognitive Wellness Studio
utils.py - Shared utilities, constants, theme, and data manager
"""

import json
import os
import time
import math
import random
from pathlib import Path

# ─────────────────────────────────────────
#  Theme & Design Tokens  (Wellness palette)
# ─────────────────────────────────────────
COLORS = {
    # Backgrounds
    "bg_cream":       "#F7F4ED",
    "bg_card":        "#FEFCF7",
    "bg_dark":        "#1C1917",
    "bg_hover":       "#F0EBE0",

    # Primary accent – terracotta
    "accent":         "#C25E3B",
    "accent_light":   "#E8A07A",
    "accent_dark":    "#943028",

    # Secondary – sage green
    "sage":           "#6B8F71",
    "sage_light":     "#A8C5AD",

    # Text
    "text_dark":      "#1C1917",
    "text_mid":       "#5C5550",
    "text_light":     "#A89F96",

    # Borders
    "border":         "#D8D0C1",
    "border_dark":    "#1C1917",

    # Game-specific accents
    "game1":          "#C25E3B",   # Yaad Rakho  – terracotta
    "game2":          "#6B8F71",   # Dhyan Ki Chaal – sage
    "game3":          "#8B6DB5",   # Pehchaan Aur Jodo – purple
    "game4":          "#C9873C",   # Kal Aaj Kal – amber
    "game5":          "#3B7EC2",   # Awaaz Pehchano – blue
    "game6":          "#C24B6B",   # Sahi Jagah – rose

    # Utility
    "white":          "#FFFFFF",
    "success":        "#4CAF50",
    "warning":        "#FF9800",
    "error":          "#F44336",
}

FONTS = {
    "display":  ("Georgia", 32, "bold"),
    "title":    ("Georgia", 22, "bold"),
    "subtitle": ("Georgia", 16, "italic"),
    "heading":  ("Segoe UI", 14, "bold"),
    "body":     ("Segoe UI", 12),
    "small":    ("Segoe UI", 10),
    "score":    ("Georgia", 28, "bold"),
    "emoji":    ("Segoe UI Emoji", 24),
    "emoji_sm": ("Segoe UI Emoji", 16),
}

# ─────────────────────────────────────────
#  Progress / Score Persistence
# ─────────────────────────────────────────
DATA_FILE = Path(__file__).parent / "sahaya_progress.json"

GAME_IDS = [
    "yaad_rakho",
    "dhyan_ki_chaal",
    "pehchaan_aur_jodo",
    "kal_aaj_kal",
    "awaaz_pehchano",
    "sahi_jagah",
]

DEFAULT_PROGRESS = {
    gid: {"best_score": 0.0, "levels_unlocked": 1, "play_count": 0, "last_score": 0.0}
    for gid in GAME_IDS
}


def load_progress() -> dict:
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            # ensure all keys exist
            for gid in GAME_IDS:
                if gid not in data:
                    data[gid] = DEFAULT_PROGRESS[gid].copy()
            return data
        except Exception:
            pass
    return {k: v.copy() for k, v in DEFAULT_PROGRESS.items()}


def save_progress(progress: dict):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(progress, f, indent=2)
    except Exception as e:
        print(f"[Sahaya] Could not save progress: {e}")


def update_score(progress: dict, game_id: str, score: float, levels_completed: int = 1):
    """Update best score and unlock next level."""
    rec = progress.get(game_id, DEFAULT_PROGRESS[game_id].copy())
    rec["last_score"] = round(score, 1)
    rec["best_score"] = round(max(rec["best_score"], score), 1)
    rec["play_count"] = rec.get("play_count", 0) + 1
    # unlock next level (max 5)
    if score >= 5.0:
        rec["levels_unlocked"] = min(5, rec.get("levels_unlocked", 1) + 1)
    progress[game_id] = rec
    save_progress(progress)


def overall_focus_score(progress: dict) -> float:
    scores = [progress[g]["best_score"] for g in GAME_IDS]
    return round(sum(scores) / len(scores), 1) if scores else 0.0


# ─────────────────────────────────────────
#  Emoji / Icon pools used by games
# ─────────────────────────────────────────
EMOJI_FRUITS  = ["🍎","🍊","🍋","🍇","🍓","🫐","🍒","🍑","🥭","🍌","🍉","🍈"]
EMOJI_ANIMALS = ["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐮"]
EMOJI_OBJECTS = ["⚽","🏀","🎸","🎺","🎻","🎹","🎲","🎯","🎳","🎮","🕹️","🃏"]
EMOJI_NATURE  = ["🌸","🌺","🌻","🌹","🌷","🌼","🍀","🌿","🌱","🍁","🌾","🌵"]
EMOJI_FOOD    = ["🍕","🍔","🌮","🍜","🍣","🍩","🎂","🍰","🧁","🍦","🍪","🥗"]
EMOJI_FACES   = ["😀","😁","😂","🤣","😊","😍","🤩","🥳","😎","🤓","🧐","😏"]

ALL_EMOJI_POOLS = [EMOJI_FRUITS, EMOJI_ANIMALS, EMOJI_OBJECTS, EMOJI_NATURE, EMOJI_FOOD]

# Category pools for Sahi Jagah
CATEGORY_DATA = {
    "🍽️ Kitchen": ["🍳","🥄","🔪","🫕","🥘","🍲","🥗","🫙","🧂","🥣","🍶","🫖"],
    "💼 Office":  ["📎","📏","✂️","📌","🖊️","📝","📋","💼","🖥️","⌨️","🖱️","📁"],
    "🌿 Garden":  ["🌱","🪴","🌻","🌷","🌸","🍀","🌿","🪸","🌾","🍁","🌲","🌳"],
    "🎮 Sports":  ["⚽","🏀","🏈","⚾","🥎","🎾","🏐","🏉","🥏","🏓","🏸","🥊"],
}

DAILY_ROUTINE_STEPS = [
    "Wake up",
    "Brush teeth",
    "Take a bath",
    "Get dressed",
    "Eat breakfast",
    "Go to work / school",
    "Have lunch",
    "Take a break",
    "Exercise / walk",
    "Eat dinner",
    "Read a book",
    "Sleep",
]

# Tone frequencies for Awaaz Pehchano (Hz)
SOUND_TONES = [261, 294, 330, 349, 392, 440, 494, 523]  # C4 to C5
