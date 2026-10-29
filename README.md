# 🤖 GoLo AI Assistant
### Intelligent Merchant & Retail Guide — Powered by NexaPrime

A professional, full-stack AI-powered assistant built for the **GoLo Merchant Platform**. Features Dual-Path RAG, real-time query prediction, step-by-step guidance, multimodal image analysis, multilingual support, and a modern single-page application interface.

---

## 🏗️ Repository Architecture

```text
golo/
├── backend/                       # FastAPI AI REST server
│   ├── app.py                     # API router
│   ├── ai_engine.py               # Core AI engine
│   ├── rag_engine.py              # TF-IDF + Gemini GenAI RAG engine
│   ├── knowledge_base.py          # FAQs and application knowledge
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Local environment secrets (do not commit)
│   └── .env.example               # Environment configuration template
│
├── frontend/                      # Main GoLo AI web application
│   ├── index.html                 # Main single-page application
│   ├── style.css                  # Responsive styles and animations
│   ├── script.js                  # Chat, voice, image and autocomplete
│   ├── bundled.html               # Single-file frontend bundle
│   └── [assets]                   # Logos, icons and preview assets
│
├── legacy-v1-robot/               # Alternative animated robot interface
│   ├── index.html
│   └── [robot assets]
│
├── docs/                          # Project specifications and FAQs
├── tests/                         # Automated tests
├── scripts/                       # Build and distribution utilities
│   └── sync_bundle.py
├── .gitignore                     # Ignore rules for secrets and caches
├── run.py                         # Development launcher
└── README.md                      # Project documentation
```

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10 or higher
- pip
- A Gemini API key if required by your configuration

### 2. Install Dependencies

Open a terminal in the project root:

```bash
cd backend
pip install -r requirements.txt
pip install numpy scikit-learn google-genai
cd ..
```

### 3. Configure Environment Variables

Create `backend/.env` using `backend/.env.example` as a template.

On Windows Command Prompt:

```cmd
copy backend\.env.example backend\.env
```

Configure the required API keys and environment variables in `backend/.env`. Keep this file private and do not commit secrets to GitLab.

### 4. Run the Application

From the project root, run:

```bash
python run.py
```

Alternatively, start the backend and frontend separately.

**Backend — Terminal 1**

```bash
cd backend
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

**Frontend — Terminal 2**

```bash
python -m http.server 3000 --directory frontend
```

### 5. Open in Your Browser

| Service | URL | Description |
|---|---|---|
| Main application | http://localhost:3000 | GoLo AI web interface |
| API documentation | http://localhost:8000/docs | Swagger API documentation |
| Backend health | http://localhost:8000/health | Service health information |
| Robot UI (v1) | http://localhost:3001 | Alternative robot interface, if separately configured |

---

## ✨ Features and Capabilities

- **Dual-Path RAG Engine:** Local TF-IDF retrieval combined with generative AI responses.
- **Intent Classification:** Routes platform-related questions and handles out-of-scope queries.
- **Real-Time Autocomplete:** Predicts merchant queries while users type.
- **Multi-Turn Chat:** Provides a conversational interface with chat navigation.
- **Chat Session Retention:** Supports chat history retention and cleanup.
- **Multimodal Image Analysis:** Supports image analysis through `/multimodal/analyze`.
- **Voice Input:** Includes speech-to-text functionality.
- **Multilingual Support:** Provides responses in supported user-selected languages.
- **Rate Limiting and Usage Tracking:** Supports merchant usage and quota tracking.
- **Customer Support Escalation:** Supports escalation to customer service.

The exact behavior and availability of these features depend on the current implementation and configuration.

---

## 🔌 API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | API status and root information |
| `GET` | `/health` | System health and knowledge status |
| `POST` | `/chat` | Conversational assistant |
| `GET` | `/suggest?q=&limit=4` | Autocomplete suggestions |
| `GET` | `/faqs` | Frequently asked questions |
| `GET` | `/faqs/popular` | Popular merchant questions |
| `GET` | `/faqs/{category}` | Category-specific FAQs |
| `GET` | `/search?query=&top_k=` | Knowledge retrieval |
| `POST` | `/ratings` | Conversation ratings |
| `POST` | `/escalate` | Customer support escalation |
| `POST` | `/multimodal/analyze` | Image analysis |
| `GET` | `/merchant/{id}/usage` | Merchant usage information |
| `GET` | `/analytics/metrics` | System analytics |
| `GET` | `/languages` | Supported language information |

For the current request parameters, response formats and endpoint behavior, refer to the running API documentation at `http://localhost:8000/docs`.

---

## 🗄️ Database Options

FAQ storage can be configured through environment variables in `backend/.env`.

- **`FAQ_SOURCE=memory`** — Uses in-memory FAQ data when supported by the application configuration.
- **`FAQ_SOURCE=database`** — Selects database-backed FAQ storage when implemented and configured.

Set `DATABASE_URL` and any other required settings according to the project's actual database implementation. Supported database engines depend on the installed dependencies and application code.

---

## 🧪 Testing

The repository includes tests for API endpoints, RAG retrieval and live suggestions.

Relevant files include:

- `tests/test_all_endpoints.py`
- `tests/test_rag.py`
- `tests/test_suggest_live.py`

Run tests according to the project's Python test configuration and ensure any required services and API credentials are configured.

---

## 🔐 Security

- Keep `.env` files, API keys, passwords and tokens out of version control.
- Use `.env.example` to document the required configuration variables.
- Review `.gitignore` before pushing project files.
- Never commit production credentials or private user data.

---

## 📤 GitLab Repository

This project is maintained in GitLab:

https://gitlab.com/nexaprime-group3/chat-bot-aaju-baju

To upload future changes, use:

```bash
git add .
git commit -m "Update GoLo AI Assistant"
git push origin main
```

Ensure sensitive files are excluded before running `git add .`.

---

## 📄 License and Confidentiality

**© 2026 GoLo AI / NexaPrime. All rights reserved.**

Proprietary software for the GoLo merchant, hyper-local discovery and retail ecosystem.

Do not redistribute or publish this software without the appropriate authorization.
