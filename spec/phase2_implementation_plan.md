# Phase 2 Implementation Plan: The Web MVP

## Goal
Transform the local CLI tool into a web application with user authentication, a fresh paper feed, and a calibration workflow.

## Architecture

### 1. Technology Stack
-   **Frontend**: Next.js 14+ (App Router), Shadcn UI, Tailwind CSS.
-   **Backend**: FastAPI (Python) - wraps our existing `src` logic.
-   **Database**: Supabase (PostgreSQL + `pgvector`).
-   **Auth**: Clerk (integrated with Next.js).
-   **Infrastructure**:
    -   Frontend: Vercel (or local for now).
    -   Backend: Local (future: Modal/Railway).
    -   DB: Supabase Cloud.

### 2. Data Migration
Move from `data/papers.json` and `data/embeddings.npy` to Supabase.
-   **Table `papers`**:
    -   `id` (text, primary key - arXiv ID)
    -   `title` (text)
    -   `abstract` (text)
    -   `embedding` (vector(384))
    -   `url` (text)
    -   `authors` (text[])
    -   `categories` (text[])
    -   `date` (timestamp)
-   **Table `user_interactions`**:
    -   `id` (uuid, primary key)
    -   `user_id` (text, from Clerk)
    -   `paper_id` (fk to papers)
    -   `interaction_type` (text: 'star', 'ignore', 'click')
    -   `created_at` (timestamp)

### 3. Backend (FastAPI)
Expose endpoints for the frontend:
-   `GET /api/v1/search?q=...` -> Semantic search using Supabase `pgvector`.
-   `POST /api/v1/calibrate` -> Accepts list of paper IDs, trains/updates user profile (simple centroid or linear classifier).
-   `GET /api/v1/feed` -> Returns personalized recommendations (based on starred papers).

### 4. Frontend (Next.js)
-   **Pages**:
    -   `/` (Landing + Login).
    -   `/calibration` (Onboarding: Search & Star 5 papers).
    -   `/feed` (Main Dashboard).
-   **Components**:
    -   `PaperCard`: Title, Abstract, "Star/Dismiss" buttons.
    -   `SearchBar`: Main input for calibration.

## Step-by-Step Implementation

1.  **Database Setup**:
    -   Create Supabase project (manually or via CLI).
    -   Run migration script to create tables.
    -   Write script `src/migrate_to_supabase.py` to push local JSON/NPY to Supabase.
2.  **Backend API**:
    -   Create `api/` directory.
    -   Implement FastAPI app with `paper` and `user` routers.
    -   Connect to Supabase using `supabase-py` or direct PostgreSQL connection (`psycopg` + `pgvector`).
3.  **Frontend Setup**:
    -   Initialize Next.js app in `web/`.
    -   Install Shadcn UI.
    -   Setup Clerk Auth.
4.  **Calibration UI**:
    -   Build search interface hitting the FastAPI backend.
    -   Connect "Star" action to `user_interactions` table.
5.  **Feed Logic**:
    -   Implement "More like starred" logic (simple mean embedding search for MVP).

## Directory Structure Update
```
resurch/
├── api/                # [NEW] FastAPI Backend
│   ├── main.py
│   └── ...
├── web/                # [NEW] Next.js Frontend
│   ├── src/app/
│   └── ...
├── src/                # Existing Core Logic (Ingest/Embed)
├── spec/
│   ├── phase2_implementation_plan.md
│   └── phase2_test_spec.md
└── ...
```
