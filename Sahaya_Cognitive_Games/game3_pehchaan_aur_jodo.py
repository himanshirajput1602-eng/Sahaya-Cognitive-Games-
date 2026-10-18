"""
Sahaya - Cognitive Wellness Studio
game3_pehchaan_aur_jodo.py  –  Pehchaan Aur Jodo (Visual Matching)

Rules:
  • Face-down cards are laid out in a grid. Player flips 2 at a time.
  • Matching pairs stay revealed; non-matches flip back.
  • 5 levels: 4 pairs → 6 → 8 → 10 → 12 pairs.
  • Score: 10 – (penalties) where penalty = 0.5 per extra flip beyond minimum.
"""

import tkinter as tk
import random
import time
from utils import COLORS, FONTS, ALL_EMOJI_POOLS


LEVELS = [
    {"pairs": 4,  "cols": 4, "label": "Level 1 – 4 pairs"},
    {"pairs": 6,  "cols": 4, "label": "Level 2 – 6 pairs"},
    {"pairs": 8,  "cols": 4, "label": "Level 3 – 8 pairs"},
    {"pairs": 10, "cols": 5, "label": "Level 4 – 10 pairs"},
    {"pairs": 12, "cols": 6, "label": "Level 5 – 12 pairs"},
]

FLIP_DELAY_MS = 900   # how long both non-matching cards stay visible


class PehchaanAurJodoGame(tk.Frame):

    def __init__(self, master, on_complete, progress_data, **kwargs):
        super().__init__(master, bg=COLORS["bg_cream"], **kwargs)
        self.on_complete    = on_complete
        self.progress_data  = progress_data

        self.current_level  = 0
        self.level_scores   = []

        # Per-level state
        self.cards          = []    # list of dicts {emoji, revealed, matched, btn}
        self.flipped         = []   # indices of currently face-up unmatched cards
        self.errors          = 0
        self.flips           = 0
        self.lock            = False  # prevent clicks during flip-back animation

        self._build_ui()
        self._start_level(0)

    # ─────────────────────  UI Building  ─────────────────────
    def _build_ui(self):
        hdr = tk.Frame(self, bg=COLORS["game3"], pady=12)
        hdr.pack(fill="x")

        tk.Label(hdr, text="🃏  Pehchaan Aur Jodo", font=FONTS["title"],
                 bg=COLORS["game3"], fg=COLORS["white"]).pack(side="left", padx=20)

        self.lbl_level = tk.Label(hdr, text="", font=FONTS["heading"],
                                  bg=COLORS["game3"], fg=COLORS["white"])
        self.lbl_level.pack(side="right", padx=20)

        # Stats bar
        stats = tk.Frame(self, bg=COLORS["bg_card"], pady=8)
        stats.pack(fill="x", padx=0)

        self.lbl_matches = tk.Label(stats, text="Matched: 0", font=FONTS["heading"],
                                    bg=COLORS["bg_card"], fg=COLORS["sage"])
        self.lbl_matches.pack(side="left", padx=30)

        self.lbl_errors = tk.Label(stats, text="Errors: 0", font=FONTS["heading"],
                                   bg=COLORS["bg_card"], fg=COLORS["accent"])
        self.lbl_errors.pack(side="left", padx=30)

        self.lbl_flips = tk.Label(stats, text="Flips: 0", font=FONTS["heading"],
                                  bg=COLORS["bg_card"], fg=COLORS["text_mid"])
        self.lbl_flips.pack(side="left", padx=30)

        self.lbl_instruction = tk.Label(self, text="",
                                        font=FONTS["body"],
                                        bg=COLORS["bg_cream"],
                                        fg=COLORS["text_mid"],
                                        wraplength=700)
        self.lbl_instruction.pack(pady=(10, 4))

        # Grid container (scrollable if needed)
        self.grid_outer = tk.Frame(self, bg=COLORS["bg_cream"])
        self.grid_outer.pack(fill="both", expand=True, padx=40, pady=4)

        self.grid_frame = tk.Frame(self.grid_outer, bg=COLORS["bg_cream"])
        self.grid_frame.pack(anchor="center")

        # Feedback
        self.feedback_frame = tk.Frame(self, bg=COLORS["bg_cream"])
        self.feedback_frame.pack(pady=6)

        self.lbl_feedback = tk.Label(self.feedback_frame, text="",
                                     font=FONTS["heading"],
                                     bg=COLORS["bg_cream"],
                                     fg=COLORS["text_dark"], wraplength=640)
        self.lbl_feedback.pack()

        self.btn_next = tk.Button(self.feedback_frame, text="Next Level →",
                                  font=FONTS["heading"],
                                  bg=COLORS["game3"], fg=COLORS["white"],
                                  relief="flat", bd=0, padx=24, pady=10,
                                  cursor="hand2", command=self._next_level)

    # ─────────────────────  Level Flow  ─────────────────────
    def _start_level(self, lvl_idx):
        self.current_level = lvl_idx
        cfg                = LEVELS[lvl_idx]
        self.flipped       = []
        self.errors        = 0
        self.flips         = 0
        self.lock          = False

        pairs = cfg["pairs"]

        pool_src = random.choice(ALL_EMOJI_POOLS)
        chosen   = random.sample(pool_src, min(pairs, len(pool_src)))
        deck     = chosen * 2
        random.shuffle(deck)

        self.cards = [
            {"emoji": em, "revealed": False, "matched": False, "btn": None}
            for em in deck
        ]

        self.lbl_level.config(text=cfg["label"])
        self.lbl_instruction.config(
            text=f"Find all {pairs} matching pairs! Click two cards at a time.")
        self.lbl_feedback.config(text="")
        self.btn_next.pack_forget()
        self._update_stats()
        self._render_grid(cfg["cols"])

    def _render_grid(self, cols):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        for i, card in enumerate(self.cards):
            btn = tk.Button(self.grid_frame,
                            text="🎴",
                            font=FONTS["emoji"],
                            bg=COLORS["bg_card"],
                            fg=COLORS["text_dark"],
                            relief="flat", bd=2,
                            padx=10, pady=10,
                            width=3,
                            cursor="hand2",
                            command=lambda i=i: self._on_flip(i))
            btn.grid(row=i // cols, column=i % cols, padx=5, pady=5)
            card["btn"] = btn

    def _update_stats(self):
        matched = sum(1 for c in self.cards if c["matched"]) // 2
        self.lbl_matches.config(text=f"Matched: {matched}")
        self.lbl_errors.config(text=f"Errors: {self.errors}")
        self.lbl_flips.config(text=f"Flips: {self.flips}")

    # ─────────────────────  Interaction  ─────────────────────
    def _on_flip(self, idx):
        if self.lock:
            return
        card = self.cards[idx]
        if card["matched"] or card["revealed"] or len(self.flipped) >= 2:
            return

        # Reveal card
        card["revealed"] = True
        card["btn"].config(text=card["emoji"],
                           bg=COLORS["accent_light"],
                           fg=COLORS["text_dark"])
        self.flips += 1
        self.flipped.append(idx)
        self._update_stats()

        if len(self.flipped) == 2:
            self._check_match()

    def _check_match(self):
        i1, i2 = self.flipped
        c1, c2 = self.cards[i1], self.cards[i2]

        if c1["emoji"] == c2["emoji"]:
            # Match!
            c1["matched"] = c2["matched"] = True
            c1["btn"].config(bg=COLORS["success"], fg=COLORS["white"])
            c2["btn"].config(bg=COLORS["success"], fg=COLORS["white"])
            self.flipped = []
            self._update_stats()
            self._check_win()
        else:
            # No match – flip back after delay
            self.errors += 1
            self.lock = True
            c1["btn"].config(bg=COLORS["error"], fg=COLORS["white"])
            c2["btn"].config(bg=COLORS["error"], fg=COLORS["white"])
            self.after(FLIP_DELAY_MS, self._flip_back, i1, i2)

    def _flip_back(self, i1, i2):
        for i in (i1, i2):
            c = self.cards[i]
            c["revealed"] = False
            c["btn"].config(text="🎴", bg=COLORS["bg_card"],
                            fg=COLORS["text_dark"])
        self.flipped = []
        self.lock    = False
        self._update_stats()

    def _check_win(self):
        if all(c["matched"] for c in self.cards):
            cfg    = LEVELS[self.current_level]
            pairs  = cfg["pairs"]
            min_flips = pairs * 2
            extra  = max(0, self.flips - min_flips)
            penalty = min(extra * 0.4, 10.0)
            frac   = max(0.0, (10.0 - penalty) / 10.0)
            self.level_scores.append(frac)

            stars = "⭐" * round(frac * 5)
            self.lbl_feedback.config(
                text=f"{stars}  All matched! {self.errors} errors, {self.flips} flips.",
                fg=COLORS["sage"] if self.errors < pairs else COLORS["accent_dark"])

            if self.current_level < len(LEVELS) - 1:
                self.btn_next.config(text="Next Level →", command=self._next_level)
            else:
                self.btn_next.config(text="🏁 See Results", command=self._finish)
            self.btn_next.pack(pady=8)

    def _next_level(self):
        self.btn_next.pack_forget()
        self._start_level(self.current_level + 1)

    def _finish(self):
        avg_frac    = sum(self.level_scores) / len(self.level_scores)
        final_score = round(avg_frac * 10, 1)
        self.on_complete(final_score)
