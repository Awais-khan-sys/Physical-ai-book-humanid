# Quick Setup Guide

## Step-by-Step Instructions

### 1. Install Dependencies

**Frontend:**
```bash
cd frontend
npm install
```

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `backend/.env`:
```env
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=YOUR_QDRANT_KEY_HERE
QDRANT_COLLECTION_NAME=physical_ai_textbook
CORS_ORIGINS=http://localhost:3000
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Qdrant: https://cloud.qdrant.io/ (free tier available)

### 3. Start Backend

```bash
cd backend
python main.py
```

Backend will run at: http://localhost:8000

### 4. Ingest Textbook Content

In a new terminal:
```bash
cd backend
python ingest_textbook.py
```

Wait for completion (~2-3 minutes for 5 chapters).

### 5. Start Frontend

In a new terminal:
```bash
cd frontend
npm start
```

Frontend will run at: http://localhost:3000

### 6. Test Everything

1. Open http://localhost:3000
2. Click the floating chatbot button (bottom-right)
3. Ask: "What is Physical AI?"
4. Select text on the page, ask: "Explain this"

## Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (need 3.11+)
- Verify all packages installed: `pip list`

**Qdrant connection errors:**
- Double-check URL and API key in `.env`
- Ensure cluster is active in Qdrant dashboard

**Frontend build errors:**
- Delete node_modules: `rm -rf node_modules`
- Reinstall: `npm install`

**Chatbot not responding:**
- Verify backend is running: `curl http://localhost:8000/health`
- Check browser console for errors (F12)
- Ensure CORS is configured correctly

## Production Deployment

### Frontend → Vercel
```bash
cd frontend
npm run build
vercel --prod
```

### Backend → Railway
1. Push to GitHub
2. Create new project on Railway
3. Connect GitHub repo
4. Add environment variables
5. Deploy

Update `frontend/src/components/Chatbot.js` line 33 with your deployed backend URL.

## Need Help?

- Check README.md for detailed documentation
- Review DEMO_VIDEO_SCRIPT.md for usage examples
- Open an issue on GitHub
