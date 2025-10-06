## EPenguin API

This document describes the public API endpoints implemented in `website/routes/api.py`.

Base path: `/api`

No authentication is required by the routes documented here (they are defined as plain `@bp.route` handlers). Responses are JSON.

### GET /api/problems

Returns a paginated list of problems with optional filters.

Query parameters
- `page` (int, optional) — page number, default: `1`.
- `count` (int, optional) — items per page, default: `20`.
- `oj` (string, optional) — filter by online judge code (e.g. `luyencode`).
- `id` (string, optional) — partial match filter on problem id (case-insensitive).
- `title` (string, optional) — partial match filter on title (case-insensitive).
- `rating_start` (int, optional) — minimum rating (inclusive).
- `rating_end` (int, optional) — maximum rating (inclusive).

Behavior
- The endpoint builds a SQLAlchemy query on `FreeProblem` and applies provided filters.
- Results are ordered by `updated_at` descending.
- Pagination is applied using `page` and `count`.

Success response (200)

{
  "ojs": ["luyencode"],
  "pages": 10,
  "problems": [
    {
      "oj": "luyencode",
      "id": "luyencode_100",
      "link": "https://luyencode.net/problem/100",
      "updated_at": "2025-10-06T12:34:56",
      "title": "Example Problem",
      "rating": 1000
    }
  ]
}

Error responses
- 500 — returned when a query parameter has an invalid type (the handler catches exceptions and returns a 500 with an error message like `{"error": "invalid type ..."}`).

Examples
- Fetch page 1 with 10 items:

    curl -s "http://localhost:5000/api/problems?page=1&count=10"

- Filter by OJ and rating range:

    curl -s "http://localhost:5000/api/problems?oj=luyencode&rating_start=800&rating_end=1200"

---

### GET /api/problem/<id>

Returns detailed information for a single problem.

Path parameters
- `id` (string) — problem id (primary key in `FreeProblem`).

Success response (200)

{
  "oj": "luyencode",
  "id": "luyencode_100",
  "link": "https://luyencode.net/problem/100",
  "updated_at": "2025-10-06T12:34:56",
  "rating": 1000,
  "title": "Example Problem",
  "description": "Full problem text...",
  "translated": "Translated text if available",
  "timelimit": "1s",
  "memorylimit": "512MB",
  "input": "Input description",
  "output": "Output description"
}

Error responses
- 404 — returned if the problem does not exist: `{"error": "Problem not exists"}`.

Example

    curl -s "http://localhost:5000/api/problem/luyencode_100"

Notes
- `updated_at` is returned from the database as a datetime-like value (the exact string format depends on how SQLAlchemy serializes the field in your environment). `rating` may be null if unknown.

---

### GET /api/problem/<id>/update

Enqueues a background job to re-fetch/update a problem. This uses the app's `scheduler` (Flask-APScheduler) and the `current_app.bots` mapping.

Path parameters
- `id` (string) — problem id.

Behavior
- The route looks up the `FreeProblem` by id. If found, it calls `scheduler.add_job(...)` with:
  - `id=problem.id`
  - `func=current_app.bots[problem.oj].fetch`
  - `kwargs={"problemid": problem.id}`
- This schedules (or immediately executes depending on scheduler config) the bot's `fetch` function to update the problem details.

Success response (200)

{"success": "Job has been added"}

Error responses
- 404 — returned if the problem does not exist: `{"error": "Problem not exists"}`.

Notes and caveats
- Ensure `current_app.bots` contains a mapping for the problem's `oj` that exposes a callable `fetch(problemid=...)`. If the bot or fetch function is misconfigured, the scheduled job may fail at runtime.
- The job id used is the problem id; adding a job with the same id may overwrite or raise depending on scheduler settings.

---

Contact / Troubleshooting
- If you don't see jobs running: check your Flask logs for prints from bots (for example `print("task!!")` in the `luyencode` bot). Also check that the Flask-APScheduler `scheduler.start()` has been called during app startup (it is in `website/__init__.py`).

If you want, I can also add a small health route `/api/_scheduler` that returns scheduled jobs and statuses.
