# 🌿 Sahaya · Cognitive Wellness Studio
> **सहाया** · Mindful Mental Fitness Suite with 6 Interactive Cognitive Mini-Games

---

## 📦 Project Package

All files are located in:  
📁 `C:\Users\himan\.gemini\antigravity-ide\scratch\sahaya\`

A complete standalone zip archive is also prepared for easy download/sharing:  
🎁 **`sahaya_complete_project.zip`**

---

## 🚀 How to Run

### 1. Web Studio (In Chrome / Modern Browser)
You can run the web version locally via Python's built-in HTTP server:
```bash
cd C:\Users\himan\.gemini\antigravity-ide\scratch\sahaya
python -m http.server 8080
```
Then open your browser at:  
👉 **http://localhost:8080**

### 2. Desktop Application (Python GUI)
```bash
cd C:\Users\himan\.gemini\antigravity-ide\scratch\sahaya
pip install -r requirements.txt
python main.py
```

---

## 📁 File Structure

```
sahaya/
├── index.html                   ← Web Studio markup, header, and modals
├── styles.css                   ← Wellness design system tokens, layout, and animations
├── app.js                       ← Audio synthesis, Web Speech API & 6 game engines
├── main.py                      ← Desktop Tkinter entry point & router
├── utils.py                     ← Desktop color tokens, pools, and score I/O
├── game1_yaad_rakho.py          ← 🧠 Yaad Rakho (Memory & Recall)
├── game2_dhyan_ki_chaal.py      ← 👁️ Dhyan Ki Chaal (Spatial Attention)
├── game3_pehchaan_aur_jodo.py   ← 🃏 Pehchaan Aur Jodo (Card Matching)
├── game4_kal_aaj_kal.py         ← 🎙️ Kal, Aaj, Kal (Routine Recall)
├── game5_awaaz_pehchano.py      ← 🔊 Awaaz Pehchano (Sound Recognition)
├── game6_sahi_jagah.py          ← 🗂️ Sahi Jagah (Categorization & Speed)
├── requirements.txt             ← Desktop dependencies (Pillow, pygame)
└── sahaya_complete_project.zip  ← Portable archive of all source files
```

---

## 🎮 The 6 Cognitive Games

| # | Game | Hindi | Cognitive Focus | Key Features |
|---|------|-------|-----------------|--------------|
| 1 | **Yaad Rakho** | याद रखो | Working Memory | Sequence observation ➔ masked order recall |
| 2 | **Dhyan Ki Chaal** | ध्यान की चाल | Spatial Attention | Matrix flash ➔ slot coordinate placement ($2\times2$ to $5\times5$) |
| 3 | **Pehchaan Aur Jodo**| पहचान और जोड़ो| Visual Association | Tactile card flip pairs with efficiency scoring |
| 4 | **Kal, Aaj, Kal** | कल, आज, कल | Autobiographical Recall | Speech-to-Text voice routine recall with semantic evaluation |
| 5 | **Awaaz Pehchano** | आवाज़ पहचानो | Auditory Recognition | 10 realistic synthesized sounds ➔ randomized picture cards |
| 6 | **Sahi Jagah** | सही जगह | Categorization & Speed | Rapid object sorting into Kitchen/Office/Garden/Sports bins |

---

## 🌟 Key Highlights
- **100% Offline Capability:** Web Audio synthesizes realistic sounds dynamically without network dependencies.
- **Microphone & Speech-to-Text:** Live voice recognition with an on-demand typing fallback.
- **Standardized Scoring:** Every game calculates an accurate final score strictly out of **10.0**.
- **Cross-Platform:** Runs seamlessly in modern browsers and as a native desktop application.
