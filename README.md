# Physical AI & Humanoid Robotics Textbook

An AI-native, interactive textbook on Physical AI and Humanoid Robotics, built for a hackathon using **Spec-Kit Plus** and **Claude Code**. Features a modern dark UI with motion-driven design and an embedded RAG chatbot powered by Qdrant and OpenAI.

![Demo](https://via.placeholder.com/1200x600/1a1d23/00d9ff?text=Physical+AI+Textbook)

## Features

- **AI-Generated Content**: 5 comprehensive chapters on Physical AI, written by Claude
- **Modern Dark Theme**: Dark-neutral gradient with electric cyan accents
- **Motion-First Design**: Smooth animations inspired by Vercel Docs + Linear.app
- **RAG Chatbot**: Embedded AI tutor with context-aware Q&A
- **Selected Text Questions**: Highlight text and ask specific questions
- **Responsive Design**: Mobile-first, works on all devices
- **Fast & Lightweight**: Built with Docusaurus for blazing-fast performance

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Docusaurus)             │
│  - Dark gradient theme                              │
│  - 5 textbook chapters                              │
│  - Floating chatbot UI                              │
│  - Smooth animations & transitions                  │
└─────────────────┬───────────────────────────────────┘
                  │ HTTP/REST
┌─────────────────▼───────────────────────────────────┐
│                Backend (FastAPI)                     │
│  - /api/query: Process questions                    │
│  - /api/ingest: Add content to vector DB            │
│  - Embedding generation (OpenAI)                    │
└─────────────────┬───────────────────────────────────┘
                  │ gRPC/HTTP
┌─────────────────▼───────────────────────────────────┐
│               Vector Database (Qdrant Cloud)         │
│  - Stores textbook embeddings                       │
│  - Semantic search for RAG                          │
│  - Fast retrieval (< 50ms)                          │
└─────────────────────────────────────────────────────┘
```

## Tech Stack

**Frontend**:
- Docusaurus 3.0
- React 18
- Custom CSS (dark theme + animations)

**Backend**:
- FastAPI (Python 3.11+)
- OpenAI API (embeddings + chat)
- Qdrant Cloud (vector database)

**Development**:
- Spec-Kit Plus workflow
- Claude Code agent
- Git for version control

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- OpenAI API key
- Qdrant Cloud account (free tier available)

### 1. Clone Repository

```bash
git clone https://github.com/your-username/physical-ai-textbook.git
cd physical-ai-textbook
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys:
#   OPENAI_API_KEY=sk-...
#   QDRANT_URL=https://your-cluster.qdrant.io
#   QDRANT_API_KEY=...
```

### 3. Initialize Qdrant & Ingest Content

```bash
# Start the FastAPI server first
python main.py

# In another terminal, run the ingestion script
python ingest_textbook.py
```

This will:
1. Create a Qdrant collection
2. Chunk the textbook chapters
3. Generate embeddings
4. Upload to Qdrant Cloud

**Expected output**:
```
🚀 Physical AI Textbook Ingestion Pipeline
==================================================
✓ Created collection: physical_ai_textbook
📚 Found 5 markdown files
📖 Processing: intro.md
  ✓ Created 8 chunks
...
📥 Ingesting 67 chunks...
✅ Successfully ingested 67 chunks into Qdrant!
```

### 4. Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm start
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 5. Test the Chatbot

1. Click the floating chatbot button (bottom-right, breathing animation)
2. Ask: "What is Zero Moment Point?"
3. Select text on the page, then ask: "Explain this in simpler terms"

## Project Structure

```
physical-ai-textbook/
├── frontend/                    # Docusaurus site
│   ├── docs/                   # Textbook chapters (Markdown)
│   │   ├── intro.md
│   │   ├── chapter1-foundations.md
│   │   ├── chapter2-perception.md
│   │   ├── chapter3-control.md
│   │   ├── chapter4-ai-learning.md
│   │   └── chapter5-applications.md
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chatbot.js      # Chatbot component
│   │   │   └── Chatbot.css     # Chatbot styles
│   │   ├── css/
│   │   │   └── custom.css      # Dark theme + animations
│   │   └── theme/
│   │       └── Root.js         # Global wrapper for chatbot
│   ├── docusaurus.config.js    # Docusaurus configuration
│   ├── sidebars.js             # Sidebar navigation
│   └── package.json
│
├── backend/                     # FastAPI server
│   ├── main.py                 # API endpoints
│   ├── ingest_textbook.py      # Content ingestion script
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment template
│   └── .env                    # Your API keys (gitignored)
│
├── specs/                       # Spec-Kit Plus artifacts
│   └── physical-ai-textbook/
│       ├── spec.md             # Feature specification
│       ├── plan.md             # Architecture plan
│       └── tasks.md            # Implementation tasks
│
├── .specify/                    # Spec-Kit Plus templates
│   ├── memory/
│   │   └── constitution.md     # Project principles
│   └── templates/
│
├── CLAUDE.md                    # Claude Code instructions
├── DEMO_VIDEO_SCRIPT.md         # Demo video guide
└── README.md                    # This file
```

## Theme & Design System

### Color Palette

- **Dark gradient**: Charcoal (#1a1d23) → Slate (#2d3139)
- **Accent**: Electric cyan (#00d9ff)
- **Text**: Light gray (#e8eaed)
- **Glass panels**: Semi-transparent with blur

### Animations

- **Page transitions**: Fade + vertical motion (6-10px, 250ms)
- **Button hover**: Glow pulse + micro-scale (1.02x)
- **Card hover**: Lift (4px) + shadow bloom
- **Chatbot button**: Breathing animation (2.5s loop)

All animations are GPU-accelerated and under 300ms.

### Typography

- **Font**: Inter (system fallback to -apple-system, Segoe UI)
- **Headings**: 600 weight, -0.02em letter-spacing
- **Body**: 400 weight, 1.7 line-height

## API Endpoints

### `POST /api/query`

Query the textbook chatbot.

**Request**:
```json
{
  "question": "What is inverse kinematics?",
  "selected_text": "optional selected text from page",
  "conversation_history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

**Response**:
```json
{
  "answer": "Inverse kinematics (IK) is...",
  "sources": [
    {"chapter": "Chapter 3: Control", "section": "3.2 Kinematics", "score": 0.89}
  ],
  "context_used": "## Inverse Kinematics..."
}
```

### `POST /api/ingest`

Ingest new content into Qdrant.

**Request**:
```json
{
  "text": "Content to ingest...",
  "metadata": {
    "chapter": "Chapter X",
    "section": "Section Y"
  }
}
```

### `GET /health`

Health check endpoint.

## Deployment

### Frontend (Vercel / Netlify)

```bash
cd frontend
npm run build
# Deploy the 'build' directory
```

**Vercel**:
```bash
npm install -g vercel
vercel --prod
```

**Netlify**:
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=build
```

### Backend (Railway / Render / Fly.io)

**Railway**:
1. Push to GitHub
2. Connect repository on Railway
3. Add environment variables
4. Deploy

**Render**:
1. Create new Web Service
2. Connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

**Fly.io**:
```bash
fly launch
fly secrets set OPENAI_API_KEY=... QDRANT_URL=... QDRANT_API_KEY=...
fly deploy
```

### Environment Variables

**Backend (.env)**:
```env
OPENAI_API_KEY=sk-proj-...
QDRANT_URL=https://xyz.qdrant.io
QDRANT_API_KEY=...
QDRANT_COLLECTION_NAME=physical_ai_textbook
CORS_ORIGINS=https://your-frontend.vercel.app
```

**Frontend**:
Update `Chatbot.js` line 33 with your deployed backend URL:
```javascript
const response = await fetch('https://your-backend.railway.app/api/query', {
```

## Demo Video

See [DEMO_VIDEO_SCRIPT.md](./DEMO_VIDEO_SCRIPT.md) for a detailed 90-second demo script with timing, transitions, and recording tips.

**Quick summary**:
- 0-10s: Landing page with dark theme
- 10-30s: Navigate chapters
- 30-55s: Ask chatbot a question
- 55-75s: Selected text Q&A
- 75-90s: Feature montage + links

## Development Workflow (Spec-Kit Plus)

This project was built using the **Spec-Kit Plus** workflow:

1. **Constitution** (`/sp.constitution`): Define project principles
2. **Specification** (`/sp.specify`): Write feature spec
3. **Planning** (`/sp.plan`): Architecture design
4. **Tasks** (`/sp.tasks`): Break down implementation
5. **Implementation** (`/sp.implement`): Execute tasks
6. **Commit & PR** (`/sp.git.commit_pr`): Git workflow

All artifacts stored in `specs/` and `.specify/`.

## Troubleshooting

### Chatbot not responding

1. Check backend is running: `curl http://localhost:8000/health`
2. Verify environment variables in `.env`
3. Check browser console for CORS errors
4. Ensure Qdrant collection has data: `python ingest_textbook.py`

### Qdrant connection errors

- Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Check cluster is active in Qdrant Cloud dashboard
- Test connection: `curl -H "api-key: YOUR_KEY" https://your-cluster.qdrant.io/collections`

### Docusaurus build errors

- Delete `node_modules` and `.docusaurus` cache: `rm -rf node_modules .docusaurus`
- Reinstall: `npm install`
- Clear cache: `npm run clear`

### Theme not loading

- Hard refresh browser: Ctrl+Shift+R (Windows) / Cmd+Shift+R (Mac)
- Check `custom.css` is imported in `docusaurus.config.js`
- Verify CSS variables in `:root` selector

## Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m 'Add my feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- **Claude Code**: AI agent for development
- **Spec-Kit Plus**: Spec-driven development workflow
- **Docusaurus**: Static site generator
- **Qdrant**: Vector database
- **OpenAI**: Embeddings and chat models

## Links

- **Live Demo**: [your-demo-url.vercel.app]
- **GitHub**: [github.com/your-username/physical-ai-textbook]
- **Demo Video**: [youtube.com/watch?v=...]

---

**Built with Claude Code for [Hackathon Name] • 2024**
