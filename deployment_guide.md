# Deployment Guide for "Resurch"

Use this guide to deploy your Web MVP to the cloud.

## Prerequisites
- [ ] Push all your latest code to GitHub (including the new `render.yaml` and `.github` folder).

## 1. Deploy Backend (Render)
1.  Go to [dashboard.render.com](https://dashboard.render.com).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository `resurch`.
4.  Render might auto-detect `render.yaml`. If so, click **Apply**.
5.  If not asked for `render.yaml`, configure manually:
    *   **Name**: `resurch-api`
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r api/requirements.txt`
    *   **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port 10000`
6.  **Environment Variables** (Critical):
    *   `SUPABASE_URL`: (Copy from your local `.env`)
    *   `SUPABASE_SERVICE_KEY`: (Copy from your local `.env`)
    *   `PYTHON_VERSION`: `3.9.0` (Render defaults to 3.7 sometimes)
7.  Click **Create Web Service**.
8.  **Wait**: It will take a few minutes. Once done, copy your backend URL (e.g., `https://resurch-api.onrender.com`).

## 2. Deploy Frontend (Vercel)
1.  Go to [vercel.com/new](https://vercel.com/new).
2.  Import your `resurch` GitHub repository.
3.  **Framework Preset**: Select `Next.js`.
4.  **Root Directory**: Click "Edit" and select `web` folder.
5.  **Environment Variables**:
    *   `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`: (Copy from `web/.env.local`)
    *   `CLERK_SECRET_KEY`: (Copy from `web/.env.local` - optional for frontend deploy but good for API routes)
    *   `NEXT_PUBLIC_API_URL`: **Paste your Render Backend URL here** (no trailing slash).
6.  Click **Deploy**.

## 3. Final Configuration
1.  **Clerk (Important Correction)**:
    *   **Stay in Development Mode**: It turns out Clerk **requires** a custom top-level domain (like `.com`) for Production instances. Since we are using a free `vercel.app` subdomain, we must stick to the **"Development"** instance.
    *   **Impact**: Your Vercel app will work perfectly, but you will see a "Development Mode" banner at the bottom of the screen. This is normal for free-tier MVPs.
    *   **Action**: Ensure your **Vercel Environment Variables** are using the **Development Keys** (starting with `pk_test_...` and `sk_test_...`), NOT production keys.
2.  **Supabase**: Go to Supabase Dashboard -> **Authentication** -> **URL Configuration**. Add your Vercel domain (e.g. `https://resurch.vercel.app`) to "Site URL" and "Redirect URLs".

## 4. Daily Automation (GitHub Actions)
1.  Go to your GitHub Repo -> **Settings** -> **Secrets and variables** -> **Actions**.
2.  Add New Repository Secret:
    *   `SUPABASE_URL`
    *   `SUPABASE_SERVICE_KEY`
3.  Go to the **Actions** tab in GitHub and verify the "Daily ArXiv Ingestion" workflow is listed. You can manually run it to test.
