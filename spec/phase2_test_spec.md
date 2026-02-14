# Phase 2 Test Specification

## Strategy
-   **Backend**: `pytest` + `TestClient` (FastAPI) + Mocked Supabase/Database.
-   **Frontend**: `jest` + `react-testing-library` (Unit/Component tests).
-   **E2E**: `Playwright` (Optional for Phase 2, but good to have eventually).

## Test Cases

### 1. Backend API (`api/tests/test_api.py`)
-   **`test_search_endpoint`**:
    -   Mock database search query.
    -   Verify correct JSON response format (list of papers).
-   **`test_calibrate_endpoint`**:
    -   Mock user interaction insert.
    -   Verify successful 200 OK response on valid paper IDs.
-   **`test_feed_endpoint`**:
    -   Mock user interaction retrieval (starred papers).
    -   Mock embedding calculation (mean of starred).
    -   Mock similarity search.
    -   Verify returns list of recommended papers.

### 2. Frontend Components (`web/tests/`)
-   **`PaperCard.test.tsx`**:
    -   Render card with dummy props.
    -   Click "Star" button -> verify callback fired.
-   **`SearchBar.test.tsx`**:
    -   Type into input -> verify `onChange` / search trigger.

### 3. Integration Checks
-   **Migration Script**: Run `migrate_to_supabase.py` against a local dockerized Supabase (or mock) to ensure data integrity.
