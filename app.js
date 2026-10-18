/**
 * Sahaya · Cognitive Wellness Studio
 * Main Application Logic & 6 Mini-Games Engine
 */

const AUDIO_NOTES = {
  "C4": 261.63,
  "D4": 293.66,
  "E4": 329.63,
  "F4": 349.23,
  "G4": 392.00,
  "A4": 440.00,
  "B4": 493.88,
  "C5": 523.25
};

const CATEGORY_DATA = {
  "🍽️ Kitchen": ["🍳","🥄","🔪","🫕","🥘","🍲","🥗","🫙","🧂","🥣","🍶","🫖"],
  "💼 Office":  ["📎","📏","✂️","📌","🖊️","📝","📋","💼","🖥️","⌨️","🖱️","📁"],
  "🌿 Garden":  ["🌱","🪴","🌻","🌷","🌸","🍀","🌿","🪸","🌾","🍁","🌲","🌳"],
  "🎮 Sports":  ["⚽","🏀","🏈","⚾","🥎","🎾","🏐","🏉","🥏","🏓","🏸","🥊"],
};

const ROUTINE_ACTIVITIES = [
  { id: 1, period: "🌅 Dawn · 06:30 AM", title: "Wake up & Drink Warm Water", icon: "🛏️" },
  { id: 2, period: "🌅 Morning · 07:00 AM", title: "Freshen up & Brush Teeth", icon: "🪥" },
  { id: 3, period: "🌅 Morning · 07:30 AM", title: "Morning Yoga & Meditation", icon: "🧘" },
  { id: 4, period: "🌅 Morning · 08:30 AM", title: "Nutritious Healthy Breakfast", icon: "🍳" },
  { id: 5, period: "☀️ Midday · 09:30 AM", title: "Deep Work & Creative Focus", icon: "💼" },
  { id: 6, period: "☀️ Midday · 01:00 PM", title: "Mindful Lunch & Digital Pause", icon: "🥗" },
  { id: 7, period: "☀️ Afternoon · 02:00 PM", title: "Gentle Sunlight Walk in Nature", icon: "🚶" },
  { id: 8, period: "☀️ Afternoon · 04:30 PM", title: "Afternoon Herbal Tea Break", icon: "🍵" },
  { id: 9, period: "🌆 Evening · 06:30 PM", title: "Evening Exercise & Movement", icon: "🏃" },
  { id: 10, period: "🌆 Evening · 08:00 PM", title: "Warm Dinner with Loved Ones", icon: "🍲" },
  { id: 11, period: "🌙 Night · 09:30 PM", title: "Reflective Reading & Journaling", icon: "📖" },
  { id: 12, period: "🌙 Night · 10:30 PM", title: "Lights Out & Restful Sleep", icon: "😴" }
];

const EMOJI_POOLS = [
  ["🍎","🍊","🍋","🍇","🍓","🫐","🍒","🍑","🥭","🍌","🍉","🍈"],
  ["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐮"],
  ["⚽","🏀","🎸","🎺","🎻","🎹","🎲","🎯","🎳","🎮","🕹️","🃏"],
  ["🌸","🌺","🌻","🌹","🌷","🌼","🍀","🌿","🌱","🍁","🌾","🌵"]
];

const GAMES_CONFIG = [
  {
    id: "yaad_rakho",
    name: "Yaad Rakho",
    hindi: "याद रखो",
    tag: "Memory & Recall",
    emoji: "🧠",
    color: "#c25e3b",
    desc: "Observe a fleeting sequence of symbols and reconstruct the exact order from memory.",
    levels: 5
  },
  {
    id: "dhyan_ki_chaal",
    name: "Dhyan Ki Chaal",
    hindi: "ध्यान की चाल",
    tag: "Attention & Focus",
    emoji: "👁️",
    color: "#6b8f71",
    desc: "A grid of icons appears for a breath. Reconstruct the spatial arrangement.",
    levels: 5
  },
  {
    id: "pehchaan_aur_jodo",
    name: "Pehchaan Aur Jodo",
    hindi: "पहचान और जोड़ो",
    tag: "Visual Association",
    emoji: "🃏",
    color: "#7d5a88",
    desc: "Mindful card pairs. Flip and match matching icons with minimal steps.",
    levels: 5
  },
  {
    id: "kal_aaj_kal",
    name: "Kal, Aaj, Kal",
    hindi: "कल, आज, कल",
    tag: "Voice Routine Recall",
    emoji: "🎙️",
    color: "#b87d4b",
    desc: "Speak your answers to questions about your daily routine and episodic memory with speech-to-text evaluation.",
    levels: 5
  },
  {
    id: "awaaz_pehchano",
    name: "Awaaz Pehchano",
    hindi: "आवाज़ पहचानो",
    tag: "Sound & Visual Matching",
    emoji: "🔊",
    color: "#5d6d7e",
    desc: "Listen to real environmental sounds and select the matching picture card with precision speed.",
    levels: 5
  },
  {
    id: "sahi_jagah",
    name: "Sahi Jagah",
    hindi: "सही जगह",
    tag: "Categorization & Speed",
    emoji: "🗂️",
    color: "#d97706",
    desc: "Rapid sorting under time constraint into Kitchen, Office, Garden, and Sports bins.",
    levels: 5
  }
];

class AudioSynthesizer {
  constructor() {
    this.ctx = null;
    this.onPlayCallback = null;
  }

  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioCtx();
    }
    if (this.ctx.state === "suspended") {
      this.ctx.resume();
    }
  }

  playTone(freq, duration = 0.6, type = "sine") {
    this.playSingingBowl(freq, duration);
  }

  playSingingBowl(freq, duration = 1.2) {
    try {
      this.init();
      if (this.onPlayCallback) this.onPlayCallback(freq);

      const harmonics = [
        { mult: 1.0, gain: 0.35, decay: duration },
        { mult: 2.02, gain: 0.14, decay: duration * 0.75 },
        { mult: 3.01, gain: 0.07, decay: duration * 0.55 },
        { mult: 4.03, gain: 0.03, decay: duration * 0.4 }
      ];

      harmonics.forEach(h => {
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq * h.mult, this.ctx.currentTime);
        g.gain.setValueAtTime(0.001, this.ctx.currentTime);
        g.gain.exponentialRampToValueAtTime(h.gain, this.ctx.currentTime + 0.03);
        g.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + h.decay);
        osc.connect(g);
        g.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + h.decay);
      });
    } catch (e) {
      console.warn("Audio playback not permitted or unavailable", e);
    }
  }

  playChimes(freqs, interval = 0.3) {
    freqs.forEach((f, idx) => {
      setTimeout(() => this.playSingingBowl(f, 0.9), idx * interval * 1000);
    });
  }

  playHarmonicChord(freqs, duration = 1.6) {
    try {
      this.init();
      if (this.onPlayCallback) this.onPlayCallback(freqs[0]);
      freqs.forEach(f => {
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(f, this.ctx.currentTime);
        g.gain.setValueAtTime(0.001, this.ctx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.2 / freqs.length, this.ctx.currentTime + 0.05);
        g.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);
        osc.connect(g);
        g.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + duration);
      });
    } catch(e) {}
  }

  playEnvironmentalSound(soundId) {
    try {
      this.init();
      const now = this.ctx.currentTime;
      switch(soundId) {
        case "bell": {
          const freqs = [784, 1568, 2352, 3136];
          freqs.forEach((f, i) => {
            const osc = this.ctx.createOscillator();
            const g = this.ctx.createGain();
            osc.frequency.setValueAtTime(f, now);
            g.gain.setValueAtTime(0.001, now);
            g.gain.exponentialRampToValueAtTime(0.35 / (i + 1), now + 0.02);
            g.gain.exponentialRampToValueAtTime(0.0001, now + 2.0);
            osc.connect(g);
            g.connect(this.ctx.destination);
            osc.start(now);
            osc.stop(now + 2.0);
          });
          break;
        }
        case "bird": {
          for (let burst = 0; burst < 3; burst++) {
            const t = now + burst * 0.22;
            const osc = this.ctx.createOscillator();
            const g = this.ctx.createGain();
            osc.frequency.setValueAtTime(2600, t);
            osc.frequency.exponentialRampToValueAtTime(4200, t + 0.08);
            osc.frequency.exponentialRampToValueAtTime(3100, t + 0.16);
            g.gain.setValueAtTime(0.001, t);
            g.gain.linearRampToValueAtTime(0.25, t + 0.04);
            g.gain.linearRampToValueAtTime(0.001, t + 0.18);
            osc.connect(g);
            g.connect(this.ctx.destination);
            osc.start(t);
            osc.stop(t + 0.19);
          }
          break;
        }
        case "clock": {
          [0, 0.4, 0.8, 1.2].forEach((offset, idx) => {
            const t = now + offset;
            const freq = idx % 2 === 0 ? 1200 : 900;
            const osc = this.ctx.createOscillator();
            const g = this.ctx.createGain();
            osc.type = "triangle";
            osc.frequency.setValueAtTime(freq, t);
            g.gain.setValueAtTime(0.3, t);
            g.gain.exponentialRampToValueAtTime(0.001, t + 0.04);
            osc.connect(g);
            g.connect(this.ctx.destination);
            osc.start(t);
            osc.stop(t + 0.05);
          });
          break;
        }
        case "water": {
          const bufferSize = this.ctx.sampleRate * 2.0;
          const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
          const output = noiseBuffer.getChannelData(0);
          let lastOut = 0.0;
          for (let i = 0; i < bufferSize; i++) {
            const white = Math.random() * 2 - 1;
            output[i] = (lastOut + (0.02 * white)) / 1.02;
            lastOut = output[i];
          }
          const whiteSource = this.ctx.createBufferSource();
          whiteSource.buffer = noiseBuffer;
          const filter = this.ctx.createBiquadFilter();
          filter.type = "bandpass";
          filter.frequency.setValueAtTime(500, now);
          filter.frequency.linearRampToValueAtTime(750, now + 1.0);
          filter.frequency.linearRampToValueAtTime(450, now + 2.0);
          filter.Q.value = 3.0;
          const g = this.ctx.createGain();
          g.gain.setValueAtTime(0.01, now);
          g.gain.linearRampToValueAtTime(0.4, now + 0.3);
          g.gain.linearRampToValueAtTime(0.001, now + 2.0);
          whiteSource.connect(filter);
          filter.connect(g);
          g.connect(this.ctx.destination);
          whiteSource.start(now);
          whiteSource.stop(now + 2.0);
          break;
        }
        case "drum": {
          const osc = this.ctx.createOscillator();
          const g = this.ctx.createGain();
          osc.frequency.setValueAtTime(160, now);
          osc.frequency.exponentialRampToValueAtTime(45, now + 0.35);
          g.gain.setValueAtTime(0.5, now);
          g.gain.exponentialRampToValueAtTime(0.001, now + 0.7);
          osc.connect(g);
          g.connect(this.ctx.destination);
          osc.start(now);
          osc.stop(now + 0.7);
          break;
        }
        case "horn": {
          [392, 466].forEach(f => {
            const osc = this.ctx.createOscillator();
            const g = this.ctx.createGain();
            osc.type = "sawtooth";
            osc.frequency.setValueAtTime(f, now);
            g.gain.setValueAtTime(0.12, now);
            g.gain.setValueAtTime(0.12, now + 0.45);
            g.gain.exponentialRampToValueAtTime(0.001, now + 0.55);
            osc.connect(g);
            g.connect(this.ctx.destination);
            osc.start(now);
            osc.stop(now + 0.55);
          });
          break;
        }
        case "rain": {
          for (let i = 0; i < 22; i++) {
            const t = now + Math.random() * 1.5;
            const osc = this.ctx.createOscillator();
            const g = this.ctx.createGain();
            osc.frequency.setValueAtTime(1000 + Math.random() * 2000, t);
            g.gain.setValueAtTime(0.08, t);
            g.gain.exponentialRampToValueAtTime(0.001, t + 0.03);
            osc.connect(g);
            g.connect(this.ctx.destination);
            osc.start(t);
            osc.stop(t + 0.04);
          }
          break;
        }
        case "train": {
          [520, 620].forEach(f => {
            const osc = this.ctx.createOscillator();
            const g = this.ctx.createGain();
            osc.type = "triangle";
            osc.frequency.setValueAtTime(f, now);
            g.gain.setValueAtTime(0.001, now);
            g.gain.linearRampToValueAtTime(0.18, now + 0.3);
            g.gain.setValueAtTime(0.18, now + 0.9);
            g.gain.linearRampToValueAtTime(0.001, now + 1.4);
            osc.connect(g);
            g.connect(this.ctx.destination);
            osc.start(now);
            osc.stop(now + 1.4);
          });
          break;
        }
        case "door": {
          [0, 0.25].forEach(offset => {
            const t = now + offset;
            const osc = this.ctx.createOscillator();
            const g = this.ctx.createGain();
            osc.type = "sine";
            osc.frequency.setValueAtTime(220, t);
            osc.frequency.exponentialRampToValueAtTime(90, t + 0.08);
            g.gain.setValueAtTime(0.4, t);
            g.gain.exponentialRampToValueAtTime(0.001, t + 0.09);
            osc.connect(g);
            g.connect(this.ctx.destination);
            osc.start(t);
            osc.stop(t + 0.1);
          });
          break;
        }
        case "cat": {
          const osc = this.ctx.createOscillator();
          const g = this.ctx.createGain();
          osc.type = "triangle";
          osc.frequency.setValueAtTime(500, now);
          osc.frequency.linearRampToValueAtTime(800, now + 0.3);
          osc.frequency.exponentialRampToValueAtTime(420, now + 0.8);
          g.gain.setValueAtTime(0.01, now);
          g.gain.linearRampToValueAtTime(0.2, now + 0.2);
          g.gain.exponentialRampToValueAtTime(0.001, now + 0.85);
          osc.connect(g);
          g.connect(this.ctx.destination);
          osc.start(now);
          osc.stop(now + 0.85);
          break;
        }
        default:
          this.playSingingBowl(440, 0.8);
      }
    } catch(e) {
      console.warn("Sound play error", e);
    }
  }
}

class SahayaApp {
  constructor() {
    this.audio = new AudioSynthesizer();
    this.currentGame = null;
    this.currentGameInstance = null;
    this.progress = this.loadProgress();
    this.initUI();
  }

  loadProgress() {
    const saved = localStorage.getItem("sahaya_progress_web");
    if (saved) {
      try { return JSON.parse(saved); } catch (e) {}
    }
    const def = {};
    GAMES_CONFIG.forEach(g => {
      def[g.id] = { best_score: 0.0, levels_unlocked: 1, play_count: 0, last_score: 0.0 };
    });
    return def;
  }

  saveProgress() {
    localStorage.setItem("sahaya_progress_web", JSON.stringify(this.progress));
  }

  initUI() {
    this.renderDashboardCards();
    this.updateStats();
  }

  toggleTheme() {
    document.body.classList.toggle("dark-mode");
  }

  updateStats() {
    let totalPlays = 0;
    let highest = 0.0;
    let sum = 0.0;
    let count = 0;

    Object.values(this.progress).forEach(p => {
      totalPlays += p.play_count || 0;
      if (p.best_score > highest) highest = p.best_score;
      sum += p.best_score || 0;
      count++;
    });

    const avgFocus = count > 0 ? (sum / count).toFixed(1) : "0.0";
    document.getElementById("global-focus-val").textContent = `${avgFocus} / 10`;
    document.getElementById("total-practices-completed").textContent = totalPlays;
    document.getElementById("highest-score-stat").textContent = highest.toFixed(1);
  }

  renderDashboardCards() {
    const grid = document.getElementById("practice-cards-grid");
    grid.innerHTML = "";

    GAMES_CONFIG.forEach(g => {
      const rec = this.progress[g.id] || { best_score: 0.0, levels_unlocked: 1 };
      const card = document.createElement("div");
      card.className = "practice-card";
      card.onclick = () => this.launchGame(g);

      card.innerHTML = `
        <div class="card-top">
          <div class="card-icon-wrap" style="background: ${g.color}18; color: ${g.color};">
            ${g.emoji}
          </div>
          <span class="card-badge" style="color: ${g.color}; border-color: ${g.color};">
            ${g.tag}
          </span>
        </div>
        <div class="card-title-group">
          <h3>${g.name}</h3>
          <div class="card-hindi">${g.hindi}</div>
        </div>
        <p class="card-desc">${g.desc}</p>
        <div class="card-footer">
          <div class="card-score-box">
            <span class="card-score-lbl">Best Score</span>
            <span class="card-score-val">${rec.best_score.toFixed(1)} <small>/ 10</small></span>
          </div>
          <button class="btn-play-card" style="background: ${g.color}; color: #fff;">
            Begin Ritual →
          </button>
        </div>
      `;
      grid.appendChild(card);
    });
  }

  resetAllProgress() {
    if (confirm("Reset all cognitive scores and practice progress?")) {
      localStorage.removeItem("sahaya_progress_web");
      this.progress = this.loadProgress();
      this.renderDashboardCards();
      this.updateStats();
    }
  }

  showDashboard() {
    if (this.currentGameInstance && this.currentGameInstance.destroy) {
      this.currentGameInstance.destroy();
    }
    document.getElementById("modal-result").classList.remove("active");
    document.getElementById("view-game").classList.remove("active");
    document.getElementById("view-dashboard").classList.add("active");
    this.renderDashboardCards();
    this.updateStats();
  }

  launchGame(gameConfig) {
    this.currentGame = gameConfig;
    document.getElementById("view-dashboard").classList.remove("active");
    document.getElementById("view-game").classList.add("active");
    document.getElementById("modal-result").classList.remove("active");

    document.getElementById("arena-game-title").textContent = `${gameConfig.emoji} ${gameConfig.name} (${gameConfig.hindi})`;
    document.getElementById("arena-game-tag").textContent = gameConfig.tag;
    document.getElementById("arena-game-tag").style.color = gameConfig.color;

    const container = document.getElementById("arena-content-area");
    container.innerHTML = "";

    // Instantiate game class
    switch(gameConfig.id) {
      case "yaad_rakho":
        this.currentGameInstance = new YaadRakhoGame(container, this);
        break;
      case "dhyan_ki_chaal":
        this.currentGameInstance = new DhyanKiChaalGame(container, this);
        break;
      case "pehchaan_aur_jodo":
        this.currentGameInstance = new PehchaanGame(container, this);
        break;
      case "kal_aaj_kal":
        this.currentGameInstance = new KalAajKalGame(container, this);
        break;
      case "awaaz_pehchano":
        this.currentGameInstance = new AwaazGame(container, this);
        break;
      case "sahi_jagah":
        this.currentGameInstance = new SahiJagahGame(container, this);
        break;
    }
  }

  replayCurrentGame() {
    if (this.currentGame) {
      this.launchGame(this.currentGame);
    }
  }

  onGameComplete(score) {
    const gid = this.currentGame.id;
    const rec = this.progress[gid] || { best_score: 0.0, levels_unlocked: 1, play_count: 0 };
    rec.last_score = score;
    rec.best_score = Math.max(rec.best_score, score);
    rec.play_count = (rec.play_count || 0) + 1;
    this.progress[gid] = rec;
    this.saveProgress();

    // Show modal
    const modal = document.getElementById("modal-result");
    document.getElementById("res-game-name").textContent = `${this.currentGame.name} (${this.currentGame.hindi})`;
    document.getElementById("res-score-num").textContent = score.toFixed(1);

    const starsCount = Math.round((score / 10) * 5);
    document.getElementById("res-stars").textContent = "⭐".repeat(starsCount) + "☆".repeat(5 - starsCount);

    let feedback = "Practice makes the mind steady and sharp.";
    if (score >= 9.0) feedback = "Transcendent focus! Your mental clarity is exceptional.";
    else if (score >= 7.0) feedback = "Strong mindful precision. Well done.";
    else if (score >= 5.0) feedback = "Good session. Consistency nurtures cognitive growth.";
    document.getElementById("res-feedback-msg").textContent = feedback;

    // Animate circular ring
    const ring = document.getElementById("res-ring-progress");
    const circumference = 2 * Math.PI * 52;
    const offset = circumference - (score / 10) * circumference;
    ring.style.strokeDasharray = circumference;
    ring.style.strokeDashoffset = circumference;
    modal.classList.add("active");

    setTimeout(() => {
      ring.style.strokeDashoffset = offset;
    }, 50);
  }
}

// ─────────────────────────────────────────────────────────────
// GAME 1: YAAD RAKHO (Memory & Recall)
// ─────────────────────────────────────────────────────────────
class YaadRakhoGame {
  constructor(container, app) {
    this.container = container;
    this.app = app;
    this.level = 0;
    this.scores = [];
    this.levels = [
      { count: 3, previewMs: 4000 },
      { count: 5, previewMs: 5000 },
      { count: 7, previewMs: 6000 },
      { count: 9, previewMs: 7000 },
      { count: 11, previewMs: 8000 }
    ];
    this.startLevel(0);
  }

  destroy() {
    clearTimeout(this.timer);
    clearInterval(this.countdownInterval);
  }

  startLevel(idx) {
    this.level = idx;
    document.getElementById("arena-level-badge").textContent = `Level ${idx + 1} of 5`;
    const cfg = this.levels[idx];

    // Pick random items from pool
    const pool = EMOJI_POOLS[idx % EMOJI_POOLS.length];
    const shuffled = [...pool].sort(() => 0.5 - Math.random());
    this.targetSeq = shuffled.slice(0, cfg.count);
    this.candidatePool = [...this.targetSeq, ...shuffled.slice(cfg.count, cfg.count + 4)].sort(() => 0.5 - Math.random());
    this.userPicks = [];

    this.renderPreview(cfg.previewMs);
  }

  renderPreview(previewMs) {
    let timeLeft = Math.round(previewMs / 1000);
    this.container.innerHTML = `
      <div class="game-hud">
        <div class="hud-item">Phase: <span style="color:#c25e3b;">Memorize the Order</span></div>
        <div class="hud-item">Timer: <span id="yr-timer">${timeLeft}s</span></div>
      </div>
      <div class="game-instruction-box">
        <p class="instruction-text">Breathe gently and observe this exact sequence before it fades.</p>
      </div>
      <div class="sequence-display">
        ${this.targetSeq.map(item => `<div class="seq-tile">${item}</div>`).join("")}
      </div>
    `;

    this.countdownInterval = setInterval(() => {
      timeLeft--;
      const el = document.getElementById("yr-timer");
      if (el) el.textContent = `${timeLeft}s`;
    }, 1000);

    this.timer = setTimeout(() => {
      clearInterval(this.countdownInterval);
      this.renderInputPhase();
    }, previewMs);
  }

  renderInputPhase() {
    this.container.innerHTML = `
      <div class="game-hud">
        <div class="hud-item">Phase: <span>Reconstruct Sequence</span></div>
        <div class="hud-item">Placed: <span id="yr-placed">0 / ${this.targetSeq.length}</span></div>
      </div>
      <div class="game-instruction-box">
        <p class="instruction-text">Click the symbols below in their original chronological order.</p>
      </div>
      <div class="sequence-display" id="yr-user-slots">
        ${this.targetSeq.map((_, i) => `<div class="seq-tile empty" id="slot-${i}">?</div>`).join("")}
      </div>
      <div class="pool-container" id="yr-candidates">
        ${this.candidatePool.map((item, i) => `
          <button class="pool-btn" onclick="app.currentGameInstance.pickItem('${item}', this)">${item}</button>
        `).join("")}
      </div>
      <div style="margin-top: 1.5rem; display: flex; gap: 1rem;">
        <button class="btn-secondary" onclick="app.currentGameInstance.undoLast()">Undo Last ⌫</button>
      </div>
    `;
  }

  pickItem(item, btn) {
    if (this.userPicks.length >= this.targetSeq.length) return;
    const idx = this.userPicks.length;
    this.userPicks.push({ item, btn });
    btn.disabled = true;

    const slot = document.getElementById(`slot-${idx}`);
    if (slot) {
      slot.textContent = item;
      slot.classList.remove("empty");
    }
    document.getElementById("yr-placed").textContent = `${this.userPicks.length} / ${this.targetSeq.length}`;

    if (this.userPicks.length === this.targetSeq.length) {
      this.evaluateLevel();
    }
  }

  undoLast() {
    if (this.userPicks.length === 0) return;
    const last = this.userPicks.pop();
    last.btn.disabled = false;
    const slot = document.getElementById(`slot-${this.userPicks.length}`);
    if (slot) {
      slot.textContent = "?";
      slot.classList.add("empty");
    }
    document.getElementById("yr-placed").textContent = `${this.userPicks.length} / ${this.targetSeq.length}`;
  }

  evaluateLevel() {
    let correct = 0;
    this.targetSeq.forEach((item, i) => {
      const slot = document.getElementById(`slot-${i}`);
      if (this.userPicks[i].item === item) {
        correct++;
        slot.style.borderColor = "#6b8f71";
        slot.style.background = "#eef7f0";
      } else {
        slot.style.borderColor = "#c25e3b";
        slot.style.background = "#fdf2ee";
      }
    });

    const frac = correct / this.targetSeq.length;
    this.scores.push(frac);

    setTimeout(() => {
      if (this.level < this.levels.length - 1) {
        this.startLevel(this.level + 1);
      } else {
        const avg = this.scores.reduce((a, b) => a + b, 0) / this.scores.length;
        this.app.onGameComplete(Math.round(avg * 100) / 10);
      }
    }, 1500);
  }
}

// ─────────────────────────────────────────────────────────────
// GAME 2: DHYAN KI CHAAL (Attention & Focus Grid)
// ─────────────────────────────────────────────────────────────
class DhyanKiChaalGame {
  constructor(container, app) {
    this.container = container;
    this.app = app;
    this.level = 0;
    this.scores = [];
    this.configs = [
      { rows: 2, cols: 2, previewMs: 3000 },
      { rows: 3, cols: 3, previewMs: 4000 },
      { rows: 4, cols: 4, previewMs: 5000 },
      { rows: 5, cols: 4, previewMs: 6000 },
      { rows: 5, cols: 5, previewMs: 7000 }
    ];
    this.startLevel(0);
  }

  destroy() {
    clearTimeout(this.timer);
  }

  startLevel(idx) {
    this.level = idx;
    document.getElementById("arena-level-badge").textContent = `Level ${idx + 1} of 5`;
    const cfg = this.configs[idx];
    const totalCells = cfg.rows * cfg.cols;

    const pool = [...EMOJI_POOLS[0], ...EMOJI_POOLS[1]].sort(() => 0.5 - Math.random());
    this.gridSolution = [];
    for (let i = 0; i < totalCells; i++) {
      this.gridSolution.push(pool[i % pool.length]);
    }

    this.userPlacements = new Array(totalCells).fill(null);
    this.activeSelection = null;
    this.renderPreview(cfg);
  }

  renderPreview(cfg) {
    this.container.innerHTML = `
      <div class="game-hud">
        <div class="hud-item">Phase: <span style="color:#6b8f71;">Grid Observation</span></div>
        <div class="hud-item">Grid: <span>${cfg.rows} × ${cfg.cols}</span></div>
      </div>
      <div class="game-instruction-box">
        <p class="instruction-text">Absorb the spatial position of every symbol in the matrix.</p>
      </div>
      <div class="grid-board" style="grid-template-columns: repeat(${cfg.cols}, 68px);">
        ${this.gridSolution.map(item => `<div class="grid-cell">${item}</div>`).join("")}
      </div>
    `;

    this.timer = setTimeout(() => this.renderPlacementPhase(cfg), cfg.previewMs);
  }

  renderPlacementPhase(cfg) {
    const uniqueIcons = [...new Set(this.gridSolution)].sort(() => 0.5 - Math.random());

    this.container.innerHTML = `
      <div class="game-hud">
        <div class="hud-item">Phase: <span>Fill Grid Slots</span></div>
        <div class="hud-item">Status: <span id="dk-status">Select an icon, then click a slot</span></div>
      </div>
      <div class="grid-board" id="dk-grid" style="grid-template-columns: repeat(${cfg.cols}, 68px);">
        ${this.gridSolution.map((_, i) => `
          <div class="grid-cell" id="cell-${i}" onclick="app.currentGameInstance.placeInCell(${i})"></div>
        `).join("")}
      </div>
      <div class="pool-container">
        ${uniqueIcons.map(item => `
          <button class="pool-btn" onclick="app.currentGameInstance.selectSymbol('${item}', this)">${item}</button>
        `).join("")}
      </div>
      <div style="margin-top: 1.5rem;">
        <button class="btn-primary" onclick="app.currentGameInstance.submitGrid()">Submit Grid Solution ✓</button>
      </div>
    `;
  }

  selectSymbol(item, btn) {
    this.activeSelection = item;
    document.querySelectorAll(".pool-btn").forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    document.getElementById("dk-status").textContent = `Selected: ${item} · Click target slot`;
  }

  placeInCell(idx) {
    if (!this.activeSelection) {
      alert("Please choose a symbol from below first!");
      return;
    }
    this.userPlacements[idx] = this.activeSelection;
    const cell = document.getElementById(`cell-${idx}`);
    cell.textContent = this.activeSelection;
  }

  submitGrid() {
    let correct = 0;
    this.gridSolution.forEach((val, i) => {
      const cell = document.getElementById(`cell-${i}`);
      if (this.userPlacements[i] === val) {
        correct++;
        cell.style.borderColor = "#6b8f71";
        cell.style.background = "#eef7f0";
      } else {
        cell.style.borderColor = "#c25e3b";
        cell.style.background = "#fdf2ee";
        cell.innerHTML = `${this.userPlacements[i] || "·"} <small style="font-size:0.8rem;color:#6b8f71;">(${val})</small>`;
      }
    });

    const frac = correct / this.gridSolution.length;
    this.scores.push(frac);

    setTimeout(() => {
      if (this.level < this.configs.length - 1) {
        this.startLevel(this.level + 1);
      } else {
        const avg = this.scores.reduce((a, b) => a + b, 0) / this.scores.length;
        this.app.onGameComplete(Math.round(avg * 100) / 10);
      }
    }, 2000);
  }
}

// ─────────────────────────────────────────────────────────────
// GAME 3: PEHCHAAN AUR JODO (Card Pair Matching)
// ─────────────────────────────────────────────────────────────
class PehchaanGame {
  constructor(container, app) {
    this.container = container;
    this.app = app;
    this.level = 0;
    this.levelScores = [];
    this.configs = [
      { pairs: 4, cols: 4 },
      { pairs: 6, cols: 4 },
      { pairs: 8, cols: 4 },
      { pairs: 10, cols: 5 },
      { pairs: 12, cols: 6 }
    ];
    this.startLevel(0);
  }

  destroy() {}

  startLevel(idx) {
    this.level = idx;
    document.getElementById("arena-level-badge").textContent = `Level ${idx + 1} of 5`;
    const cfg = this.configs[idx];

    const pool = EMOJI_POOLS[idx % EMOJI_POOLS.length];
    const chosen = [...pool].sort(() => 0.5 - Math.random()).slice(0, cfg.pairs);
    const deck = [...chosen, ...chosen].sort(() => 0.5 - Math.random());

    this.deck = deck;
    this.flippedIndices = [];
    this.matchedIndices = new Set();
    this.turns = 0;
    this.render(cfg);
  }

  render(cfg) {
    this.container.innerHTML = `
      <div class="game-hud">
        <div class="hud-item">Matched Pairs: <span id="pj-pairs">0 / ${cfg.pairs}</span></div>
        <div class="hud-item">Flips: <span id="pj-turns">0</span></div>
      </div>
      <div class="game-instruction-box">
        <p class="instruction-text">Uncover matching pairs of cognitive symbols in the fewest turns.</p>
      </div>
      <div class="cards-memory-grid" style="grid-template-columns: repeat(${cfg.cols}, 75px);">
        ${this.deck.map((item, i) => `
          <div class="memory-card" id="mcard-${i}" onclick="app.currentGameInstance.flipCard(${i})">
            <span>${item}</span>
          </div>
        `).join("")}
      </div>
    `;
  }

  flipCard(idx) {
    if (this.matchedIndices.has(idx)) return;
    if (this.flippedIndices.includes(idx)) return;
    if (this.flippedIndices.length >= 2) return;

    const el = document.getElementById(`mcard-${idx}`);
    el.classList.add("flipped");
    this.flippedIndices.push(idx);

    if (this.flippedIndices.length === 2) {
      this.turns++;
      document.getElementById("pj-turns").textContent = this.turns;
      const [i1, i2] = this.flippedIndices;
      if (this.deck[i1] === this.deck[i2]) {
        // Matched
        this.matchedIndices.add(i1);
        this.matchedIndices.add(i2);
        document.getElementById(`mcard-${i1}`).classList.add("matched");
        document.getElementById(`mcard-${i2}`).classList.add("matched");
        document.getElementById("pj-pairs").textContent = `${this.matchedIndices.size / 2} / ${this.configs[this.level].pairs}`;
        this.flippedIndices = [];

        if (this.matchedIndices.size === this.deck.length) {
          this.evaluateLevel();
        }
      } else {
        // Flip back
        setTimeout(() => {
          document.getElementById(`mcard-${i1}`).classList.remove("flipped");
          document.getElementById(`mcard-${i2}`).classList.remove("flipped");
          this.flippedIndices = [];
        }, 900);
      }
    }
  }

  evaluateLevel() {
    const cfg = this.configs[this.level];
    const optimalTurns = cfg.pairs;
    const extraTurns = Math.max(0, this.turns - optimalTurns);
    const score = Math.max(2.0, 10.0 - extraTurns * 0.5);
    this.levelScores.push(score);

    setTimeout(() => {
      if (this.level < this.configs.length - 1) {
        this.startLevel(this.level + 1);
      } else {
        const avg = this.levelScores.reduce((a, b) => a + b, 0) / this.levelScores.length;
        this.app.onGameComplete(Math.round(avg * 10) / 10);
      }
    }, 1200);
  }
}

// ─────────────────────────────────────────────────────────────
// GAME 4: KAL, AAJ, KAL — Audio-Based Daily Routine Recall
// ─────────────────────────────────────────────────────────────
const ROUTINE_QUESTIONS = [
  {
    id: "breakfast",
    questionEn: "What did you eat or drink for breakfast this morning?",
    questionHi: "आज सुबह आपने नाश्ते में क्या खाया या पिया?",
    domain: "Morning Meal & Hydration",
    expectedKeywords: [
      "tea", "chai", "coffee", "milk", "water", "juice",
      "toast", "bread", "eggs", "omelet", "paratha", "poha",
      "idli", "dosa", "upma", "dalia", "cereal", "oats", "fruits",
      "apple", "banana", "biscuit", "sandwich", "ate", "drank",
      "had", "breakfast", "skipped", "nothing"
    ]
  },
  {
    id: "yesterday_evening",
    questionEn: "What was an activity or task you did yesterday evening?",
    questionHi: "कल शाम आपने कौन सा मुख्य काम या गतिविधि की थी?",
    domain: "Yesterday Evening Activity",
    expectedKeywords: [
      "walk", "walking", "park", "tv", "movie", "dinner", "cooked",
      "cooking", "read", "reading", "book", "studied", "work",
      "office", "market", "shopping", "friends", "family", "chatted",
      "talked", "exercise", "gym", "yoga", "tea", "relaxed", "home"
    ]
  },
  {
    id: "waking_routine",
    questionEn: "Tell me two or three things you did right after waking up today.",
    questionHi: "आज सोकर उठने के बाद आपने जो दो-तीन काम किए, वे बताएं।",
    domain: "Morning Routine Sequence",
    expectedKeywords: [
      "woke", "got up", "water", "brushed", "teeth", "fresh",
      "freshened", "bath", "shower", "tea", "coffee", "walk",
      "yoga", "meditated", "exercise", "stretch", "prayed", "prayer",
      "dressed", "phone", "news", "breakfast"
    ]
  },
  {
    id: "social_outdoors",
    questionEn: "Did you go outside or speak with someone yesterday? Where or with whom?",
    questionHi: "क्या कल आप बाहर गए या किसी से बात की? किसके साथ या कहाँ?",
    domain: "Social & Spatial Episodic Recall",
    expectedKeywords: [
      "went", "outside", "walk", "market", "office", "store",
      "shop", "park", "friend", "mother", "father", "son",
      "daughter", "wife", "husband", "neighbor", "colleague",
      "spoke", "talked", "call", "called", "visited", "stayed", "home"
    ]
  },
  {
    id: "sleep_routine",
    questionEn: "What time did you sleep last night, and what was your last activity before sleeping?",
    questionHi: "कल रात आप कितने बजे सोए और सोने से पहले आपने क्या किया?",
    domain: "Sleep Schedule & Wind-Down Recall",
    expectedKeywords: [
      "slept", "bed", "sleep", "night", "pm", "o'clock", "time",
      "10", "11", "12", "9", "ten", "eleven", "twelve", "nine",
      "reading", "read", "book", "phone", "tv", "water", "prayed",
      "talked", "brushed", "lights"
    ]
  }
];

class KalAajKalGame {
  constructor(container, app) {
    this.container = container;
    this.app = app;
    this.level = 0;
    this.scores = [];
    this.isRecording = false;
    this.recognition = null;
    this.currentTranscript = "";
    this.startTime = 0;
    this.typingFallback = false;
    this.initSpeechRecognition();
    this.startLevel(0);
  }

  destroy() {
    this.stopRecording();
  }

  initSpeechRecognition() {
    const SpeechAPI = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechAPI) {
      try {
        this.recognition = new SpeechAPI();
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = "en-US";

        this.recognition.onresult = (event) => {
          let interim = "";
          let finalTranscript = "";
          for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
              finalTranscript += event.results[i][0].transcript;
            } else {
              interim += event.results[i][0].transcript;
            }
          }
          this.currentTranscript = (finalTranscript || interim || "").trim();
          this.updateTranscriptUI();
        };

        this.recognition.onerror = (event) => {
          console.warn("Speech recognition notice:", event.error);
          if (event.error === "not-allowed" || event.error === "service-not-allowed") {
            this.typingFallback = true;
            this.updateFallbackUI();
          }
        };

        this.recognition.onend = () => {
          if (this.isRecording) {
            try { this.recognition.start(); } catch(e) {}
          }
        };
      } catch(e) {
        this.recognition = null;
      }
    }
  }

  startLevel(idx) {
    this.level = idx;
    document.getElementById("arena-level-badge").textContent = `Question ${idx + 1} of 5`;
    this.question = ROUTINE_QUESTIONS[idx % ROUTINE_QUESTIONS.length];
    this.currentTranscript = "";
    this.isRecording = false;
    this.startTime = Date.now();
    this.render();
  }

  render() {
    this.container.innerHTML = `
      <div class="voice-recall-container">
        <div class="game-hud">
          <div class="hud-item">Domain: <span>${this.question.domain}</span></div>
          <div class="hud-item">Phase: <span>Spoken Routine Recall</span></div>
          <div class="hud-item">Round: <span>${this.level + 1} / 5</span></div>
        </div>

        <div class="question-card">
          <span class="question-domain-badge">${this.question.domain}</span>
          <h2 class="question-text-en">"${this.question.questionEn}"</h2>
          <p class="question-text-hi">${this.question.questionHi}</p>
        </div>

        <div class="mic-zone">
          <button class="mic-button ${this.isRecording ? 'recording-active' : ''}" 
                  id="kak-mic-btn"
                  onclick="app.currentGameInstance.toggleRecording()">
            🎙️
          </button>
          <span class="mic-status-label" id="kak-mic-status">
            ${this.isRecording ? 'Listening... Speak Your Answer' : 'Click Mic to Begin Recording'}
          </span>
        </div>

        <div class="transcript-card">
          <div class="transcript-header">
            <span>Captured Spoken Answer:</span>
            <button class="btn-outline-sm" style="padding:0.15rem 0.5rem;font-size:0.7rem;" onclick="app.currentGameInstance.toggleTypingFallback()">
              ${this.typingFallback ? 'Switch to Mic 🎙️' : 'Type Instead ⌨️'}
            </button>
          </div>
          <div class="transcript-text ${!this.currentTranscript ? 'empty' : ''}" id="kak-transcript">
            ${this.currentTranscript || 'Your spoken words will transcribe here in real-time...'}
          </div>
          <div id="kak-typing-box" style="display: ${this.typingFallback ? 'block' : 'none'};">
            <input type="text" class="text-fallback-input" id="kak-text-input" 
                   placeholder="Or type what you did here..." 
                   value="${this.currentTranscript}"
                   oninput="app.currentGameInstance.onManualInput(this.value)">
          </div>
        </div>

        <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 0.5rem;">
          <button class="btn-primary" id="kak-submit-btn" onclick="app.currentGameInstance.submitResponse()">
            Submit Spoken Answer ✓
          </button>
        </div>

        <div id="kak-eval-container"></div>
      </div>
    `;
  }

  toggleRecording() {
    if (this.isRecording) {
      this.stopRecording();
    } else {
      this.startRecording();
    }
  }

  startRecording() {
    this.isRecording = true;
    const btn = document.getElementById("kak-mic-btn");
    const status = document.getElementById("kak-mic-status");
    if (btn) btn.classList.add("recording-active");
    if (status) status.textContent = "Listening... Speak naturally";

    if (this.recognition) {
      try {
        this.recognition.start();
      } catch(e) {
        console.warn("Speech API start notice:", e);
      }
    } else {
      this.typingFallback = true;
      this.updateFallbackUI();
    }
  }

  stopRecording() {
    this.isRecording = false;
    const btn = document.getElementById("kak-mic-btn");
    const status = document.getElementById("kak-mic-status");
    if (btn) btn.classList.remove("recording-active");
    if (status) status.textContent = "Recording Paused · Click to Resume";

    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch(e) {}
    }
  }

  toggleTypingFallback() {
    this.typingFallback = !this.typingFallback;
    this.updateFallbackUI();
  }

  updateFallbackUI() {
    const box = document.getElementById("kak-typing-box");
    if (box) box.style.display = this.typingFallback ? "block" : "none";
  }

  onManualInput(val) {
    this.currentTranscript = val;
    const el = document.getElementById("kak-transcript");
    if (el) {
      el.textContent = val || 'Your response will appear here...';
      el.classList.toggle("empty", !val);
    }
  }

  updateTranscriptUI() {
    const el = document.getElementById("kak-transcript");
    if (el) {
      el.textContent = this.currentTranscript || 'Listening to your voice...';
      el.classList.remove("empty");
    }
    const input = document.getElementById("kak-text-input");
    if (input && !this.typingFallback) {
      input.value = this.currentTranscript;
    }
  }

  submitResponse() {
    this.stopRecording();
    const answer = (this.currentTranscript || "").trim();
    if (!answer) {
      alert("Please speak or type your answer before submitting!");
      return;
    }

    const elapsedSec = Math.round((Date.now() - this.startTime) / 100) / 10;
    const evalResult = this.evaluateSpokenAnswer(answer, this.question, elapsedSec);
    this.scores.push(evalResult.score / 10);

    const evalContainer = document.getElementById("kak-eval-container");
    if (evalContainer) {
      evalContainer.innerHTML = `
        <div class="eval-breakdown-card">
          <div style="font-weight: 700; color: #6b8f71; font-size: 1.1rem; margin-bottom: 0.5rem;">
            ✅ Spoken Response Evaluated
          </div>
          <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.75rem;">
            "${evalResult.feedback}"
          </p>
          <div class="eval-grid">
            <div class="eval-metric">
              <span class="eval-metric-num">${evalResult.relevancePercent}%</span>
              <span class="eval-metric-lbl">Domain Relevance</span>
            </div>
            <div class="eval-metric">
              <span class="eval-metric-num">${evalResult.wordCount} words</span>
              <span class="eval-metric-lbl">Recall Detail</span>
            </div>
            <div class="eval-metric">
              <span class="eval-metric-num">${evalResult.responseTimeSec}s</span>
              <span class="eval-metric-lbl">Response Time</span>
            </div>
          </div>
          <div style="margin-top: 0.75rem; text-align: center; font-weight: 700; color: var(--accent-terracotta);">
            Round Score: ${evalResult.score} / 10
          </div>
        </div>
      `;
    }

    document.getElementById("kak-submit-btn").disabled = true;
    this.app.audio.playSingingBowl(523.25, 0.8);

    setTimeout(() => {
      if (this.level < ROUTINE_QUESTIONS.length - 1) {
        this.startLevel(this.level + 1);
      } else {
        const avg = this.scores.reduce((a, b) => a + b, 0) / this.scores.length;
        this.app.onGameComplete(Math.round(avg * 100) / 10);
      }
    }, 2800);
  }

  evaluateSpokenAnswer(transcript, questionObj, responseTimeSec) {
    const clean = transcript.toLowerCase().trim();
    const words = clean.split(/\s+/).filter(w => w.length > 0);

    // 1. Completeness & Autobiographical Detail (0 to 4.0 pts)
    let completenessPts = 0;
    if (words.length >= 7) completenessPts = 4.0;
    else if (words.length >= 4) completenessPts = 3.5;
    else if (words.length >= 2) completenessPts = 2.5;
    else completenessPts = 1.5;

    // 2. Semantic Domain Relevance (0 to 4.5 pts)
    // Matches question's semantic field without penalizing valid personal diet/routine differences
    let matchCount = 0;
    questionObj.expectedKeywords.forEach(kw => {
      if (clean.includes(kw)) matchCount++;
    });

    let relevancePts = 0;
    let feedback = "";
    if (matchCount >= 2) {
      relevancePts = 4.5;
      feedback = "Clear, context-rich autobiographical memory recalled with precision.";
    } else if (matchCount === 1) {
      relevancePts = 3.8;
      feedback = "Relevant routine details successfully retrieved.";
    } else if (words.length >= 4) {
      relevancePts = 3.2; // coherent sentence even with unlisted personal items
      feedback = "Coherent narrative recalled.";
    } else {
      relevancePts = 2.0;
      feedback = "Brief response recorded.";
    }

    // 3. Retrieval Speed bonus (0 to 1.5 pts)
    let speedPts = 1.5;
    if (responseTimeSec > 25) speedPts = 0.5;
    else if (responseTimeSec > 15) speedPts = 1.0;

    const totalScore = Math.min(10.0, Math.round((completenessPts + relevancePts + speedPts) * 10) / 10);
    return {
      score: totalScore,
      wordCount: words.length,
      matchedKeywords: matchCount,
      relevancePercent: Math.min(100, Math.round((relevancePts / 4.5) * 100)),
      responseTimeSec,
      feedback
    };
  }
}

// ─────────────────────────────────────────────────────────────
// GAME 5: AWAAZ PEHCHANO — Sound Recognition & Visual Matching
// ─────────────────────────────────────────────────────────────
const SOUND_OBJECTS = [
  { id: "bell", title: "Temple Bell", hindi: "घंटी", emoji: "🔔", desc: "Resonant brass sacred chime", category: "Instrument" },
  { id: "bird", title: "Chirping Bird", hindi: "चिड़िया", emoji: "🐦", desc: "Morning songbird melodies", category: "Nature" },
  { id: "clock", title: "Ticking Clock", hindi: "दीवार घड़ी", emoji: "⏰", desc: "Mechanical pendulum ticks", category: "Object" },
  { id: "water", title: "Flowing Stream", hindi: "बहता पानी", emoji: "🌊", desc: "Mountain river water", category: "Nature" },
  { id: "drum", title: "Beating Drum", hindi: "ढोलक / ड्रम", emoji: "🥁", desc: "Acoustic rhythmic drumbeat", category: "Instrument" },
  { id: "horn", title: "Vehicle Horn", hindi: "गाड़ी का हॉर्न", emoji: "🚗", desc: "Dual brass road alert", category: "City" },
  { id: "rain", title: "Raindrops", hindi: "बारिश की बूँदें", emoji: "🌧️", desc: "Gentle rainfall pitter-patter", category: "Nature" },
  { id: "train", title: "Train Whistle", hindi: "रेलगाड़ी की सीटी", emoji: "🚂", desc: "Locomotive horn sound", category: "Travel" },
  { id: "door", title: "Door Knocking", hindi: "दरवाज़े की दस्तक", emoji: "🚪", desc: "Double acoustic wood rap", category: "Home" },
  { id: "cat", title: "Cat Purr / Meow", hindi: "बिल्ली की आवाज़", emoji: "🐈", desc: "Gentle feline vocalization", category: "Animal" }
];

class AwaazGame {
  constructor(container, app) {
    this.container = container;
    this.app = app;
    this.level = 0;
    this.totalRounds = 5;
    this.scores = [];
    this.startLevel(0);
  }

  destroy() {}

  startLevel(idx) {
    this.level = idx;
    document.getElementById("arena-level-badge").textContent = `Sound ${idx + 1} of ${this.totalRounds}`;
    this.replaysCount = 0;
    this.startTime = Date.now();
    this.answered = false;

    // Pick 1 target sound and 3 distractors
    const shuffled = [...SOUND_OBJECTS].sort(() => 0.5 - Math.random());
    this.target = shuffled[0];
    this.choices = shuffled.slice(0, 4).sort(() => 0.5 - Math.random());

    this.render();
    setTimeout(() => this.playSound(), 400);
  }

  render() {
    this.container.innerHTML = `
      <div class="sound-matching-container">
        <div class="game-hud">
          <div class="hud-item">Phase: <span>Auditory Recognition</span></div>
          <div class="hud-item">Round: <span>${this.level + 1} of ${this.totalRounds}</span></div>
          <div class="hud-item">Replays: <span id="aw-replays">0</span></div>
        </div>

        <div class="game-instruction-box">
          <p class="instruction-text">
            Listen attentively to the environmental sound, then select the matching picture card below.
          </p>
        </div>

        <div class="sound-player-hub">
          <button class="big-speaker-btn" id="aw-speaker-btn" onclick="app.currentGameInstance.onReplayClick()">
            <span class="speaker-btn-icon">🔊</span>
            <span class="speaker-btn-lbl">Play Sound</span>
          </button>
          <div class="sound-meta-bar">
            <span class="replay-badge" id="aw-replay-badge">Replays Used: 0</span>
            <button class="btn-outline-sm" onclick="app.currentGameInstance.onReplayClick()">
              Replay Sound 🔁
            </button>
          </div>
        </div>

        <div class="picture-choices-grid" id="aw-grid">
          ${this.choices.map(c => `
            <div class="picture-card" id="pic-${c.id}" onclick="app.currentGameInstance.pickCard('${c.id}')">
              <span class="picture-card-emoji">${c.emoji}</span>
              <span class="picture-card-title">${c.title}</span>
              <span class="picture-card-category">${c.hindi} · ${c.category}</span>
            </div>
          `).join("")}
        </div>

        <div id="aw-feedback" style="margin-top: 1.5rem; font-weight: 700; height: 28px; text-align: center;"></div>
      </div>
    `;
  }

  playSound() {
    const btn = document.getElementById("aw-speaker-btn");
    if (btn) btn.classList.add("playing");
    this.app.audio.playEnvironmentalSound(this.target.id);
    setTimeout(() => {
      if (btn) btn.classList.remove("playing");
    }, 1800);
  }

  onReplayClick() {
    this.replaysCount++;
    const repEl = document.getElementById("aw-replays");
    const badge = document.getElementById("aw-replay-badge");
    if (repEl) repEl.textContent = this.replaysCount;
    if (badge) badge.textContent = `Replays Used: ${this.replaysCount}`;
    this.playSound();
  }

  pickCard(chosenId) {
    if (this.answered) return;
    this.answered = true;

    const responseTimeSec = Math.round((Date.now() - this.startTime) / 100) / 10;
    const isCorrect = chosenId === this.target.id;
    const cardEl = document.getElementById(`pic-${chosenId}`);
    const targetEl = document.getElementById(`pic-${this.target.id}`);
    const fb = document.getElementById("aw-feedback");

    // Calculate score /10
    // Correct base: 10. Deduct 0.5 per extra replay beyond 1, and 0.2 per second beyond 5s
    let roundScore = 0;
    if (isCorrect) {
      if (cardEl) cardEl.classList.add("correct-pick");
      const replayPenalty = Math.max(0, this.replaysCount - 1) * 0.5;
      const speedPenalty = Math.max(0, responseTimeSec - 5) * 0.15;
      roundScore = Math.max(4.0, Math.round((10.0 - replayPenalty - speedPenalty) * 10) / 10);

      if (fb) {
        fb.textContent = `✅ Correct! "${this.target.title}" identified in ${responseTimeSec}s (${roundScore}/10)`;
        fb.style.color = "#6b8f71";
      }
      this.app.audio.playSingingBowl(523.25, 0.6);
    } else {
      if (cardEl) cardEl.classList.add("wrong-pick");
      if (targetEl) targetEl.classList.add("correct-pick");
      roundScore = 2.0;

      if (fb) {
        fb.textContent = `❌ Sound was: "${this.target.title}" (${this.target.emoji})`;
        fb.style.color = "#c25e3b";
      }
    }

    this.scores.push(roundScore / 10);

    setTimeout(() => {
      if (this.level < this.totalRounds - 1) {
        this.startLevel(this.level + 1);
      } else {
        const avg = this.scores.reduce((a, b) => a + b, 0) / this.scores.length;
        this.app.onGameComplete(Math.round(avg * 100) / 10);
      }
    }, 2000);
  }
}

// ─────────────────────────────────────────────────────────────
// GAME 6: SAHI JAGAH (Object Categorization)
// ─────────────────────────────────────────────────────────────
class SahiJagahGame {
  constructor(container, app) {
    this.container = container;
    this.app = app;
    this.level = 0;
    this.levelScores = [];
    this.levels = [
      { categories: 2, totalItems: 8, timePerItem: 5.0 },
      { categories: 2, totalItems: 10, timePerItem: 4.5 },
      { categories: 3, totalItems: 12, timePerItem: 4.0 },
      { categories: 3, totalItems: 15, timePerItem: 3.5 },
      { categories: 4, totalItems: 18, timePerItem: 3.0 }
    ];
    this.startLevel(0);
  }

  destroy() {
    clearInterval(this.tickInterval);
  }

  startLevel(idx) {
    this.level = idx;
    document.getElementById("arena-level-badge").textContent = `Level ${idx + 1} of 5`;
    const cfg = this.levels[idx];

    const allCatKeys = Object.keys(CATEGORY_DATA);
    this.activeCats = [...allCatKeys].sort(() => 0.5 - Math.random()).slice(0, cfg.categories);

    this.itemQueue = [];
    for (let i = 0; i < cfg.totalItems; i++) {
      const cat = this.activeCats[Math.floor(Math.random() * this.activeCats.length)];
      const items = CATEGORY_DATA[cat];
      const emoji = items[Math.floor(Math.random() * items.length)];
      this.itemQueue.push({ emoji, cat });
    }

    this.correctCount = 0;
    this.totalAttempted = 0;
    this.isAnswering = false;

    this.renderLayout();
    this.nextItem();
  }

  renderLayout() {
    this.container.innerHTML = `
      <div class="game-hud">
        <div class="hud-item">Correct: <span id="sj-correct">0</span></div>
        <div class="hud-item">Items Remaining: <span id="sj-rem">${this.itemQueue.length}</span></div>
        <div class="hud-item">Timer: <span id="sj-timer-num">0.0s</span></div>
      </div>
      <div class="game-instruction-box">
        <p class="instruction-text">Sort each item into its correct category bin before the timer bar drains.</p>
      </div>
      <div class="sahi-timer-outer">
        <div class="sahi-timer-inner" id="sj-bar"></div>
      </div>
      <div class="sahi-item-card">
        <div class="sahi-item-emoji" id="sj-current-emoji">·</div>
        <div class="sahi-flash-text" id="sj-flash"></div>
      </div>
      <div class="sahi-bins-container" id="sj-bins">
        ${this.activeCats.map(cat => `
          <button class="bin-btn" onclick="app.currentGameInstance.handleSort('${cat}')">
            <span>${cat}</span>
          </button>
        `).join("")}
      </div>
    `;
  }

  nextItem() {
    clearInterval(this.tickInterval);
    this.isAnswering = false;

    if (this.itemQueue.length === 0) {
      this.evaluateLevel();
      return;
    }

    this.currentItem = this.itemQueue.shift();
    document.getElementById("sj-rem").textContent = this.itemQueue.length + 1;
    document.getElementById("sj-current-emoji").textContent = this.currentItem.emoji;
    document.getElementById("sj-flash").textContent = "";

    // Reset timer
    const cfg = this.levels[this.level];
    this.timeLeft = cfg.timePerItem;
    this.totalItemTime = cfg.timePerItem;
    this.updateTimerDisplay();

    this.tickInterval = setInterval(() => {
      this.timeLeft -= 0.1;
      this.updateTimerDisplay();
      if (this.timeLeft <= 0) {
        clearInterval(this.tickInterval);
        this.timeExpired();
      }
    }, 100);
  }

  updateTimerDisplay() {
    const ratio = Math.max(0, this.timeLeft / this.totalItemTime);
    const bar = document.getElementById("sj-bar");
    const num = document.getElementById("sj-timer-num");
    if (bar) {
      bar.style.width = `${ratio * 100}%`;
      if (ratio > 0.6) bar.style.backgroundColor = "#6b8f71";
      else if (ratio > 0.3) bar.style.backgroundColor = "#d97706";
      else bar.style.backgroundColor = "#c25e3b";
    }
    if (num) num.textContent = `${Math.max(0, this.timeLeft).toFixed(1)}s`;
  }

  timeExpired() {
    if (this.isAnswering) return;
    this.isAnswering = true;
    this.totalAttempted++;
    const flash = document.getElementById("sj-flash");
    flash.textContent = "⏰ Too slow!";
    flash.style.color = "#d97706";

    setTimeout(() => this.nextItem(), 800);
  }

  handleSort(chosenCat) {
    if (this.isAnswering || !this.currentItem) return;
    this.isAnswering = true;
    clearInterval(this.tickInterval);
    this.totalAttempted++;

    const isCorrect = chosenCat === this.currentItem.cat;
    const flash = document.getElementById("sj-flash");

    if (isCorrect) {
      this.correctCount++;
      document.getElementById("sj-correct").textContent = this.correctCount;
      flash.textContent = "✅ Correct Bin!";
      flash.style.color = "#6b8f71";
    } else {
      flash.textContent = `❌ Belongs in ${this.currentItem.cat.split(" ")[1] || this.currentItem.cat}`;
      flash.style.color = "#c25e3b";
    }

    setTimeout(() => this.nextItem(), 700);
  }

  evaluateLevel() {
    const cfg = this.levels[this.level];
    const frac = this.correctCount / cfg.totalItems;
    this.levelScores.push(frac);

    setTimeout(() => {
      if (this.level < this.levels.length - 1) {
        this.startLevel(this.level + 1);
      } else {
        const avg = this.levelScores.reduce((a, b) => a + b, 0) / this.levelScores.length;
        this.app.onGameComplete(Math.round(avg * 100) / 10);
      }
    }, 1000);
  }
}

// Global App Initialization
const app = new SahayaApp();
window.app = app;
