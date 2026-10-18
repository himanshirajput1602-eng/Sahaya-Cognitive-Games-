"""
Sahaya - Cognitive Wellness Studio
main.py  –  Main launcher: Dashboard + Game Router

Architecture:
  SahayaApp (Tk root)
  └── DashboardView  (main screen)
  └── GameView       (wraps any game Frame with back-nav)
"""

import tkinter as tk
from tkinter import messagebox, ttk
import math
import functools
import random
import time

from utils import (
    COLORS, FONTS,
    load_progress, save_progress, update_score, overall_focus_score,
    GAME_IDS,
)
from game1_yaad_rakho     import YaadRakhoGame
from game2_dhyan_ki_chaal import DhyanKiChaalGame
from game3_pehchaan_aur_jodo import PehchaanAurJodoGame
from game4_kal_aaj_kal    import KalAajKalGame
from game5_awaaz_pehchano import AwaazPehchanoGame
from game6_sahi_jagah     import SahiJaghGame


# ──────────────────────────────────────────────────────────
#  Game catalogue metadata
# ──────────────────────────────────────────────────────────
GAMES = [
    {
        "id":       "yaad_rakho",
        "name":     "Yaad Rakho",
        "hindi":    "याद रखो",
        "emoji":    "🧠",
        "tag":      "Memory & Recall",
        "desc":     "Study a sequence of icons, then reconstruct it from memory.",
        "color":    COLORS["game1"],
        "cls":      YaadRakhoGame,
        "levels":   5,
    },
    {
        "id":       "dhyan_ki_chaal",
        "name":     "Dhyan Ki Chaal",
        "hindi":    "ध्यान की चाल",
        "emoji":    "👁",
        "tag":      "Attention & Focus",
        "desc":     "Memorize a grid of icons and recreate it exactly.",
        "color":    COLORS["game2"],
        "cls":      DhyanKiChaalGame,
        "levels":   5,
    },
    {
        "id":       "pehchaan_aur_jodo",
        "name":     "Pehchaan Aur Jodo",
        "hindi":    "पहचान और जोड़ो",
        "emoji":    "🃏",
        "tag":      "Visual Matching",
        "desc":     "Classic card matching — flip pairs to reveal and match them.",
        "color":    COLORS["game3"],
        "cls":      PehchaanAurJodoGame,
        "levels":   5,
    },
    {
        "id":       "kal_aaj_kal",
        "name":     "Kal, Aaj, Kal",
        "hindi":    "कल, आज, कल",
        "emoji":    "🎙️",
        "tag":      "Voice & Routine Recall",
        "desc":     "Voice-guided episodic memory questions assessing daily life recall and retrieval.",
        "color":    COLORS["game4"],
        "cls":      KalAajKalGame,
        "levels":   5,
    },
    {
        "id":       "awaaz_pehchano",
        "name":     "Awaaz Pehchano",
        "hindi":    "आवाज़ पहचानो",
        "emoji":    "🎵",
        "tag":      "Sound & Visual Matching",
        "desc":     "Listen to audio cues and match them with randomized visual picture cards.",
        "color":    COLORS["game5"],
        "cls":      AwaazPehchanoGame,
        "levels":   5,
    },
    {
        "id":       "sahi_jagah",
        "name":     "Sahi Jagah",
        "hindi":    "सही जगह",
        "emoji":    "🗂",
        "tag":      "Categorization",
        "desc":     "Sort falling items into the correct category bin before time runs out.",
        "color":    COLORS["game6"],
        "cls":      SahiJaghGame,
        "levels":   5,
    },
]


# ══════════════════════════════════════════════════════════
#  Reusable components
# ══════════════════════════════════════════════════════════

class ScoreRing(tk.Canvas):
    """An animated circular progress ring showing score /10."""

    def __init__(self, master, score=0.0, color=COLORS["accent"], size=80, **kw):
        super().__init__(master, width=size, height=size,
                         bg=master.cget("bg"), highlightthickness=0, **kw)
        self._score = score
        self._color = color
        self._size  = size
        self._anim_score = 0.0
        self._draw()

    def _draw(self):
        s = self._size
        pad = 8
        self.delete("all")
        # Background ring
        self.create_oval(pad, pad, s-pad, s-pad,
                         outline=COLORS["border"], width=6)
        # Filled arc
        extent = (self._anim_score / 10.0) * 360
        if extent > 0:
            self.create_arc(pad, pad, s-pad, s-pad,
                            start=90, extent=-extent,
                            outline=self._color, width=6, style="arc")
        # Score text
        self.create_text(s//2, s//2,
                         text=f"{self._score:.1f}",
                         font=("Georgia", 13, "bold"),
                         fill=self._color if self._score > 0 else COLORS["text_light"])

    def animate_to(self, target_score):
        self._score = target_score
        self._anim_score = 0.0
        self._do_anim(target_score)

    def _do_anim(self, target):
        if self._anim_score < target:
            self._anim_score = min(self._anim_score + 0.25, target)
            self._draw()
            self.after(20, self._do_anim, target)
        else:
            self._anim_score = target
            self._draw()


class GameCard(tk.Frame):
    """A single game card on the dashboard."""

    def __init__(self, master, game_info, progress_rec, on_play, **kw):
        super().__init__(master, bg=COLORS["bg_card"],
                         relief="flat", bd=0, **kw)
        self._game    = game_info
        self._prog    = progress_rec
        self._on_play = on_play

        self._build()
        self._bind_hover_recursive(self)

    def _bind_hover_recursive(self, widget):
        """Bind hover events to the widget AND all descendants recursively."""
        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)
        for child in widget.winfo_children():
            self._bind_hover_recursive(child)

    def _build(self):
        color = self._game["color"]
        score = self._prog.get("best_score", 0.0)
        plays = self._prog.get("play_count", 0)
        lvls  = self._prog.get("levels_unlocked", 1)

        # Colored top strip
        strip = tk.Frame(self, bg=color, height=5)
        strip.pack(fill="x")

        body = tk.Frame(self, bg=COLORS["bg_card"], padx=16, pady=14)
        body.pack(fill="both", expand=True)

        # Top row: emoji + score ring
        top_row = tk.Frame(body, bg=COLORS["bg_card"])
        top_row.pack(fill="x")

        lbl_em = tk.Label(top_row, text=self._game["emoji"],
                          font=("Segoe UI Emoji", 30),
                          bg=COLORS["bg_card"])
        lbl_em.pack(side="left")

        self._ring = ScoreRing(top_row, score=score, color=color, size=72)
        self._ring.pack(side="right")

        # Game name
        tk.Label(body, text=self._game["name"],
                 font=FONTS["heading"],
                 bg=COLORS["bg_card"], fg=COLORS["text_dark"],
                 anchor="w").pack(anchor="w", pady=(6, 0))

        tk.Label(body, text=self._game["hindi"],
                 font=("Segoe UI", 10, "italic"),
                 bg=COLORS["bg_card"], fg=COLORS["text_light"],
                 anchor="w").pack(anchor="w")

        # Tag pill
        pill = tk.Frame(body, bg=color, padx=8, pady=2)
        pill.pack(anchor="w", pady=(4, 6))
        tk.Label(pill, text=self._game["tag"], font=FONTS["small"],
                 bg=color, fg=COLORS["white"]).pack()

        # Description
        tk.Label(body, text=self._game["desc"],
                 font=FONTS["small"],
                 bg=COLORS["bg_card"], fg=COLORS["text_mid"],
                 wraplength=200, justify="left",
                 anchor="w").pack(anchor="w", pady=(0, 8))

        # Meta: levels + plays
        meta = tk.Frame(body, bg=COLORS["bg_card"])
        meta.pack(fill="x")
        tk.Label(meta, text=f"🏆 Best: {score}/10",
                 font=FONTS["small"], bg=COLORS["bg_card"],
                 fg=COLORS["text_mid"]).pack(side="left")
        tk.Label(meta, text=f"🎮 Plays: {plays}",
                 font=FONTS["small"], bg=COLORS["bg_card"],
                 fg=COLORS["text_light"]).pack(side="right")

        # Level progress dots
        dot_row = tk.Frame(body, bg=COLORS["bg_card"])
        dot_row.pack(anchor="w", pady=(6, 8))
        for i in range(self._game["levels"]):
            filled = (i < lvls)
            dot_bg = color if filled else COLORS["border"]
            dot = tk.Frame(dot_row, bg=dot_bg, width=10, height=10)
            dot.pack(side="left", padx=2)

        # Play button
        self._btn_play = tk.Button(body, text="▶  Play",
                                   font=FONTS["heading"],
                                   bg=color, fg=COLORS["white"],
                                   relief="flat", bd=0,
                                   padx=20, pady=8,
                                   cursor="hand2",
                                   command=self._on_play)
        self._btn_play.pack(fill="x")

        self._ring.animate_to(score)

    def _on_enter(self, e=None):
        """Lighten card bg on hover (only non-button widgets)."""
        self._set_bg_recursive(self, COLORS["bg_hover"])

    def _on_leave(self, e=None):
        """Restore card bg when mouse leaves."""
        self._set_bg_recursive(self, COLORS["bg_card"])

    def _set_bg_recursive(self, widget, color):
        """Set bg on all non-button widgets to avoid styling the play button."""
        try:
            # Don't restyle the play button — it has its own color
            if widget is not self._btn_play:
                widget.config(bg=color)
        except Exception:
            pass
        for child in widget.winfo_children():
            self._set_bg_recursive(child, color)

    def refresh(self, progress_rec):
        """Rebuild the card UI with fresh progress data."""
        self._prog = progress_rec
        for w in self.winfo_children():
            w.destroy()
        self._build()
        self._bind_hover_recursive(self)


# ══════════════════════════════════════════════════════════
#  Dashboard View
# ══════════════════════════════════════════════════════════

class DashboardView(tk.Frame):

    def __init__(self, master, progress, on_launch_game, **kw):
        super().__init__(master, bg=COLORS["bg_cream"], **kw)
        self.progress       = progress
        self.on_launch_game = on_launch_game
        self._cards         = {}   # game_id → GameCard

        self._build()

    def _build(self):
        self._build_hero()
        self._build_overall_bar()
        self._build_grid()

    def _build_hero(self):
        hero = tk.Frame(self, bg=COLORS["bg_dark"], pady=28)
        hero.pack(fill="x")

        left = tk.Frame(hero, bg=COLORS["bg_dark"])
        left.pack(side="left", padx=40)

        tk.Label(left, text="🌿  Sahaya",
                 font=("Georgia", 34, "bold"),
                 bg=COLORS["bg_dark"], fg=COLORS["bg_cream"]).pack(anchor="w")

        tk.Label(left, text="सहाया  –  Cognitive Wellness Studio",
                 font=("Segoe UI", 13, "italic"),
                 bg=COLORS["bg_dark"], fg=COLORS["text_light"]).pack(anchor="w", pady=(2, 0))

        tk.Label(left, text="Train your mind. One game at a time.",
                 font=FONTS["small"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_light"]).pack(anchor="w", pady=(4, 0))

        # Overall score badge
        right = tk.Frame(hero, bg=COLORS["bg_dark"])
        right.pack(side="right", padx=40)

        overall = overall_focus_score(self.progress)
        tk.Label(right, text="Focus Score", font=FONTS["small"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_light"]).pack()
        self._overall_ring = ScoreRing(right, score=overall,
                                       color=COLORS["accent_light"], size=100)
        self._overall_ring.pack(pady=4)
        self._overall_ring.animate_to(overall)

        tk.Label(right, text="/ 10", font=FONTS["small"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_light"]).pack()

    def _build_overall_bar(self):
        bar = tk.Frame(self, bg=COLORS["bg_card"], pady=10)
        bar.pack(fill="x", pady=(0, 0))

        total_plays = sum(self.progress[g].get("play_count", 0) for g in GAME_IDS)
        games_tried = sum(1 for g in GAME_IDS if self.progress[g].get("play_count", 0) > 0)

        tk.Label(bar, text=f"🎮  {total_plays} total plays  •  {games_tried}/6 games explored",
                 font=FONTS["body"],
                 bg=COLORS["bg_card"], fg=COLORS["text_mid"]).pack(side="left", padx=30)

        tk.Label(bar, text="Pick a game below to start →",
                 font=FONTS["small"],
                 bg=COLORS["bg_card"], fg=COLORS["text_light"]).pack(side="right", padx=30)

    def _build_grid(self):
        # Scrollable canvas
        self._canvas = tk.Canvas(self, bg=COLORS["bg_cream"],
                                  highlightthickness=0)
        scrollbar    = ttk.Scrollbar(self, orient="vertical",
                                     command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._inner = tk.Frame(self._canvas, bg=COLORS["bg_cream"])
        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self._inner, anchor="nw")

        self._inner.bind("<Configure>", self._on_inner_configure)
        self._canvas.bind("<Configure>", self._on_canvas_resize)
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Heading
        tk.Label(self._inner, text="Your Games",
                 font=FONTS["title"],
                 bg=COLORS["bg_cream"], fg=COLORS["text_dark"]).grid(
                 row=0, column=0, columnspan=3, pady=(20, 12), padx=24, sticky="w")

        # 3-column card grid
        cols = 3
        for i, game in enumerate(GAMES):
            row = (i // cols) + 1
            col = i % cols

            # Use functools.partial to guarantee correct game captured (no closure risk)
            launch_fn = functools.partial(self.on_launch_game, game)

            card = GameCard(
                self._inner, game,
                self.progress[game["id"]],
                on_play=launch_fn,
            )
            card.grid(row=row, column=col, padx=14, pady=14, sticky="nsew")
            self._cards[game["id"]] = card

        for c in range(cols):
            self._inner.columnconfigure(c, weight=1, minsize=240)

    def _on_inner_configure(self, e):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_resize(self, e):
        self._canvas.itemconfig(self._canvas_window, width=e.width)

    def _on_mousewheel(self, e):
        self._canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    def destroy(self):
        """Unbind global mousewheel when dashboard is destroyed."""
        try:
            self._canvas.unbind_all("<MouseWheel>")
        except Exception:
            pass
        super().destroy()

    def refresh(self):
        """Reload all cards with fresh progress data."""
        overall = overall_focus_score(self.progress)
        self._overall_ring.animate_to(overall)
        for game in GAMES:
            gid  = game["id"]
            card = self._cards.get(gid)
            if card:
                card.refresh(self.progress[gid])


# ══════════════════════════════════════════════════════════
#  Game Result Screen
# ══════════════════════════════════════════════════════════

class ResultView(tk.Frame):
    """Full-screen result after completing a game."""

    def __init__(self, master, game_info, score, progress, on_back, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self._game     = game_info
        self._score    = score
        self._progress = progress
        self._on_back  = on_back
        self._build()

    def _build(self):
        color = self._game["color"]
        score = self._score

        tk.Label(self, text=self._game["emoji"],
                 font=("Segoe UI Emoji", 72),
                 bg=COLORS["bg_dark"]).pack(pady=(40, 8))

        tk.Label(self, text="Game Complete!",
                 font=("Georgia", 28, "bold"),
                 bg=COLORS["bg_dark"], fg=COLORS["bg_cream"]).pack()

        tk.Label(self, text=self._game["name"],
                 font=("Georgia", 16, "italic"),
                 bg=COLORS["bg_dark"], fg=COLORS["text_light"]).pack(pady=(2, 20))

        # Big score ring
        ring = ScoreRing(self, score=0.0, color=color, size=160)
        ring.pack()
        ring.animate_to(score)

        # Score label
        msg = "⭐ Excellent!" if score >= 8 else "👍 Good job!" if score >= 5 else "💪 Keep practicing!"
        tk.Label(self, text=msg,
                 font=("Georgia", 18),
                 bg=COLORS["bg_dark"], fg=COLORS["bg_cream"]).pack(pady=(16, 6))

        # Compare with previous best
        prev_best = self._progress.get("best_score", 0.0)
        if score > prev_best and prev_best > 0:
            tk.Label(self, text=f"🏆 New personal best! (was {prev_best}/10)",
                     font=FONTS["body"],
                     bg=COLORS["bg_dark"], fg=COLORS["accent_light"]).pack(pady=4)
        elif prev_best > 0:
            tk.Label(self, text=f"Personal best: {prev_best}/10",
                     font=FONTS["body"],
                     bg=COLORS["bg_dark"], fg=COLORS["text_light"]).pack(pady=4)

        # Star row
        stars_full  = int(score / 2)
        stars_row   = "⭐" * stars_full + "☆" * (5 - stars_full)
        tk.Label(self, text=stars_row, font=("Segoe UI Emoji", 28),
                 bg=COLORS["bg_dark"]).pack(pady=8)

        # Buttons
        btn_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="🏠  Back to Dashboard",
                  font=FONTS["heading"],
                  bg=color, fg=COLORS["white"],
                  relief="flat", bd=0, padx=28, pady=12,
                  cursor="hand2",
                  command=self._on_back).pack(side="left", padx=10)

        tk.Button(btn_frame, text="🔁  Play Again",
                  font=FONTS["heading"],
                  bg=COLORS["text_mid"], fg=COLORS["white"],
                  relief="flat", bd=0, padx=28, pady=12,
                  cursor="hand2",
                  command=lambda: self._on_back(replay=True)).pack(side="left", padx=10)


# ══════════════════════════════════════════════════════════
#  Main Application Root
# ══════════════════════════════════════════════════════════

class SahayaApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sahaya – Cognitive Wellness Studio")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(bg=COLORS["bg_cream"])

        # Try to set icon (optional, won't crash if missing)
        try:
            self.iconbitmap(default="")
        except Exception:
            pass

        self.progress = load_progress()
        self._active_view = None
        self._current_game = None

        self._show_splash()

    # ─────────────────────  Splash  ─────────────────────
    def _show_splash(self):
        self._clear()
        splash = tk.Frame(self, bg=COLORS["bg_dark"])
        splash.pack(fill="both", expand=True)
        self._active_view = splash

        tk.Label(splash, text="🌿", font=("Segoe UI Emoji", 80),
                 bg=COLORS["bg_dark"]).pack(pady=(80, 8))
        tk.Label(splash, text="Sahaya",
                 font=("Georgia", 48, "bold"),
                 bg=COLORS["bg_dark"], fg=COLORS["bg_cream"]).pack()
        tk.Label(splash, text="सहाया  •  Cognitive Wellness Studio",
                 font=("Segoe UI", 16, "italic"),
                 bg=COLORS["bg_dark"], fg=COLORS["text_light"]).pack(pady=4)
        tk.Label(splash, text="Train your mind with 6 beautiful cognitive mini-games.",
                 font=FONTS["body"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_light"]).pack(pady=8)

        tk.Button(splash, text="Enter →",
                  font=("Georgia", 18, "bold"),
                  bg=COLORS["accent"], fg=COLORS["white"],
                  relief="flat", bd=0, padx=40, pady=16,
                  cursor="hand2",
                  command=self._show_dashboard).pack(pady=30)

        tk.Label(splash, text="© 2025 Sahaya  •  Built with ❤️  in Python",
                 font=FONTS["small"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_light"]).pack(
                 side="bottom", pady=20)

    # ─────────────────────  Dashboard  ─────────────────────
    def _show_dashboard(self):
        self._clear()
        self.progress = load_progress()   # reload in case changed

        view = DashboardView(self, self.progress,
                             on_launch_game=self._launch_game)
        view.pack(fill="both", expand=True)
        self._active_view = view

    # ─────────────────────  Game launch  ─────────────────────
    def _launch_game(self, game_info):
        self._clear()
        self._current_game = game_info

        # ── Resolve game class explicitly by ID to be 100% safe ──
        game_id  = game_info["id"]
        game_cls = game_info["cls"]

        # Wrapper frame with top nav bar
        wrapper = tk.Frame(self, bg=COLORS["bg_cream"])
        wrapper.pack(fill="both", expand=True)

        # Nav bar
        nav = tk.Frame(wrapper, bg=COLORS["bg_dark"], pady=8)
        nav.pack(fill="x")

        tk.Button(nav, text="← Dashboard",
                  font=FONTS["small"],
                  bg=COLORS["bg_dark"], fg=COLORS["text_light"],
                  relief="flat", bd=0, padx=14, pady=6,
                  cursor="hand2",
                  command=self._show_dashboard).pack(side="left", padx=12)

        tk.Label(nav, text=f"{game_info['emoji']}  {game_info['name']}",
                 font=FONTS["heading"],
                 bg=COLORS["bg_dark"], fg=COLORS["bg_cream"]).pack(side="left", padx=8)

        # ── Game area: simple scrollable frame (NO bind_all to avoid blocking clicks) ──
        outer = tk.Frame(wrapper, bg=COLORS["bg_cream"])
        outer.pack(fill="both", expand=True)

        v_scroll = ttk.Scrollbar(outer, orient="vertical")
        v_scroll.pack(side="right", fill="y")

        game_canvas = tk.Canvas(outer, bg=COLORS["bg_cream"],
                                highlightthickness=0,
                                yscrollcommand=v_scroll.set)
        game_canvas.pack(side="left", fill="both", expand=True)
        v_scroll.config(command=game_canvas.yview)

        game_inner = tk.Frame(game_canvas, bg=COLORS["bg_cream"])
        cw = game_canvas.create_window((0, 0), window=game_inner, anchor="nw")

        def _on_inner_conf(e):
            game_canvas.configure(scrollregion=game_canvas.bbox("all"))

        def _on_canvas_conf(e):
            game_canvas.itemconfig(cw, width=e.width)

        def _on_scroll(e):
            game_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        game_inner.bind("<Configure>", _on_inner_conf)
        game_canvas.bind("<Configure>", _on_canvas_conf)
        # Bind mousewheel ONLY on the canvas, not globally (bind_all breaks button clicks)
        game_canvas.bind("<MouseWheel>", _on_scroll)
        game_inner.bind("<MouseWheel>", _on_scroll)

        # ── Instantiate the correct game class ──
        # Use functools.partial for on_complete to avoid any late-binding closure issue
        on_complete_fn = functools.partial(
            self._on_game_complete,
            game_id,        # positional arg 1: game_id
            game_info=game_info  # keyword arg: game_info dict
        )

        game_obj = game_cls(
            master=game_inner,
            on_complete=on_complete_fn,
            progress_data=self.progress[game_id],
        )
        game_obj.pack(fill="both", expand=True)

        self._active_view = wrapper

    # ─────────────────────  Game complete  ─────────────────────
    def _on_game_complete(self, game_id, score, game_info):
        """Called by any game when player finishes all levels."""
        # Save score to persistent progress
        update_score(self.progress, game_id, score)
        # Show result screen
        self._clear()

        on_back_fn = functools.partial(self._after_result, game_info)

        result = ResultView(
            self, game_info, score,
            progress=self.progress[game_id],
            on_back=on_back_fn,
        )
        result.pack(fill="both", expand=True)
        self._active_view = result

    def _after_result(self, game_info, replay=False):
        if replay:
            self._launch_game(game_info)
        else:
            self._show_dashboard()

    # ─────────────────────  Utility  ─────────────────────
    def _clear(self):
        if self._active_view and self._active_view.winfo_exists():
            self._active_view.destroy()
        self._active_view = None


# ──────────────────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = SahayaApp()
    app.mainloop()
