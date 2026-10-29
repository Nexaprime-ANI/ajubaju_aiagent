# 🤖 GoLo AI Assistant
### Intelligent Merchant & Retail Guide — Powered by NexaPrime

A professional, full-stack AI-powered assistant built for the **GoLo Merchant Platform**. Features Dual-Path RAG, real-time query prediction, step-by-step guidance, multimodal image analysis, multilingual support, and a modern single-page application interface.

---

## 🏗️ Repository Architecture (GitLab Ready)

```
golo/
├── backend/                       # FastAPI AI REST server
│   ├── app.py                     # API router with 14+ endpoints
│   ├── ai_engine.py               # Core AI engine (sessions, quota, validation)
│   ├── rag_engine.py              # TF-IDF + Gemini GenAI RAG engine
│   ├── knowledge_base.py          # 163 canonical FAQs + app domain knowledge
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Local environment secrets (ignored by Git)
│   └── .env.example               # Template environment configuration
│
├── frontend/                      # Primary GoLo Ai v2 Web Application
│   ├── index.html                 # Main Single-Page Application (SPA)
│   ├── style.css                  # Light/Dark responsive styles & animations
│   ├── script.js                  # Frontend controller (chat, voice, image, autocomplete)
│   ├── bundled.html               # Self-contained single-file bundle distribution
│   └── [assets]                   # Logos, card icons, and preview assets
│
├── legacy-v1-robot/               # Alternative animated character interface (v1)
│   ├── index.html                 # Robot theme standalone web interface
│   └── [robot assets]             # 3D robot frames and state sprites
│
├── docs/                          # All project specifications, PDFs, and FAQs
│   ├── AI_Assistant_Full_Specification_Report.pdf
│   ├── AI_Assistant_Full_Specification_Report.txt
│   ├── Golo_AI_Assistant_Features_Specification.pdf
│   ├── Merchant_AI_Growth_Intelligence_Guide.pdf
│   └── GOLO_FAQ_DOCUMENTATION.md
│
├── tests/                         # Comprehensive test suite
│   ├── test_all_endpoints.py      # E2E test for all 14+ backend endpoints
│   ├── test_rag.py                # Standalone RAG retrieval benchmark
│   └── test_suggest_live.py       # Real-time autocomplete latency test
│
├── scripts/                       # Build & distribution utilities
│   └── sync_bundle.py             # Compiles frontend into bundled.html
│
├── .gitignore                     # Git ignore rules for secrets, caches, and logs
├── run.py                         # Single-command launcher for dev environment
└── README.md                      # Project documentation
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10 or higher
- pip

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
pip install numpy scikit-learn google-genai
cd ..
```

### 3. Configure Environment
```bash
# Copy the example environment template
cp backend/.env.example backend/.env

# Add your Gemini API key in backend/.env if not already present
```

### 4. Run Everything with One Command
```bash
python run.py
```

Or run services individually:
```bash
# Terminal 1 — Backend (Port 8000)
cd backend
python -m uvicorn app:app --host 127.0.0.1 --port 8000

# Terminal 2 — Frontend (Port 3000)
python -m http.server 3000 --directory frontend
```

### 5. Open in Browser
| Service | Link | Description |
|---|---|---|
| **Main App (GoLo Ai v2)** | http://localhost:3000 | Primary modern search & chat assistant |
| **API Documentation** | http://localhost:8000/docs | Swagger UI for testing all API endpoints |
| **Backend Health** | http://localhost:8000/health | Real-time service and knowledge status |
| **Robot UI (v1)** | http://localhost:3001 | Alternative animated robot interface |

---

## 📤 Pushing to GitLab

This repository is pre-configured with a `.gitignore` that safely excludes sensitive `.env` files, bytecode caches, and logs.

```bash
# Initialize git repository (if not already done)
git init

# Add all project files
git add .

# Create initial commit
git commit -m "feat: complete GoLo AI Assistant with clean GitLab architecture"

# Link to your GitLab remote repository
git remote add origin https://gitlab.com/your-username/golo-ai-assistant.git

# Push to main branch
git branch -M main
git push -u origin main
```

---

## ✨ Features & Capabilities

- **Dual-Path RAG Engine:** Fast local TF-IDF (163 FAQs) + Google Gemini 2.0 / 3.8 Flash generative synthesis.
- **In-Scope Intent Classifier:** Accurately routes platform queries and refuses out-of-scope inquiries (*"It is not our app related question. Please try again."*).
- **Google-Style Autocomplete:** Live query predictions generated as merchants type in the search bar.
- **ChatGPT-Style Navigation:** Seamless transition from landing search capsule to active multi-turn chat.
- **7-Day Chat Session Retention:** Automatic cleanup of chat history older than 7 calendar days.
- **Multimodal Visual Analysis:** Direct image upload analysis (`/multimodal/analyze`) for receipts and products.
- **Voice Speech-to-Text:** Integrated mic toggle with push-to-transcribe capabilities.
- **100+ Global Languages:** Language selector delivering answers in the merchant's chosen language.
- **Rate Limit & Tier Tracking:** 20 RPM / 200 RPD merchant quota tracking with upgrade workflows.
- **Customer Service Escalation:** Direct helpline contact and one-click L2 support ticket creation.

---

## 🔌 API Endpoints Summary

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | API status and root info |
| `GET` | `/health` | System health, FAQ count, and categories |
| `POST` | `/chat` | Main conversational reasoning endpoint |
| `GET` | `/suggest?q=&limit=4` | Typeahead autocomplete suggestions |
| `GET` | `/faqs` | All 163 canonical FAQs |
| `GET` | `/faqs/popular` | Most frequently asked merchant questions |
| `GET` | `/faqs/{category}` | Category-filtered FAQs |
| `GET` | `/search?query=&top_k=` | TF-IDF semantic vector search |
| `POST` | `/ratings` | Post-conversation star rating (1–5) |
| `POST` | `/escalate` | Create customer support escalation ticket |
| `POST` | `/multimodal/analyze` | Vision analysis on base64 image data |
| `GET` | `/merchant/{id}/usage` | Live RPM and quota consumption |
| `GET` | `/analytics/metrics` | System analytics and resolution rates |
| `GET` | `/languages` | 100+ supported international languages |

---

## 🗄️ Database Options

The `.env` file supports plug-and-play database backends:
- **`FAQ_SOURCE=memory`** (Default): High-speed in-memory database of 163 canonical FAQs.
- **`FAQ_SOURCE=database`**: Switch to PostgreSQL, MySQL, SQLite, or MongoDB by populating `DATABASE_URL` in `backend/.env`.

---

## 📄 License & Confidentiality

**© 2026 GoLo Ai Inc. / NexaPrime. All rights reserved.**  
Proprietary software for the GoLo hyper-local discovery and retail savings ecosystem.
