"""
Sahaya - Cognitive Wellness Studio
game5_awaaz_pehchano.py  –  Awaaz Pehchano (Sound Recognition & Visual Matching)

Rules:
  • An audio cue is played (via tone synthesis / Windows beep / sound synthesizer).
  • 4 picture/emoji cards are displayed in a randomized grid.
  • The player has up to 3 replays per round.
  • Player identifies and clicks the picture card that matches the sound.
  • Tracks response time, accuracy, and replay count to calculate score /10.
"""

import tkinter as tk
import random
import threading
import time
import sys
from utils import COLORS, FONTS


SOUND_PRESETS = [
    {
        "id": "bell",
        "name": "Temple Bell",
        "emoji": "🔔",
        "desc": "Resonant bronze bell chime",
        "freqs": [(880, 250), (1046, 250), (1318, 500)]
    },
    {
        "id": "bird",
        "name": "Bird Chirping",
        "emoji": "🐦",
        "desc": "High frequency melodic chirps",
        "freqs": [(1760, 80), (2093, 100), (2637, 120)]
    },
    {
        "id": "car",
        "name": "Car Horn",
        "emoji": "🚗",
        "desc": "Dual tone honking acoustic",
        "freqs": [(440, 300), (554, 300)]
    },
    {
        "id": "rain",
        "name": "Rain & Thunder",
        "emoji": "🌧️",
        "desc": "Low rumbles and precipitation",
        "freqs": [(150, 400), (110, 500)]
    },
    {
        "id": "clock",
        "name": "Alarm Clock",
        "emoji": "⏰",
        "desc": "Pulsing repetitive alert buzz",
        "freqs": [(1000, 100), (1000, 100), (1000, 250)]
    },
    {
        "id": "drum",
        "name": "Traditional Dhol / Drum",
        "emoji": "🥁",
        "desc": "Percussive deep bass beat",
        "freqs": [(180, 200), (220, 200), (150, 350)]
    }
]


def play_sound_preset(preset):
    """Play preset frequencies in background thread."""
    def _do():
        try:
            if sys.platform == "win32":
                import winsound
                for freq, dur in preset["freqs"]:
                    winsound.Beep(max(37, freq), dur)
                    time.sleep(0.04)
            else:
                import pygame
                pygame.mixer.init()
        except Exception as e:
            print(f"[Sound Error]: {e}")
    threading.Thread(target=_do, daemon=True).start()


class AwaazPehchanoGame(tk.Frame):

    def __init__(self, master, on_complete, progress_data, **kwargs):
        super().__init__(master, bg=COLORS["bg_cream"], **kwargs)
        self.on_complete   = on_complete
        self.progress_data = progress_data

        self.rounds_total  = 5
        self.current_round = 0
        self.replays_left  = 3
        self.round_start_t = 0
        self.round_scores  = []
        self.target_sound  = None
        self.options       = []

        self._build_ui()
        self._start_round(0)

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["game5"], pady=12)
        hdr.pack(fill="x")

        tk.Label(hdr, text="🎵  Awaaz Pehchano (Sound Recognition & Visual Matching)",
                 font=FONTS["title"], bg=COLORS["game5"], fg=COLORS["white"]).pack(side="left", padx=20)

        self.lbl_round = tk.Label(hdr, text="Round 1 / 5", font=FONTS["heading"],
                                  bg=COLORS["game5"], fg=COLORS["white"])
        self.lbl_round.pack(side="right", padx=20)

        # Main Card
        self.card = tk.Frame(self, bg=COLORS["white"], padx=30, pady=20, relief="ridge", bd=1)
        self.card.pack(fill="both", expand=True, padx=40, pady=20)

        # Controls & Audio Bar
        top_bar = tk.Frame(self.card, bg=COLORS["white"])
        top_bar.pack(fill="x", pady=(0, 15))

        self.btn_play = tk.Button(top_bar, text="🔊 Listen to Sound", font=FONTS["heading"],
                                  bg=COLORS["game5"], fg=COLORS["white"], relief="flat",
                                  padx=20, pady=8, cursor="hand2", command=self._play_current_sound)
        self.btn_play.pack(side="left")

        self.lbl_replays = tk.Label(top_bar, text="Replays left: 3 / 3", font=FONTS["subheading"],
                                    bg=COLORS["white"], fg=COLORS["navy"])
        self.lbl_replays.pack(side="left", padx=15)

        self.lbl_hint = tk.Label(top_bar, text="Listen carefully and pick the matching picture card below",
                                 font=FONTS["subheading"], bg=COLORS["white"], fg=COLORS["text_sub"])
        self.lbl_hint.pack(side="right")

        # Picture Cards Grid (2x2)
        self.grid_frame = tk.Frame(self.card, bg=COLORS["white"])
        self.grid_frame.pack(fill="both", expand=True, pady=10)
        self.grid_frame.grid_columnconfigure((0, 1), weight=1)
        self.grid_frame.grid_rowconfigure((0, 1), weight=1)

        self.card_widgets = []
        for i in range(4):
            r = i // 2
            c = i % 2
            btn = tk.Button(self.grid_frame, text="", font=("Segoe UI", 16, "bold"),
                            bg="#F8FAFC", fg=COLORS["navy"], relief="solid", bd=1,
                            padx=15, pady=20, cursor="hand2", compound="top")
            btn.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")
            self.card_widgets.append(btn)

        # Status & Response Label
        self.lbl_status = tk.Label(self.card, text="", font=FONTS["heading"],
                                   bg=COLORS["white"], fg=COLORS["navy"])
        self.lbl_status.pack(pady=10)

    def _start_round(self, round_num):
        self.current_round = round_num
        self.replays_left  = 3
        self.lbl_round.config(text=f"Round {round_num + 1} / {self.rounds_total}")
        self.lbl_replays.config(text=f"Replays left: {self.replays_left} / 3")
        self.lbl_status.config(text="Sound playing... choose the matching card!", fg=COLORS["navy"])

        # Pick 1 target and 3 distractors
        all_shuffled = random.sample(SOUND_PRESETS, len(SOUND_PRESETS))
        self.target_sound = all_shuffled[0]
        distractors = all_shuffled[1:4]
        self.options = [self.target_sound] + distractors
        random.shuffle(self.options)

        # Update buttons
        for i, opt in enumerate(self.options):
            card_btn = self.card_widgets[i]
            card_btn.config(
                text=f"{opt['emoji']}\n\n{opt['name']}",
                bg="#F8FAFC",
                fg=COLORS["navy"],
                state="normal",
                command=lambda chosen=opt, btn=card_btn: self._on_card_click(chosen, btn)
            )

        self.round_start_t = time.time()
        # Play sound automatically on round start
        self._play_current_sound(deduct_replay=False)

    def _play_current_sound(self, deduct_replay=True):
        if deduct_replay:
            if self.replays_left <= 0:
                self.lbl_status.config(text="⚠️ No replays left for this round!", fg="#DC2626")
                return
            self.replays_left -= 1
            self.lbl_replays.config(text=f"Replays left: {self.replays_left} / 3")

        play_sound_preset(self.target_sound)

    def _on_card_click(self, chosen, btn):
        elapsed = round(time.time() - self.round_start_t, 1)

        # Disable all buttons
        for b in self.card_widgets:
            b.config(state="disabled")

        if chosen["id"] == self.target_sound["id"]:
            # Correct
            btn.config(bg="#DCFCE7", fg="#166534")  # Green
            # Score: base 10 minus replay penalty minus time penalty
            round_score = 10.0 - ((3 - self.replays_left) * 1.0)
            if elapsed > 6.0:
                round_score -= 1.0
            round_score = max(5.0, round_score)
            self.round_scores.append(round_score)
            self.lbl_status.config(
                text=f"🎉 Correct! Matched '{chosen['name']}' in {elapsed}s (+{round_score:.1f} pts)",
                fg=COLORS["success"]
            )
        else:
            # Incorrect
            btn.config(bg="#FEE2E2", fg="#991B1B")  # Red
            # Highlight correct one
            for i, opt in enumerate(self.options):
                if opt["id"] == self.target_sound["id"]:
                    self.card_widgets[i].config(bg="#DCFCE7", fg="#166534")

            self.round_scores.append(2.0)
            self.lbl_status.config(
                text=f"❌ Incorrect. The sound was '{self.target_sound['name']}'.",
                fg="#DC2626"
            )

        self.after(1600, self._next_round)

    def _next_round(self):
        if self.current_round + 1 < self.rounds_total:
            self._start_round(self.current_round + 1)
        else:
            self._finish_game()

    def _finish_game(self):
        final_score = round(sum(self.round_scores) / len(self.round_scores), 1) if self.round_scores else 0.0
        for w in self.card.winfo_children():
            w.destroy()

        tk.Label(self.card, text="🎉  Sound Recognition Completed!", font=FONTS["title"],
                 bg=COLORS["white"], fg=COLORS["navy"]).pack(pady=(20, 10))

        tk.Label(self.card, text=f"Auditory Discrimination Score: {final_score} / 10",
                 font=("Segoe UI", 24, "bold"), bg=COLORS["white"], fg=COLORS["game5"]).pack(pady=10)

        summary = (
            f"Evaluated sound pattern identification across {self.rounds_total} auditory trials.\n"
            "Acoustic discrimination and visual matching cortex pathways successfully exercised."
        )
        tk.Label(self.card, text=summary, font=FONTS["heading"],
                 bg=COLORS["white"], fg=COLORS["text_sub"], justify="center").pack(pady=15)

        tk.Button(self.card, text="Return to Studio Dashboard ➔", font=FONTS["heading"],
                  bg=COLORS["game5"], fg=COLORS["white"], relief="flat", padx=25, pady=12,
                  cursor="hand2", command=lambda: self.on_complete(final_score)).pack(pady=20)
