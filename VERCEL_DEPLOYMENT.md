# Vercel Deployment Guide

## Quick Deploy (Recommended)

### Option 1: Deploy via Vercel Dashboard

1. **Go to Vercel**: https://vercel.com
2. **Sign in** with your GitHub account
3. **Click "Add New Project"**
4. **Import your repository**: `Awais-khan-sys/Physical-ai-book-humanid`
5. **Configure Project**:
   - **Framework Preset**: Other (Docusaurus will be detected automatically)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`

6. **Environment Variables** (Add these in Vercel dashboard):
   ```
   REACT_APP_API_URL=https://your-backend-url.railway.app
   ```
   *(You'll update this after deploying the backend)*

7. **Click "Deploy"**

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend directory
cd frontend

# Login to Vercel
vercel login

# Deploy to production
vercel --prod

# Follow the prompts:
# - Link to existing project? No
# - Project name: physical-ai-textbook
# - Directory: ./
# - Override settings? No
```

## Backend Deployment (Railway)

Before your frontend works properly, deploy the backend:

### Railway Deployment

1. **Go to Railway**: https://railway.app
2. **Sign in** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Select**: `Awais-khan-sys/Physical-ai-book-humanid`
5. **Settings**:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Watch Paths**: `backend/**`

6. **Add Environment Variables** (use your actual values from backend/.env):
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   QDRANT_URL=your_qdrant_cluster_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_COLLECTION_NAME=textbook_chunks
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

7. **Deploy** and copy the Railway URL (e.g., `https://physical-ai-backend.railway.app`)

8. **Run Ingestion** (one-time):
   - SSH into Railway or run locally:
   ```bash
   cd backend
   python ingest_textbook.py
   ```

### Update Frontend with Backend URL

After backend is deployed:

1. Go to Vercel dashboard → Your project → Settings → Environment Variables
2. Update `REACT_APP_API_URL` to your Railway backend URL
3. Redeploy frontend

## Automated Deployment Script

Run this after both services are deployed:

```bash
# Update backend URL in frontend
cd frontend
echo "REACT_APP_API_URL=https://your-backend.railway.app" > .env.production

# Commit and push (triggers auto-deploy)
git add .env.production
git commit -m "config: Add production backend URL"
git push origin master
```

## Verification Checklist

After deployment:

- [ ] Frontend is accessible at Vercel URL
- [ ] Backend health check works: `curl https://your-backend.railway.app/health`
- [ ] Qdrant has data: Check collection in Qdrant dashboard
- [ ] Chatbot button appears on frontend
- [ ] Chatbot responds to questions
- [ ] Selected text Q&A works
- [ ] No CORS errors in browser console

## Troubleshooting

### Frontend Issues

**Build fails**:
- Check Node version (need 18+)
- Try: `cd frontend && rm -rf node_modules .docusaurus && npm install`

**Chatbot not working**:
- Verify `REACT_APP_API_URL` is set correctly
- Check browser console for CORS errors
- Ensure backend CORS allows your Vercel domain

### Backend Issues

**Ingestion fails**:
- Check Qdrant credentials
- Verify collection exists: `curl https://your-qdrant-url/collections`
- Check OpenAI API key is valid

**Slow responses**:
- Normal for first request (cold start)
- Consider upgrading Railway plan for always-on

### CORS Errors

Update backend CORS in Railway:
```
CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
```

## Production URLs

After deployment, update these in your README:

- **Frontend**: `https://physical-ai-textbook.vercel.app` (example)
- **Backend**: `https://physical-ai-backend.railway.app` (example)
- **GitHub**: https://github.com/Awais-khan-sys/Physical-ai-book-humanid

## Cost Estimate

- **Vercel**: Free (Hobby plan)
- **Railway**: Free tier ($5 credit/month)
- **Qdrant Cloud**: Free tier (1GB)
- **OpenAI**: Pay-as-you-go (~$0.01 per query)

**Total**: ~$0-5/month for moderate usage

## Performance Optimization

After deployment:

1. **Enable Caching**: Add to `vercel.json`:
   ```json
   {
     "headers": [
       {
         "source": "/static/(.*)",
         "headers": [
           {
             "key": "Cache-Control",
             "value": "public, max-age=31536000, immutable"
           }
         ]
       }
     ]
   }
   ```

2. **Add Edge Functions**: For better global performance

3. **Monitor Usage**: Set up alerts in Railway and Vercel

## Security Notes

- ✅ API keys in environment variables (not in code)
- ✅ CORS properly configured
- ✅ .gitignore excludes .env files
- ⚠️ Consider rate limiting on backend
- ⚠️ Add authentication for production use

## Next Steps

1. Deploy backend to Railway
2. Run ingestion script
3. Deploy frontend to Vercel
4. Update frontend with backend URL
5. Test end-to-end
6. Update README with live URLs
7. Create demo video
8. Submit to hackathon!

---

**Need Help?**
- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- Issues: https://github.com/Awais-khan-sys/Physical-ai-book-humanid/issues
