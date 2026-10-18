"""
Sahaya - Cognitive Wellness Studio
game6_sahi_jagah.py  –  Sahi Jagah (Object Categorization)

Rules:
  • Items appear one by one and the player must click the correct
    category bin before the timer bar empties.
  • 5 levels: 2 categories → 3 → 4 categories, items appear faster.
  • Score /10 based on (correct sorts) / total items per level, averaged across levels.

Fixes applied:
  - Guard all .after() callbacks with winfo_exists() to prevent crashes
    when navigating away mid-game.
  - Mutex flag (self._answering) prevents double-count from simultaneous
    timer-expiry + button-click events.
  - timer_outer parent uses pack_propagate(False) so the timer bar displays with proper height.
  - Category label formatting made safe for any emoji/text format.
  - Bin buttons styled with clear active feedback and disabling during transition.
  - Proper timer cancellation on level change and widget destruction.
"""

import tkinter as tk
import random
from utils import COLORS, FONTS, CATEGORY_DATA


# ──────────────────────────────────────────────────────────
#  Level configuration
# ──────────────────────────────────────────────────────────
LEVELS = [
    {"categories": 2, "items_total": 10, "time_per_item": 6.0,
     "label": "Level 1 – 2 Categories"},
    {"categories": 2, "items_total": 12, "time_per_item": 5.0,
     "label": "Level 2 – Faster"},
    {"categories": 3, "items_total": 15, "time_per_item": 5.0,
     "label": "Level 3 – 3 Categories"},
    {"categories": 3, "items_total": 18, "time_per_item": 4.0,
     "label": "Level 4 – Even Faster"},
    {"categories": 4, "items_total": 20, "time_per_item": 3.5,
     "label": "Level 5 – 4 Categories"},
]

ALL_CATEGORIES = list(CATEGORY_DATA.keys())

BIN_COLORS = [
    COLORS["game1"],   # terracotta
    COLORS["sage"],    # sage green
    COLORS["game3"],   # purple
    COLORS["game5"],   # blue
]


def _short_cat_name(cat_str: str) -> str:
    """Return the text portion of a category string like '🍽️ Kitchen' -> 'Kitchen'."""
    parts = cat_str.strip().split()
    return " ".join(parts[1:]) if len(parts) > 1 else cat_str


class SahiJaghGame(tk.Frame):
    """
    Self-contained Frame for Sahi Jagah.
    on_complete(score: float 0-10) is called when all levels are done.
    """

    def __init__(self, master, on_complete, progress_data, **kwargs):
        super().__init__(master, bg=COLORS["bg_cream"], **kwargs)
        self.on_complete   = on_complete
        self.progress_data = progress_data

        self.current_level = 0
        self.level_scores  = []

        # Per-level state
        self.active_cats     = []
        self.item_queue      = []
        self.current_item    = None   # (emoji, correct_cat)
        self.correct_count   = 0
        self.total_attempted = 0
        self.phase           = "idle"
        self._timer_id       = None
        self._time_left      = 0.0
        self._answering      = False  # mutex: True while transitioning after an answer

        self._build_ui()
        self.bind("<Destroy>", self._on_destroy)
        self._start_level(0)

    def _on_destroy(self, event=None):
        """Cleanup any pending timer callback when widget is removed."""
        self._cancel_timer()

    # ─────────────────────  UI Building  ─────────────────────
    def _build_ui(self):
        # ── Header ──
        hdr = tk.Frame(self, bg=COLORS["game6"], pady=12)
        hdr.pack(fill="x")

        tk.Label(hdr, text="🗂  Sahi Jagah", font=FONTS["title"],
                 bg=COLORS["game6"], fg=COLORS["white"]).pack(side="left", padx=20)

        self.lbl_level = tk.Label(hdr, text="", font=FONTS["heading"],
                                  bg=COLORS["game6"], fg=COLORS["white"])
        self.lbl_level.pack(side="right", padx=20)

        # ── Stats bar ──
        stats = tk.Frame(self, bg=COLORS["bg_card"], pady=8)
        stats.pack(fill="x")

        self.lbl_correct = tk.Label(stats, text="✅ Correct: 0",
                                    font=FONTS["heading"],
                                    bg=COLORS["bg_card"], fg=COLORS["sage"])
        self.lbl_correct.pack(side="left", padx=24)

        self.lbl_wrong = tk.Label(stats, text="❌ Wrong: 0",
                                  font=FONTS["heading"],
                                  bg=COLORS["bg_card"], fg=COLORS["accent"])
        self.lbl_wrong.pack(side="left", padx=24)

        self.lbl_remaining = tk.Label(stats, text="Items left: 0",
                                      font=FONTS["heading"],
                                      bg=COLORS["bg_card"], fg=COLORS["text_mid"])
        self.lbl_remaining.pack(side="right", padx=24)

        # ── Timer bar ──
        # Use pack_propagate(False) so height is strictly maintained
        timer_outer = tk.Frame(self, bg=COLORS["border"], height=10)
        timer_outer.pack(fill="x")
        timer_outer.pack_propagate(False)
        self.timer_bar = tk.Frame(timer_outer, bg=COLORS["sage"], height=10)
        self.timer_bar.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        # ── Instruction ──
        self.lbl_instruction = tk.Label(
            self, text="",
            font=FONTS["body"], bg=COLORS["bg_cream"], fg=COLORS["text_mid"],
            wraplength=700, justify="center")
        self.lbl_instruction.pack(pady=(10, 2))

        # ── Big item display card ──
        item_card = tk.Frame(self, bg=COLORS["bg_card"],
                             relief="flat", bd=0, pady=16)
        item_card.pack(fill="x", padx=80, pady=8)

        self.lbl_item = tk.Label(item_card, text="",
                                 font=("Segoe UI Emoji", 72),
                                 bg=COLORS["bg_card"])
        self.lbl_item.pack()

        self.lbl_timer_text = tk.Label(item_card, text="",
                                       font=("Georgia", 18, "bold"),
                                       bg=COLORS["bg_card"], fg=COLORS["accent"])
        self.lbl_timer_text.pack()

        self.lbl_flash = tk.Label(item_card, text="",
                                  font=FONTS["heading"],
                                  bg=COLORS["bg_card"])
        self.lbl_flash.pack(pady=(4, 0))

        # ── Category bin buttons container ──
        self.bins_frame = tk.Frame(self, bg=COLORS["bg_cream"])
        self.bins_frame.pack(fill="x", padx=30, pady=12)

        # ── Feedback & next-level button ──
        self.feedback_frame = tk.Frame(self, bg=COLORS["bg_cream"])
        self.feedback_frame.pack(pady=4)

        self.lbl_feedback = tk.Label(
            self.feedback_frame, text="",
            font=FONTS["heading"], bg=COLORS["bg_cream"],
            fg=COLORS["text_dark"], wraplength=680)
        self.lbl_feedback.pack()

        self.btn_next = tk.Button(
            self.feedback_frame, text="Next Level →",
            font=FONTS["heading"],
            bg=COLORS["game6"], fg=COLORS["white"],
            relief="flat", bd=0, padx=28, pady=12,
            cursor="hand2", command=self._next_level)

    # ─────────────────────  Level Flow  ─────────────────────
    def _start_level(self, lvl_idx):
        self.current_level   = lvl_idx
        cfg                  = LEVELS[lvl_idx]
        self._cancel_timer()

        self.correct_count   = 0
        self.total_attempted = 0
        self.phase           = "playing"
        self._answering      = False

        # Pick active categories for this level
        num_cats = min(cfg["categories"], len(ALL_CATEGORIES))
        self.active_cats = random.sample(ALL_CATEGORIES, num_cats)

        # Build item queue
        self.item_queue = []
        for _ in range(cfg["items_total"]):
            cat  = random.choice(self.active_cats)
            item = random.choice(CATEGORY_DATA[cat])
            self.item_queue.append((item, cat))
        random.shuffle(self.item_queue)

        # Reset UI
        self.lbl_feedback.config(text="")
        self.btn_next.pack_forget()
        self.lbl_level.config(text=cfg["label"])
        self.lbl_instruction.config(
            text=f"Sort each item into the correct category bin!  "
                 f"⏱ {cfg['time_per_item']:.1f}s per item.")

        self._update_score_labels()
        self._render_bins()
        self._next_item()

    def _render_bins(self):
        """Re-render category bin buttons for active categories."""
        for w in self.bins_frame.winfo_children():
            w.destroy()

        for i, cat in enumerate(self.active_cats):
            color = BIN_COLORS[i % len(BIN_COLORS)]
            btn   = tk.Button(
                self.bins_frame,
                text=cat,
                font=FONTS["heading"],
                bg=color, fg=COLORS["white"],
                relief="flat", bd=0,
                padx=16, pady=20,
                cursor="hand2",
                wraplength=180,
                command=lambda c=cat: self._on_sort(c))
            btn.pack(side="left", fill="x", expand=True, padx=8, pady=4)

    # ─────────────────────  Item Flow  ─────────────────────
    def _next_item(self):
        if not self.winfo_exists():
            return

        self._cancel_timer()
        self._answering = False

        if not self.item_queue:
            self._end_level()
            return

        self.current_item = self.item_queue.pop(0)
        cfg               = LEVELS[self.current_level]
        self._time_left   = cfg["time_per_item"]

        self.lbl_item.config(text=self.current_item[0], bg=COLORS["bg_card"])
        self.lbl_flash.config(text="", fg=COLORS["text_mid"], bg=COLORS["bg_card"])
        self.lbl_remaining.config(text=f"Items left: {len(self.item_queue) + 1}")

        self._set_bins_state("normal")
        self._tick()

    def _tick(self):
        if not self.winfo_exists():
            return

        cfg   = LEVELS[self.current_level]
        total = cfg["time_per_item"]
        ratio = max(0.0, self._time_left / total)

        self.timer_bar.place_configure(relwidth=ratio)
        if ratio > 0.6:
            bar_col = COLORS["success"]
        elif ratio > 0.3:
            bar_col = COLORS["warning"]
        else:
            bar_col = COLORS["error"]
        self.timer_bar.config(bg=bar_col)
        self.lbl_timer_text.config(text=f"⏱ {self._time_left:.1f}s")

        if self._time_left <= 0:
            self._time_expired()
            return

        self._time_left = round(self._time_left - 0.1, 1)
        self._timer_id  = self.after(100, self._tick)

    def _time_expired(self):
        """Player ran out of time."""
        if self._answering or not self.winfo_exists():
            return
        self._answering = True
        self._cancel_timer()

        self.total_attempted += 1
        self._set_bins_state("disabled")
        self._show_flash("⏰  Time's up!", COLORS["warning"])
        self._update_score_labels()

        self._timer_id = self.after(900, self._next_item)

    def _on_sort(self, chosen_cat):
        """Player clicked a category bin."""
        if self.phase != "playing" or self._answering or not self.winfo_exists():
            return

        self._answering = True
        self._cancel_timer()
        self._set_bins_state("disabled")

        _, correct_cat = self.current_item
        is_correct = (chosen_cat == correct_cat)
        self.total_attempted += 1

        if is_correct:
            self.correct_count += 1
            self._show_flash("✅  Correct!", COLORS["success"])
        else:
            cat_label = _short_cat_name(correct_cat)
            self._show_flash(f"❌  Goes in: {cat_label}", COLORS["error"])

        self._update_score_labels()
        self._timer_id = self.after(750, self._next_item)

    # ─────────────────────  Helpers  ─────────────────────
    def _cancel_timer(self):
        if self._timer_id is not None:
            try:
                self.after_cancel(self._timer_id)
            except Exception:
                pass
            self._timer_id = None

    def _set_bins_state(self, state: str):
        for btn in self.bins_frame.winfo_children():
            if isinstance(btn, tk.Button):
                try:
                    btn.config(state=state)
                except Exception:
                    pass

    def _show_flash(self, msg: str, color: str):
        try:
            self.lbl_flash.config(text=msg, fg=color, bg=COLORS["bg_card"])
        except Exception:
            pass

    def _update_score_labels(self):
        wrong = self.total_attempted - self.correct_count
        self.lbl_correct.config(text=f"✅ Correct: {self.correct_count}")
        self.lbl_wrong.config(text=f"❌ Wrong: {wrong}")

    # ─────────────────────  Level End & Finish  ─────────────────────
    def _end_level(self):
        if not self.winfo_exists():
            return

        self.phase = "done"
        self._cancel_timer()
        self.timer_bar.place_configure(relwidth=0)
        self.lbl_timer_text.config(text="")

        cfg   = LEVELS[self.current_level]
        total = cfg["items_total"]
        frac  = self.correct_count / total if total > 0 else 0.0
        self.level_scores.append(frac)

        pct = int(round(frac * 100))
        stars = "⭐" * round(frac * 5)
        self.lbl_feedback.config(
            text=f"{stars}  {self.correct_count}/{total} correct  ({pct}%)",
            fg=COLORS["sage"] if frac >= 0.6 else COLORS["accent_dark"])

        self.lbl_item.config(text="🎉")
        self._show_flash("Level Complete! 🎊", COLORS["sage"])

        if self.current_level < len(LEVELS) - 1:
            self.btn_next.config(text="Next Level →", command=self._next_level)
        else:
            self.btn_next.config(text="🏁 See Results", command=self._finish)
        self.btn_next.pack(pady=10)

    def _next_level(self):
        self.btn_next.pack_forget()
        self._start_level(self.current_level + 1)

    def _finish(self):
        avg_frac    = sum(self.level_scores) / len(self.level_scores) if self.level_scores else 0.0
        final_score = round(avg_frac * 10, 1)
        self.on_complete(final_score)


# Alias for backward compatibility if referenced by either name
SahiJagahGame = SahiJaghGame
