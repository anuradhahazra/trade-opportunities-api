# Project Notes

## Commands Executed

- `python -m venv venv` - Create virtual environment
- `pip install -r requirements.txt` - Install dependencies (FastAPI, uvicorn, httpx, python-dotenv, pydantic)
- `python main.py` or `uvicorn app.main:app --reload` - Run FastAPI server on port 8000

## File Structure

- `main.py` - Entry point, runs uvicorn server
- `app/main.py` - FastAPI application with /analyze/{sector} endpoint
- `app/config.py` - Settings (API keys, rate limits, timeouts)
- `app/models.py` - Pydantic models for request/response validation
- `app/auth.py` - API key authentication via X-API-Key header
- `app/rate_limiter.py` - In-memory rate limiting (10 requests per 60 seconds)
- `app/session_manager.py` - In-memory session tracking with timeout
- `app/data_fetcher.py` - Fetches India market data via DuckDuckGo search
- `app/analyzer.py` - LLM analysis using Google Gemini API (falls back to mock if key missing)
- `requirements.txt` - Python dependencies
- `README.md` - Setup and usage instructions

## Authentication

- Header-based: `X-API-Key` header required
- Default key: `dev-api-key-12345` (set via API_KEY env var)
- Returns 401 if missing, 403 if invalid

## Rate Limiting

- In-memory storage per API key
- Default: 10 requests per 60 seconds
- Returns 429 when exceeded
- Configurable via RATE_LIMIT_REQUESTS and RATE_LIMIT_WINDOW in config

## AI Usage

- Primary: Google Gemini API (gemini-pro model)
- Requires GEMINI_API_KEY environment variable
- Falls back to mock analysis if key missing or API fails
- Generates structured markdown report with sections: Executive Summary, Market Overview, Trends, Opportunities, Risks, Recommendations

## How to Run

1. Activate venv: `venv\Scripts\activate`
2. Install: `pip install -r requirements.txt`
3. (Optional) Create `.env` with API_KEY and GEMINI_API_KEY
4. Run: `python main.py`
5. Test: `curl -H "X-API-Key: dev-api-key-12345" http://localhost:8000/analyze/pharmaceuticals`

