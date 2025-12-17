# Project Directory Structure

```
physical-ai-textbook/
│
├── 📁 frontend/                          # Docusaurus website
│   ├── 📁 docs/                         # Textbook chapters (Markdown)
│   │   ├── intro.md                     # Introduction
│   │   ├── chapter1-foundations.md      # Chapter 1
│   │   ├── chapter2-perception.md       # Chapter 2
│   │   ├── chapter3-control.md          # Chapter 3
│   │   ├── chapter4-ai-learning.md      # Chapter 4
│   │   └── chapter5-applications.md     # Chapter 5
│   │
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── Chatbot.js              # React chatbot component
│   │   │   └── Chatbot.css             # Chatbot styles + animations
│   │   │
│   │   ├── 📁 css/
│   │   │   └── custom.css              # Dark theme + motion system
│   │   │
│   │   └── 📁 theme/
│   │       └── Root.js                 # Global wrapper for chatbot
│   │
│   ├── 📁 static/
│   │   └── 📁 img/
│   │       └── logo.svg                # Robot logo
│   │
│   ├── docusaurus.config.js            # Docusaurus configuration
│   ├── sidebars.js                     # Sidebar navigation structure
│   ├── babel.config.js                 # Babel configuration
│   └── package.json                    # Frontend dependencies
│
├── 📁 backend/                          # FastAPI server
│   ├── main.py                         # API server with endpoints
│   ├── ingest_textbook.py             # Content ingestion script
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Environment template
│   └── .env                            # API keys (gitignored)
│
├── 📁 docs/                            # Original textbook source
│   ├── intro.md                        # Same as frontend/docs
│   ├── chapter1-foundations.md
│   ├── chapter2-perception.md
│   ├── chapter3-control.md
│   ├── chapter4-ai-learning.md
│   └── chapter5-applications.md
│
├── 📁 specs/                           # Spec-Kit Plus artifacts
│   └── 📁 physical-ai-textbook/
│       └── spec.md                     # Feature specification
│
├── 📁 .specify/                        # Spec-Kit Plus templates
│   ├── 📁 memory/
│   │   └── constitution.md            # Project principles
│   ├── 📁 templates/
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   ├── tasks-template.md
│   │   └── phr-template.prompt.md
│   └── 📁 scripts/
│       └── 📁 powershell/
│
├── 📁 history/                         # Prompt history records
│   ├── 📁 prompts/
│   │   ├── 📁 constitution/
│   │   ├── 📁 physical-ai-textbook/
│   │   └── 📁 general/
│   └── 📁 adr/                        # Architecture Decision Records
│
├── 📁 .claude/                         # Claude Code commands
│   └── 📁 commands/
│       ├── sp.constitution.md
│       ├── sp.specify.md
│       ├── sp.plan.md
│       ├── sp.tasks.md
│       └── sp.implement.md
│
├── 📄 README.md                        # Main documentation
├── 📄 SETUP_GUIDE.md                   # Quick setup instructions
├── 📄 DEMO_VIDEO_SCRIPT.md             # 90-second demo guide
├── 📄 PROJECT_SUMMARY.md               # Comprehensive overview
├── 📄 DIRECTORY_STRUCTURE.md           # This file
├── 📄 CLAUDE.md                        # Claude Code instructions
├── 📄 LICENSE                          # MIT License
└── 📄 .gitignore                       # Git ignore rules

```

## Key Files Explained

### Frontend
- **docusaurus.config.js**: Main configuration (theme, navbar, footer)
- **sidebars.js**: Chapter navigation structure
- **custom.css**: Complete dark theme + animation system
- **Chatbot.js**: React component with state management
- **Root.js**: Global wrapper to inject chatbot on every page

### Backend
- **main.py**: FastAPI app with REST endpoints (/api/query, /api/ingest, /health)
- **ingest_textbook.py**: Script to chunk and embed textbook content
- **requirements.txt**: Python dependencies (FastAPI, Qdrant, OpenAI)

### Documentation
- **README.md**: Complete guide with setup, API docs, deployment
- **SETUP_GUIDE.md**: Step-by-step quick start
- **DEMO_VIDEO_SCRIPT.md**: Shot-by-shot demo plan with timing
- **PROJECT_SUMMARY.md**: High-level overview and metrics

### Spec-Kit Plus
- **.specify/**: Templates and scripts for Spec-Driven Development
- **specs/**: Feature specifications
- **history/**: Prompt History Records and ADRs
- **.claude/**: Custom slash commands

## File Counts

- **Textbook chapters**: 6 files (intro + 5 chapters)
- **Frontend components**: 4 files (JS/CSS)
- **Backend files**: 3 files (Python)
- **Documentation**: 5 files (MD)
- **Configuration**: 5 files (JS/JSON/env)

**Total lines of code**: ~5,000+ (estimated)
**Total words (textbook)**: ~15,000

## Generated vs. Manual

| Component | Generated | Manual |
|-----------|-----------|--------|
| Textbook content | ✅ 100% AI | - |
| UI theme | - | ✅ Custom CSS |
| Chatbot logic | ✅ ~70% AI | 30% integration |
| Backend API | ✅ ~80% AI | 20% config |
| Documentation | ✅ ~90% AI | 10% customization |

## Next Steps After Clone

1. `cd frontend && npm install`
2. `cd backend && pip install -r requirements.txt`
3. Create `backend/.env` with API keys
4. `python backend/main.py` (start backend)
5. `python backend/ingest_textbook.py` (ingest content)
6. `npm start` in frontend (start UI)
7. Open http://localhost:3000

## Deployment Structure

```
Production Setup:
├── Frontend → Vercel
│   └── Static site (build/)
├── Backend → Railway/Render
│   └── FastAPI server
└── Database → Qdrant Cloud
    └── Vector embeddings
```
