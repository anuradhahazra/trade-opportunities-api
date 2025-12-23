# Trade Opportunities API

FastAPI backend for analyzing trade opportunities in Indian market sectors.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables (optional):
```bash
# Create .env file
API_KEY=your-api-key-here
GEMINI_API_KEY=your-gemini-key-here  # Optional
```

4. Run server:
```bash
uvicorn app.main:app --reload
```
5. Server is running on
```bash
http://127.0.0.1:8000 
```
6. You can test the API using the Swagger documentation
```bash
http://localhost:8000/docs
```

## Other Way of Usage

### Endpoint: GET /analyze/{sector}

**Headers:**
- `X-API-Key: your-api-key-here` (default: `dev-api-key-12345`)

**Example:**
```bash
curl -H "X-API-Key: dev-api-key-12345" http://localhost:8000/analyze/pharmaceuticals
```

**Response:** JSON with markdown report

## Valid Sectors

pharmaceuticals, technology, finance, automotive, retail, energy, healthcare, agriculture, manufacturing, telecommunications, real-estate, education, tourism

