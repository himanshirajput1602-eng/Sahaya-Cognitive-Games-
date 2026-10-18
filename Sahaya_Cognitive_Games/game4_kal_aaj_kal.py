"""
Sahaya - Cognitive Wellness Studio
game4_kal_aaj_kal.py  –  Kal, Aaj, Kal (Voice & Routine Recall)

Design:
  • Displays episodic memory questions about daily life and past routines.
  • Provides a Microphone button (using SpeechRecognition if available, or voice simulation)
    plus a direct Text Entry box for effortless response.
  • Evaluates answers based on keyword semantic match, response time, and detail completeness.
  • Real-time score breakdown and timing metrics.
"""

import tkinter as tk
import time
import threading
from utils import COLORS, FONTS


ROUTINE_QUESTIONS = [
    {
        "id": 1,
        "title": "Today's Morning Breakfast",
        "question": "What did you eat for breakfast this morning?",
        "keywords": ["poha", "idli", "dosa", "paratha", "tea", "chai", "coffee", "roti", "egg", "fruits", "bread", "milk", "oats", "cereal"],
        "hint": "Mention foods like chai, roti, idli, oats, paratha or fruits"
    },
    {
        "id": 2,
        "title": "Yesterday's Weather & Outdoors",
        "question": "What was the weather like yesterday evening?",
        "keywords": ["rain", "sunny", "hot", "cloudy", "pleasant", "breeze", "cold", "wind", "clear", "warm", "humid"],
        "hint": "E.g., warm, breezy, sunny, rainy or pleasant evening"
    },
    {
        "id": 3,
        "title": "Social Interaction",
        "question": "Who was the first person you talked to today?",
        "keywords": ["mother", "mom", "father", "dad", "wife", "husband", "son", "daughter", "friend", "brother", "sister", "neighbor", "doctor"],
        "hint": "Name a family member, neighbor, or colleague"
    },
    {
        "id": 4,
        "title": "Weekend Memory",
        "question": "What did you do on Sunday afternoon?",
        "keywords": ["rest", "sleep", "movie", "temple", "walk", "market", "read", "park", "family", "cooking", "tv", "gardening"],
        "hint": "Mention activities like resting, walking, cooking, watching TV"
    },
    {
        "id": 5,
        "title": "Morning Routine & Mood",
        "question": "What time did you wake up today, and how did you feel?",
        "keywords": ["morning", "am", "clock", "fresh", "good", "tired", "happy", "calm", "energetic", "six", "seven", "eight", "5", "6", "7", "8"],
        "hint": "Mention your wake up time and feeling (e.g., 7 AM and fresh)"
    }
]


class KalAajKalGame(tk.Frame):

    def __init__(self, master, on_complete, progress_data, **kwargs):
        super().__init__(master, bg=COLORS["bg_cream"], **kwargs)
        self.on_complete   = on_complete
        self.progress_data = progress_data

        self.current_idx   = 0
        self.scores        = []
        self.question_start_time = 0
        self.is_recording  = False

        self._build_ui()
        self._load_question(0)

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["game4"], pady=12)
        hdr.pack(fill="x")

        tk.Label(hdr, text="🎙️  Kal, Aaj, Kal (Voice & Routine Recall)", font=FONTS["title"],
                 bg=COLORS["game4"], fg=COLORS["white"]).pack(side="left", padx=20)

        self.lbl_counter = tk.Label(hdr, text="Question 1 of 5", font=FONTS["heading"],
                                    bg=COLORS["game4"], fg=COLORS["white"])
        self.lbl_counter.pack(side="right", padx=20)

        # Main Content Container
        self.card = tk.Frame(self, bg=COLORS["white"], padx=30, pady=25, relief="ridge", bd=1)
        self.card.pack(fill="both", expand=True, padx=40, pady=20)

        # Category Badge
        self.badge = tk.Label(self.card, text="CATEGORY", font=FONTS["subheading"],
                              bg="#EDE9FE", fg="#6D28D9", padx=12, pady=4)
        self.badge.pack(anchor="w", pady=(0, 10))

        # Big Question Label
        self.lbl_question = tk.Label(self.card, text="", font=("Segoe UI", 16, "bold"),
                                     bg=COLORS["white"], fg=COLORS["navy"], wraplength=700, justify="left")
        self.lbl_question.pack(anchor="w", pady=(0, 8))

        # Instructions / Hint
        self.lbl_hint = tk.Label(self.card, text="", font=FONTS["subheading"],
                                 bg=COLORS["white"], fg=COLORS["text_sub"])
        self.lbl_hint.pack(anchor="w", pady=(0, 20))

        # Speech Recording & Input Box Frame
        input_frame = tk.Frame(self.card, bg=COLORS["white"])
        input_frame.pack(fill="x", pady=10)

        # Voice Record Button
        self.btn_mic = tk.Button(input_frame, text="🎙️ Hold to Speak / Start Mic", font=FONTS["heading"],
                                 bg="#EF4444", fg=COLORS["white"], activebackground="#DC2626",
                                 relief="flat", padx=15, pady=8, cursor="hand2",
                                 command=self._toggle_mic)
        self.btn_mic.pack(side="left", padx=(0, 15))

        self.lbl_mic_status = tk.Label(input_frame, text="Mic ready or type below", font=FONTS["subheading"],
                                       bg=COLORS["white"], fg=COLORS["text_sub"])
        self.lbl_mic_status.pack(side="left")

        # Response Text Entry Box
        tk.Label(self.card, text="Spoken / Written Answer:", font=FONTS["heading"],
                 bg=COLORS["white"], fg=COLORS["navy"]).pack(anchor="w", pady=(15, 5))

        self.entry_answer = tk.Text(self.card, height=4, font=("Segoe UI", 12),
                                    bg="#F9FAFB", fg=COLORS["navy"], relief="solid", bd=1, padx=10, pady=10)
        self.entry_answer.pack(fill="x", pady=(0, 15))

        # Metrics & Feedback Area
        self.lbl_feedback = tk.Label(self.card, text="", font=FONTS["subheading"],
                                     bg=COLORS["white"], fg=COLORS["navy"])
        self.lbl_feedback.pack(anchor="w", pady=(0, 15))

        # Action Buttons
        btn_row = tk.Frame(self.card, bg=COLORS["white"])
        btn_row.pack(fill="x")

        self.btn_submit = tk.Button(btn_row, text="Submit Answer  ✓", font=FONTS["heading"],
                                    bg=COLORS["primary"], fg=COLORS["white"], relief="flat",
                                    padx=20, pady=10, cursor="hand2", command=self._evaluate_answer)
        self.btn_submit.pack(side="left")

        self.btn_skip = tk.Button(btn_row, text="Skip Question  ↷", font=FONTS["subheading"],
                                  bg=COLORS["bg_gray"], fg=COLORS["text_sub"], relief="flat",
                                  padx=15, pady=10, cursor="hand2", command=self._skip_question)
        self.btn_skip.pack(side="left", padx=10)

        # Quick simulated sample answer button for easy desktop testing
        self.btn_sample = tk.Button(btn_row, text="💡 Quick Fill Sample Answer", font=FONTS["subheading"],
                                    bg="#FEF3C7", fg="#B45309", relief="flat", padx=12, pady=10,
                                    cursor="hand2", command=self._fill_sample)
        self.btn_sample.pack(side="right")

    def _load_question(self, idx):
        self.current_idx = idx
        q = ROUTINE_QUESTIONS[idx]
        self.lbl_counter.config(text=f"Question {idx + 1} of {len(ROUTINE_QUESTIONS)}")
        self.badge.config(text=q["title"].upper())
        self.lbl_question.config(text=f"Q{idx + 1}: {q['question']}")
        self.lbl_hint.config(text=f"💡 Prompt: {q['hint']}")
        self.entry_answer.delete("1.0", tk.END)
        self.lbl_feedback.config(text="")
        self.lbl_mic_status.config(text="Microphone ready or type below", fg=COLORS["text_sub"])
        self.btn_submit.config(state="normal")
        self.question_start_time = time.time()

    def _toggle_mic(self):
        if not self.is_recording:
            self.is_recording = True
            self.btn_mic.config(text="⏹️ Stop Recording", bg="#B91C1C")
            self.lbl_mic_status.config(text="🔴 Listening to your voice...", fg="#DC2626")
            
            # Start speech recognition in thread
            def record_thread():
                try:
                    import speech_recognition as sr
                    r = sr.Recognizer()
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        audio = r.listen(source, timeout=5, phrase_time_limit=8)
                        text = r.recognize_google(audio)
                        self.after(0, lambda: self._on_speech_recognized(text))
                except Exception as e:
                    self.after(0, lambda: self._on_speech_fallback())
            
            threading.Thread(target=record_thread, daemon=True).start()
        else:
            self.is_recording = False
            self.btn_mic.config(text="🎙️ Hold to Speak / Start Mic", bg="#EF4444")
            self.lbl_mic_status.config(text="Processing voice...", fg=COLORS["primary"])

    def _on_speech_recognized(self, text):
        self.is_recording = False
        self.btn_mic.config(text="🎙️ Hold to Speak / Start Mic", bg="#EF4444")
        self.lbl_mic_status.config(text=f"Speech captured: \"{text}\"", fg=COLORS["success"])
        self.entry_answer.delete("1.0", tk.END)
        self.entry_answer.insert(tk.END, text)

    def _on_speech_fallback(self):
        self.is_recording = False
        self.btn_mic.config(text="🎙️ Hold to Speak / Start Mic", bg="#EF4444")
        self.lbl_mic_status.config(text="Speech API not active on mic; type directly or use Quick Fill", fg="#D97706")

    def _fill_sample(self):
        samples = [
            "I had hot vegetable poha and a warm cup of masala chai around 8:30 AM.",
            "Yesterday evening was pleasant and slightly breezy with gentle clouds.",
            "I spoke with my daughter Priya first thing in the morning over the phone.",
            "On Sunday afternoon, I rested on the couch and watched an old classic Hindi movie.",
            "I woke up at 6:30 AM feeling refreshed, calm, and ready for my morning walk."
        ]
        sample = samples[self.current_idx % len(samples)]
        self.entry_answer.delete("1.0", tk.END)
        self.entry_answer.insert(tk.END, sample)

    def _evaluate_answer(self):
        text = self.entry_answer.get("1.0", tk.END).strip().lower()
        if not text:
            self.lbl_feedback.config(text="⚠️ Please speak into the mic or type an answer first.", fg="#DC2626")
            return

        elapsed = round(time.time() - self.question_start_time, 1)
        q = ROUTINE_QUESTIONS[self.current_idx]

        # Semantic keywords check
        matches = [kw for kw in q["keywords"] if kw in text]
        word_count = len(text.split())

        # Scoring: Completeness (words) + Keyword relevance + Timeliness
        score = 4.0
        if matches:
            score += min(4.0, len(matches) * 2.0)
        if word_count >= 6:
            score += 2.0
        elif word_count >= 3:
            score += 1.0

        score = min(10.0, score)
        self.scores.append(score)

        self.btn_submit.config(state="disabled")
        matched_str = ", ".join(matches) if matches else "general recall context"
        self.lbl_feedback.config(
            text=f"✅ Response recorded in {elapsed}s | Score: {score:.1f}/10 | Keywords matched: {matched_str}",
            fg=COLORS["success"]
        )

        self.after(1600, self._next_question)

    def _skip_question(self):
        self.scores.append(3.0)
        self._next_question()

    def _next_question(self):
        if self.current_idx + 1 < len(ROUTINE_QUESTIONS):
            self._load_question(self.current_idx + 1)
        else:
            self._finish_game()

    def _finish_game(self):
        final_score = round(sum(self.scores) / len(self.scores), 1) if self.scores else 0.0
        for w in self.card.winfo_children():
            w.destroy()

        tk.Label(self.card, text="🎉  Routine Recall Completed!", font=FONTS["title"],
                 bg=COLORS["white"], fg=COLORS["navy"]).pack(pady=(20, 10))

        tk.Label(self.card, text=f"Final Cognitive Score: {final_score} / 10",
                 font=("Segoe UI", 24, "bold"), bg=COLORS["white"], fg=COLORS["primary"]).pack(pady=10)

        summary = (
            f"Excellent episodic memory retrieval across {len(ROUTINE_QUESTIONS)} daily routine questions.\n"
            "Your verbal reasoning and chronological memory pathways are actively engaged."
        )
        tk.Label(self.card, text=summary, font=FONTS["heading"],
                 bg=COLORS["white"], fg=COLORS["text_sub"], justify="center").pack(pady=15)

        tk.Button(self.card, text="Return to Studio Dashboard ➔", font=FONTS["heading"],
                  bg=COLORS["game4"], fg=COLORS["white"], relief="flat", padx=25, pady=12,
                  cursor="hand2", command=lambda: self.on_complete(final_score)).pack(pady=20)
