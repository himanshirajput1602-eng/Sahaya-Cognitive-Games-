"""
Sahaya - Cognitive Wellness Studio
game1_yaad_rakho.py  –  Yaad Rakho (Memory & Recall)

Rules:
  • A sequence of emoji icons is shown for a few seconds.
  • Icons disappear. Player must reconstruct the EXACT sequence
    by clicking icons in the correct order from a shuffled pool.
  • 5 levels: seq length 3 → 5 → 7 → 9 → 11
  • Score /10 based on (correct_positions / total_positions) across levels.
"""

import tkinter as tk
import random
import time
from utils import COLORS, FONTS, ALL_EMOJI_POOLS, EMOJI_ANIMALS, EMOJI_FRUITS, EMOJI_OBJECTS


# ──────────────────────────────────────────────────────────
#  Level configuration
# ──────────────────────────────────────────────────────────
LEVELS = [
    {"seq_len": 3, "show_time": 3.0, "extra_distractors": 3,  "label": "Level 1 – Warm Up"},
    {"seq_len": 5, "show_time": 4.0, "extra_distractors": 4,  "label": "Level 2 – Focus"},
    {"seq_len": 7, "show_time": 5.0, "extra_distractors": 5,  "label": "Level 3 – Challenge"},
    {"seq_len": 9, "show_time": 6.0, "extra_distractors": 6,  "label": "Level 4 – Expert"},
    {"seq_len": 11,"show_time": 7.0, "extra_distractors": 7,  "label": "Level 5 – Master"},
]


class YaadRakhoGame(tk.Frame):
    """
    Self-contained Frame for Yaad Rakho.
    Call with master=parent, on_complete=callback(score:float).
    """

    def __init__(self, master, on_complete, progress_data, **kwargs):
        super().__init__(master, bg=COLORS["bg_cream"], **kwargs)
        self.on_complete = on_complete
        self.progress_data = progress_data

        # state
        self.current_level   = 0
        self.level_scores    = []          # fraction correct per level
        self.sequence        = []          # the answer sequence (emojis)
        self.player_sequence = []          # what user has clicked so far
        self.phase           = "idle"      # idle | show | recall | result
        self.pool            = []          # shuffled pool shown to player
        self.btn_pool        = []          # Button widgets for pool
        self._countdown_id   = None

        self._build_ui()
        self._start_level(0)

    # ─────────────────────  UI Building  ─────────────────────
    def _build_ui(self):
        # Header row
        hdr = tk.Frame(self, bg=COLORS["game1"], pady=12)
        hdr.pack(fill="x")

        tk.Label(hdr, text="🧠  Yaad Rakho", font=FONTS["title"],
                 bg=COLORS["game1"], fg=COLORS["white"]).pack(side="left", padx=20)

        self.lbl_level = tk.Label(hdr, text="", font=FONTS["heading"],
                                  bg=COLORS["game1"], fg=COLORS["white"])
        self.lbl_level.pack(side="right", padx=20)

        # Instruction bar
        self.lbl_instruction = tk.Label(self, text="", font=FONTS["body"],
                                        bg=COLORS["bg_cream"], fg=COLORS["text_mid"],
                                        wraplength=640, justify="center")
        self.lbl_instruction.pack(pady=(12, 4))

        # Timer label
        self.lbl_timer = tk.Label(self, text="", font=("Georgia", 20, "bold"),
                                  bg=COLORS["bg_cream"], fg=COLORS["accent"])
        self.lbl_timer.pack()

        # ── Sequence display area ──
        self.seq_frame = tk.Frame(self, bg=COLORS["bg_card"],
                                  relief="flat", bd=0, pady=16, padx=16)
        self.seq_frame.pack(fill="x", padx=40, pady=(10, 6))

        self.lbl_seq_header = tk.Label(self.seq_frame, text="📺  Remember this sequence:",
                                       font=FONTS["heading"], bg=COLORS["bg_card"],
                                       fg=COLORS["text_mid"])
        self.lbl_seq_header.pack(anchor="w", padx=8, pady=(0, 8))

        self.seq_icons_frame = tk.Frame(self.seq_frame, bg=COLORS["bg_card"])
        self.seq_icons_frame.pack()

        # ── Player answer row ──
        ans_lbl = tk.Label(self, text="Your sequence:", font=FONTS["small"],
                            bg=COLORS["bg_cream"], fg=COLORS["text_light"])
        ans_lbl.pack(anchor="w", padx=48, pady=(6, 0))

        self.answer_frame = tk.Frame(self, bg=COLORS["bg_cream"], height=60)
        self.answer_frame.pack(fill="x", padx=40, pady=(0, 4))

        # Undo + clear buttons row
        ctrl = tk.Frame(self, bg=COLORS["bg_cream"])
        ctrl.pack(pady=2)

        self.btn_undo = tk.Button(ctrl, text="↩ Undo", font=FONTS["small"],
                                  bg=COLORS["bg_card"], fg=COLORS["text_mid"],
                                  relief="flat", bd=0, padx=14, pady=6,
                                  cursor="hand2", command=self._undo,
                                  state="disabled")
        self.btn_undo.pack(side="left", padx=6)

        self.btn_submit = tk.Button(ctrl, text="✓ Submit Answer", font=FONTS["heading"],
                                    bg=COLORS["accent"], fg=COLORS["white"],
                                    relief="flat", bd=0, padx=20, pady=8,
                                    cursor="hand2", command=self._submit,
                                    state="disabled")
        self.btn_submit.pack(side="left", padx=6)

        # ── Pool frame (clickable icons) ──
        pool_lbl = tk.Label(self, text="Click icons in the correct order →",
                            font=FONTS["small"], bg=COLORS["bg_cream"],
                            fg=COLORS["text_light"])
        pool_lbl.pack(anchor="w", padx=48, pady=(10, 2))

        self.pool_frame = tk.Frame(self, bg=COLORS["bg_card"], pady=14, padx=14)
        self.pool_frame.pack(fill="x", padx=40, pady=(0, 4))

        # ── Feedback / result area ──
        self.feedback_frame = tk.Frame(self, bg=COLORS["bg_cream"])
        self.feedback_frame.pack(fill="x", padx=40, pady=4)

        self.lbl_feedback = tk.Label(self.feedback_frame, text="", font=FONTS["heading"],
                                     bg=COLORS["bg_cream"], fg=COLORS["text_dark"],
                                     wraplength=640)
        self.lbl_feedback.pack()

        self.btn_next = tk.Button(self.feedback_frame, text="Next Level →",
                                  font=FONTS["heading"],
                                  bg=COLORS["sage"], fg=COLORS["white"],
                                  relief="flat", bd=0, padx=24, pady=10,
                                  cursor="hand2", command=self._next_level)
        # (packed dynamically)

    # ─────────────────────  Level Flow  ─────────────────────
    def _start_level(self, lvl_idx):
        self.current_level   = lvl_idx
        cfg                  = LEVELS[lvl_idx]
        self.phase           = "show"
        self.player_sequence = []
        self.btn_pool        = []

        # pick random emoji pool
        pool_src  = random.choice(ALL_EMOJI_POOLS)
        sample    = random.sample(pool_src, min(cfg["seq_len"] + cfg["extra_distractors"],
                                                len(pool_src)))
        self.sequence = random.sample(sample, cfg["seq_len"])

        # distractors: items in pool but NOT in sequence
        distractors = [e for e in pool_src if e not in self.sequence]
        extra        = random.sample(distractors, min(cfg["extra_distractors"],
                                                      len(distractors)))
        self.pool = self.sequence + extra
        random.shuffle(self.pool)

        # Update UI labels
        self.lbl_level.config(text=cfg["label"])
        self.lbl_instruction.config(
            text=f"Study the {cfg['seq_len']} icons in sequence. You have {cfg['show_time']:.0f} seconds!")
        self.lbl_feedback.config(text="")
        self.btn_next.pack_forget()
        self.btn_undo.config(state="disabled")
        self.btn_submit.config(state="disabled")

        # Show sequence
        self._render_sequence(reveal=True)
        self._clear_pool()
        self._render_answer()

        # Start countdown then hide
        self._run_countdown(cfg["show_time"])

    def _run_countdown(self, seconds_left):
        if seconds_left > 0:
            self.lbl_timer.config(text=f"⏱ {seconds_left:.0f}s")
            self._countdown_id = self.after(1000, self._run_countdown, seconds_left - 1)
        else:
            self.lbl_timer.config(text="")
            self._begin_recall()

    def _begin_recall(self):
        self.phase = "recall"
        self.lbl_instruction.config(
            text="Sequence hidden! Reconstruct it by clicking the icons below in order.")
        self._render_sequence(reveal=False)
        self._render_pool()
        self.btn_undo.config(state="normal")

    def _render_sequence(self, reveal=True):
        for w in self.seq_icons_frame.winfo_children():
            w.destroy()
        if reveal:
            for i, em in enumerate(self.sequence):
                card = tk.Frame(self.seq_icons_frame, bg=COLORS["bg_cream"],
                                bd=2, relief="flat", padx=6, pady=6)
                card.grid(row=0, column=i, padx=4)

                tk.Label(card, text=str(i+1), font=FONTS["small"],
                         bg=COLORS["bg_cream"], fg=COLORS["text_light"]).pack()
                tk.Label(card, text=em, font=FONTS["emoji"],
                         bg=COLORS["bg_cream"]).pack()
        else:
            for i in range(len(self.sequence)):
                card = tk.Frame(self.seq_icons_frame, bg=COLORS["border"],
                                width=58, height=68)
                card.grid(row=0, column=i, padx=4)
                card.pack_propagate(False)
                tk.Label(card, text="❓", font=FONTS["emoji"],
                         bg=COLORS["border"]).place(relx=.5, rely=.5, anchor="center")

    def _render_pool(self):
        self._clear_pool()
        cols = min(8, len(self.pool))
        for i, em in enumerate(self.pool):
            btn = tk.Button(self.pool_frame, text=em, font=FONTS["emoji"],
                            bg=COLORS["bg_card"], fg=COLORS["text_dark"],
                            relief="flat", bd=0, padx=10, pady=8,
                            cursor="hand2",
                            command=lambda e=em, b=None: self._on_pick(e))
            btn.grid(row=i // cols, column=i % cols, padx=5, pady=5)
            # store ref so we can disable individually
            self.btn_pool.append((em, btn))
            # re-bind with actual button ref
            btn.config(command=lambda em=em, btn=btn: self._on_pick(em, btn))

    def _clear_pool(self):
        for w in self.pool_frame.winfo_children():
            w.destroy()
        self.btn_pool = []

    def _render_answer(self):
        for w in self.answer_frame.winfo_children():
            w.destroy()
        for i, em in enumerate(self.player_sequence):
            card = tk.Frame(self.answer_frame, bg=COLORS["accent_light"],
                            bd=2, relief="flat", padx=6, pady=4)
            card.pack(side="left", padx=4, pady=6)
            tk.Label(card, text=str(i+1), font=FONTS["small"],
                     bg=COLORS["accent_light"], fg=COLORS["white"]).pack()
            tk.Label(card, text=em, font=FONTS["emoji"],
                     bg=COLORS["accent_light"]).pack()

    # ─────────────────────  Interaction  ─────────────────────
    def _on_pick(self, em, btn):
        if self.phase != "recall":
            return
        if len(self.player_sequence) >= len(self.sequence):
            return
        self.player_sequence.append(em)
        btn.config(state="disabled", bg=COLORS["border"])
        self._render_answer()
        if len(self.player_sequence) == len(self.sequence):
            self.btn_submit.config(state="normal")

    def _undo(self):
        if not self.player_sequence or self.phase != "recall":
            return
        removed = self.player_sequence.pop()
        # re-enable the corresponding button
        for em, btn in self.btn_pool:
            if em == removed and str(btn.cget("state")) == "disabled":
                btn.config(state="normal", bg=COLORS["bg_card"])
                break
        self._render_answer()
        self.btn_submit.config(state="disabled")

    def _submit(self):
        if self.phase != "recall":
            return
        self.phase = "result"

        correct = sum(1 for a, b in zip(self.player_sequence, self.sequence) if a == b)
        total   = len(self.sequence)
        frac    = correct / total
        self.level_scores.append(frac)

        # reveal correct sequence
        self._render_sequence(reveal=True)

        # Color-coded answer vs correct
        for w in self.answer_frame.winfo_children():
            w.destroy()
        for i, (player_em, correct_em) in enumerate(
                zip(self.player_sequence, self.sequence)):
            ok  = player_em == correct_em
            bg  = COLORS["success"] if ok else COLORS["error"]
            card = tk.Frame(self.answer_frame, bg=bg, padx=6, pady=4)
            card.pack(side="left", padx=4, pady=6)
            tk.Label(card, text=str(i+1), font=FONTS["small"],
                     bg=bg, fg=COLORS["white"]).pack()
            tk.Label(card, text=player_em, font=FONTS["emoji"],
                     bg=bg).pack()

        stars = "⭐" * round(frac * 5)
        self.lbl_feedback.config(
            text=f"{stars}  {correct}/{total} correct  ({frac*100:.0f}%)",
            fg=COLORS["sage"] if frac >= 0.6 else COLORS["accent_dark"])

        self.btn_undo.config(state="disabled")
        self.btn_submit.config(state="disabled")

        if self.current_level < len(LEVELS) - 1:
            self.btn_next.config(text="Next Level →", command=self._next_level)
        else:
            self.btn_next.config(text="🏁 See Results", command=self._finish)
        self.btn_next.pack(pady=8)

    def _next_level(self):
        self.btn_next.pack_forget()
        self._start_level(self.current_level + 1)

    def _finish(self):
        avg_frac  = sum(self.level_scores) / len(self.level_scores)
        final_score = round(avg_frac * 10, 1)
        self.on_complete(final_score)
