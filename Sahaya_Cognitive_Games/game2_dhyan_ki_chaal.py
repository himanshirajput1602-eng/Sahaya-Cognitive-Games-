"""
Sahaya - Cognitive Wellness Studio
game2_dhyan_ki_chaal.py  –  Dhyan Ki Chaal (Attention & Focus)

Rules:
  • A grid of emoji icons is shown briefly (study phase).
  • Grid disappears. Player sees an EMPTY grid + a pool of icons
    (including distractors) and must drag/click icons INTO the correct
    grid slots to reconstruct what was there.
  • 5 levels: grid grows from 2×2 → 3×3 → 4×4 → 5×4 → 5×5.
  • Score /10 based on correct placements / total cells.
"""

import tkinter as tk
import random
import time
from utils import COLORS, FONTS, ALL_EMOJI_POOLS


# ──────────────────────────────────────────────────────────
#  Level configuration
# ──────────────────────────────────────────────────────────
LEVELS = [
    {"rows": 2, "cols": 2, "show_time": 3.0, "distractors": 4,  "label": "Level 1 – 2×2"},
    {"rows": 3, "cols": 3, "show_time": 5.0, "distractors": 6,  "label": "Level 2 – 3×3"},
    {"rows": 4, "cols": 4, "show_time": 7.0, "distractors": 8,  "label": "Level 3 – 4×4"},
    {"rows": 5, "cols": 4, "show_time": 8.0, "distractors": 10, "label": "Level 4 – 5×4"},
    {"rows": 5, "cols": 5, "show_time": 10.0,"distractors": 12, "label": "Level 5 – 5×5"},
]


class DhyanKiChaalGame(tk.Frame):
    """
    Self-contained Frame for Dhyan Ki Chaal.
    on_complete(score: float 0-10) called when all 5 levels done.
    """

    def __init__(self, master, on_complete, progress_data, **kwargs):
        super().__init__(master, bg=COLORS["bg_cream"], **kwargs)
        self.on_complete = on_complete
        self.progress_data = progress_data

        self.current_level   = 0
        self.level_scores    = []
        self.grid_content    = []          # list of emojis (rows*cols), row-major
        self.player_grid     = []          # player's current placement (None or emoji)
        self.pool            = []          # available icons for player
        self.selected_icon   = None        # icon currently "held" by player
        self.selected_source = None        # ('pool', idx) or ('grid', idx)
        self.phase           = "idle"
        self._countdown_id   = None

        # Tkinter vars
        self.selected_var    = tk.StringVar(value="")

        self._build_ui()
        self._start_level(0)

    # ─────────────────────  UI Building  ─────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["game2"], pady=12)
        hdr.pack(fill="x")

        tk.Label(hdr, text="👁  Dhyan Ki Chaal", font=FONTS["title"],
                 bg=COLORS["game2"], fg=COLORS["white"]).pack(side="left", padx=20)

        self.lbl_level = tk.Label(hdr, text="", font=FONTS["heading"],
                                  bg=COLORS["game2"], fg=COLORS["white"])
        self.lbl_level.pack(side="right", padx=20)

        # Instruction
        self.lbl_instruction = tk.Label(self, text="", font=FONTS["body"],
                                        bg=COLORS["bg_cream"], fg=COLORS["text_mid"],
                                        wraplength=700, justify="center")
        self.lbl_instruction.pack(pady=(10, 2))

        # Timer
        self.lbl_timer = tk.Label(self, text="", font=("Georgia", 20, "bold"),
                                  bg=COLORS["bg_cream"], fg=COLORS["sage"])
        self.lbl_timer.pack()

        # ── Main content area (grid + pool side-by-side) ──
        self.content = tk.Frame(self, bg=COLORS["bg_cream"])
        self.content.pack(fill="both", expand=True, padx=30, pady=6)

        # Left: grid
        grid_outer = tk.Frame(self.content, bg=COLORS["bg_cream"])
        grid_outer.pack(side="left", fill="both", expand=True)

        tk.Label(grid_outer, text="The Frame", font=FONTS["heading"],
                 bg=COLORS["bg_cream"], fg=COLORS["text_mid"]).pack(pady=(0,6))

        self.grid_frame = tk.Frame(grid_outer, bg=COLORS["border"],
                                   bd=2, relief="sunken")
        self.grid_frame.pack(padx=10)

        # Right: pool
        pool_outer = tk.Frame(self.content, bg=COLORS["bg_cream"], padx=14)
        pool_outer.pack(side="right", fill="y")

        tk.Label(pool_outer, text="Icon Pool", font=FONTS["heading"],
                 bg=COLORS["bg_cream"], fg=COLORS["text_mid"]).pack(pady=(0,6))

        # "selected" preview
        self.lbl_selected = tk.Label(pool_outer, text="✋ Click an icon\nto pick it up",
                                     font=FONTS["small"], bg=COLORS["bg_card"],
                                     fg=COLORS["text_light"], width=12,
                                     relief="flat", bd=2, pady=8)
        self.lbl_selected.pack(pady=(0,8))

        self.pool_frame = tk.Frame(pool_outer, bg=COLORS["bg_cream"])
        self.pool_frame.pack()

        # Buttons row
        ctrl = tk.Frame(self, bg=COLORS["bg_cream"])
        ctrl.pack(pady=6)

        self.btn_clear = tk.Button(ctrl, text="🗑 Clear Grid",
                                   font=FONTS["small"],
                                   bg=COLORS["bg_card"], fg=COLORS["text_mid"],
                                   relief="flat", bd=0, padx=14, pady=6,
                                   cursor="hand2", command=self._clear_grid,
                                   state="disabled")
        self.btn_clear.pack(side="left", padx=6)

        self.btn_submit = tk.Button(ctrl, text="✓ Submit",
                                    font=FONTS["heading"],
                                    bg=COLORS["sage"], fg=COLORS["white"],
                                    relief="flat", bd=0, padx=20, pady=8,
                                    cursor="hand2", command=self._submit,
                                    state="disabled")
        self.btn_submit.pack(side="left", padx=6)

        # Feedback
        self.feedback_frame = tk.Frame(self, bg=COLORS["bg_cream"])
        self.feedback_frame.pack(fill="x", padx=40, pady=4)

        self.lbl_feedback = tk.Label(self.feedback_frame, text="",
                                     font=FONTS["heading"],
                                     bg=COLORS["bg_cream"], fg=COLORS["text_dark"],
                                     wraplength=680)
        self.lbl_feedback.pack()

        self.btn_next = tk.Button(self.feedback_frame, text="Next Level →",
                                  font=FONTS["heading"],
                                  bg=COLORS["sage"], fg=COLORS["white"],
                                  relief="flat", bd=0, padx=24, pady=10,
                                  cursor="hand2", command=self._next_level)

    # ─────────────────────  Level Flow  ─────────────────────
    def _start_level(self, lvl_idx):
        self.current_level   = lvl_idx
        cfg                  = LEVELS[lvl_idx]
        self.phase           = "show"
        self.selected_icon   = None
        self.selected_source = None

        rows, cols = cfg["rows"], cfg["cols"]
        total_cells = rows * cols

        # pick emojis for the grid
        pool_src = random.choice(ALL_EMOJI_POOLS)
        # ensure enough unique icons
        all_icons = pool_src * 3  # allow repeats in large grids
        self.grid_content = [random.choice(pool_src) for _ in range(total_cells)]

        # Player grid starts empty
        self.player_grid = [None] * total_cells

        # Pool = grid icons + distractors (shuffled)
        distractor_pool = [e for e in pool_src if e not in set(self.grid_content)]
        extra = random.sample(distractor_pool * 3,
                              min(cfg["distractors"], len(distractor_pool)))
        self.pool = list(self.grid_content) + extra
        random.shuffle(self.pool)

        self.lbl_level.config(text=cfg["label"])
        self.lbl_instruction.config(
            text=f"Study the {rows}×{cols} grid. You have {cfg['show_time']:.0f}s!")
        self.lbl_feedback.config(text="")
        self.btn_next.pack_forget()
        self.btn_submit.config(state="disabled")
        self.btn_clear.config(state="disabled")
        self.lbl_selected.config(text="✋ Click an icon\nto pick it up",
                                 bg=COLORS["bg_card"], fg=COLORS["text_light"])

        self._render_grid(reveal=True, rows=rows, cols=cols)
        self._render_pool_hidden()

        self._run_countdown(cfg["show_time"])

    def _run_countdown(self, secs):
        if secs > 0:
            self.lbl_timer.config(text=f"⏱ {secs:.0f}s")
            self._countdown_id = self.after(1000, self._run_countdown, secs - 1)
        else:
            self.lbl_timer.config(text="")
            self._begin_recall()

    def _begin_recall(self):
        self.phase = "recall"
        cfg = LEVELS[self.current_level]
        rows, cols = cfg["rows"], cfg["cols"]
        self.lbl_instruction.config(
            text="Grid hidden! Place the correct icons in their original positions.")
        self._render_grid(reveal=False, rows=rows, cols=cols)
        self._render_pool_visible()
        self.btn_clear.config(state="normal")
        self.btn_submit.config(state="normal")

    # ──────────────  Rendering helpers  ──────────────
    def _render_grid(self, reveal, rows, cols):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        for r in range(rows):
            for c in range(cols):
                idx = r * cols + c
                cell_bg = COLORS["bg_card"] if reveal else COLORS["border"]
                cell = tk.Frame(self.grid_frame, bg=cell_bg,
                                width=68, height=68, bd=1, relief="groove")
                cell.grid(row=r, column=c, padx=2, pady=2)
                cell.pack_propagate(False)

                if reveal:
                    em = self.grid_content[idx]
                    lbl = tk.Label(cell, text=em, font=FONTS["emoji"],
                                   bg=cell_bg)
                    lbl.place(relx=.5, rely=.5, anchor="center")
                else:
                    # Clickable drop zone
                    placed = self.player_grid[idx]
                    if placed:
                        lbl = tk.Label(cell, text=placed, font=FONTS["emoji"],
                                       bg=COLORS["sage_light"])
                        lbl.place(relx=.5, rely=.5, anchor="center")
                        cell.config(bg=COLORS["sage_light"])
                        cell.bind("<Button-1>",
                                  lambda e, i=idx: self._on_cell_click(i))
                        lbl.bind("<Button-1>",
                                 lambda e, i=idx: self._on_cell_click(i))
                    else:
                        cell.bind("<Button-1>",
                                  lambda e, i=idx: self._on_cell_click(i))
                        tk.Label(cell, text="+", font=FONTS["heading"],
                                 bg=cell_bg, fg=COLORS["text_light"]).place(
                                 relx=.5, rely=.5, anchor="center")

    def _render_pool_hidden(self):
        for w in self.pool_frame.winfo_children():
            w.destroy()

    def _render_pool_visible(self):
        for w in self.pool_frame.winfo_children():
            w.destroy()

        cols = 3
        for i, em in enumerate(self.pool):
            state   = "normal" if em not in self._placed_pool_icons() else "disabled"
            btn_bg  = COLORS["bg_card"] if state == "normal" else COLORS["border"]
            btn = tk.Button(self.pool_frame, text=em, font=FONTS["emoji_sm"],
                            bg=btn_bg, relief="flat", bd=0,
                            padx=8, pady=6, cursor="hand2",
                            state=state,
                            command=lambda em=em, i=i: self._on_pool_pick(em, i))
            btn.grid(row=i // cols, column=i % cols, padx=4, pady=4)

    def _placed_pool_icons(self):
        """Returns list of emojis already placed in grid by player."""
        return [e for e in self.player_grid if e is not None]

    # ──────────────  Interaction  ──────────────
    def _on_pool_pick(self, em, idx):
        if self.phase != "recall":
            return
        self.selected_icon   = em
        self.selected_source = ("pool", idx)
        self.lbl_selected.config(text=f"Holding:\n{em}", font=FONTS["emoji"],
                                 bg=COLORS["accent_light"], fg=COLORS["white"])

    def _on_cell_click(self, cell_idx):
        if self.phase != "recall":
            return
        cfg = LEVELS[self.current_level]
        rows, cols = cfg["rows"], cfg["cols"]

        if self.selected_icon:
            # Place selected icon into this cell
            old = self.player_grid[cell_idx]
            self.player_grid[cell_idx] = self.selected_icon
            self.selected_icon   = None
            self.selected_source = None
            self.lbl_selected.config(text="✋ Click an icon\nto pick it up",
                                     bg=COLORS["bg_card"], fg=COLORS["text_light"],
                                     font=FONTS["small"])
            self._render_grid(reveal=False, rows=rows, cols=cols)
            self._render_pool_visible()
        else:
            # Pick up from cell
            if self.player_grid[cell_idx]:
                self.selected_icon   = self.player_grid[cell_idx]
                self.selected_source = ("grid", cell_idx)
                self.player_grid[cell_idx] = None
                self.lbl_selected.config(
                    text=f"Holding:\n{self.selected_icon}", font=FONTS["emoji"],
                    bg=COLORS["accent_light"], fg=COLORS["white"])
                self._render_grid(reveal=False, rows=rows, cols=cols)
                self._render_pool_visible()

    def _clear_grid(self):
        self.player_grid = [None] * len(self.player_grid)
        self.selected_icon   = None
        self.selected_source = None
        self.lbl_selected.config(text="✋ Click an icon\nto pick it up",
                                 bg=COLORS["bg_card"], fg=COLORS["text_light"],
                                 font=FONTS["small"])
        cfg = LEVELS[self.current_level]
        rows, cols = cfg["rows"], cfg["cols"]
        self._render_grid(reveal=False, rows=rows, cols=cols)
        self._render_pool_visible()

    def _submit(self):
        if self.phase != "recall":
            return
        self.phase = "result"

        correct = sum(1 for p, g in zip(self.player_grid, self.grid_content) if p == g)
        total   = len(self.grid_content)
        frac    = correct / total
        self.level_scores.append(frac)

        # Reveal correct grid with color coding
        cfg = LEVELS[self.current_level]
        rows, cols = cfg["rows"], cfg["cols"]
        for w in self.grid_frame.winfo_children():
            w.destroy()

        for r in range(rows):
            for c in range(cols):
                idx     = r * cols + c
                correct_em  = self.grid_content[idx]
                player_em   = self.player_grid[idx]
                ok      = player_em == correct_em
                bg      = COLORS["success"] if ok else COLORS["error"]

                cell = tk.Frame(self.grid_frame, bg=bg,
                                width=68, height=68, bd=1, relief="groove")
                cell.grid(row=r, column=c, padx=2, pady=2)
                cell.pack_propagate(False)

                show_em = player_em if player_em else "✕"
                tk.Label(cell, text=show_em, font=FONTS["emoji_sm"],
                         bg=bg).place(relx=.5, rely=.5, anchor="center")

        stars = "⭐" * round(frac * 5)
        self.lbl_feedback.config(
            text=f"{stars}  {correct}/{total} cells correct  ({frac*100:.0f}%)",
            fg=COLORS["sage"] if frac >= 0.6 else COLORS["accent_dark"])

        self.btn_submit.config(state="disabled")
        self.btn_clear.config(state="disabled")

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
