# Phase 3 Implementation Plan: Automated Infrastructure & Serve

## Goal
Deploy the "resurch" web MVP to the cloud to make it publicly accessible and automate the daily ingestion of new papers.

## 1. Hosting Strategy (Free Tier Optimized)

| Component | Platform | Configuration |
| :--- | :--- | :--- |
| **Frontend** | **Vercel** | - Framework: Next.js<br>- Environment Variables: `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` |
| **Backend** | **Render** | - Type: Web Service (Python)<br>- Build Command: `pip install -r api/requirements.txt`<br>- Start Command: `uvicorn api.main:app --host 0.0.0.0 --port 10000`<br>- Environment Variables: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `HF_HOME` (cache) |
| **Database** | **Supabase** | - Existing cloud instance (already remote). |
| **Auth** | **Clerk** | - Add Production URL to Clerk allowed domains. |

## 2. Embedding Strategy (CPU Constraints)
User raised a valid concern about generating embeddings on CPU (Render/GitHub Actions).
- **Model**: `all-MiniLM-L6-v2`
- **Size**: ~80MB (Very small).
- **Inference Speed**: ~10ms per sentence on modern CPU.
- **Memory**: Requires ~300MB RAM.
- **Verdict**: Acceptable for Free Tier (512MB RAM on Render).
- **Optimization**: We will load the model *globally* (already done) to keep it in memory.

## 3. Implementation Steps

### A. Backend Deployment (Render)
1.  [ ] Create `render.yaml` (Infrastructure as Code) to define the web service.
2.  [ ] User connects GitHub repo to Render.
3.  [ ] Configure Environment Variables in Render Dashboard.
4.  [ ] Verify `/api/health` endpoint.

### B. Frontend Deployment (Vercel)
1.  [ ] User connects GitHub repo to Vercel.
2.  [ ] Add `NEXT_PUBLIC_API_URL`.
3.  [ ] Update Clerk "Allowed Origins".

### C. Daily Ingestion (GitHub Actions)
1.  [ ] Create `.github/workflows/daily_ingest.yml`.
2.  [ ] Schedule: `cron: '0 8 * * *'` (8 AM UTC daily).
3.  [ ] Action will install dependencies, run `ingest_arxiv.py`, generate embeddings (CPU), and push to Supabase.

## 4. Verification
- [ ] Visit Vercel URL -> Login -> Calibration -> Feed.
- [ ] Check Render logs for successful startup (and cold start delay).
- [ ] Manually trigger GitHub Action to verify ingestion.
