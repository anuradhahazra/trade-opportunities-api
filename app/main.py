from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from datetime import datetime
from typing import Annotated

from app.config import settings
from app.models import AnalyzeResponse, ErrorResponse
from app.auth import verify_api_key
from app.rate_limiter import rate_limiter
from app.session_manager import session_manager
from app.data_fetcher import fetch_india_market_data
from app.analyzer import analyze_with_llm

app = FastAPI(
    title="Trade Opportunities API",
    description="API for analyzing trade opportunities in Indian market sectors",
    version="1.0.0"
)

# Valid sectors (can be expanded)
VALID_SECTORS = [
    "pharmaceuticals", "technology", "finance", "automotive",
    "retail", "energy", "healthcare", "agriculture", "manufacturing",
    "telecommunications", "real-estate", "education", "tourism"
]

def validate_sector(sector: str) -> str:
    """Validate and normalize sector name"""
    sector_lower = sector.lower().strip()
    sector_normalized = sector_lower.replace(" ", "-").replace("_", "-")
    
    # Check if exact match
    if sector_normalized in VALID_SECTORS:
        return sector_normalized
    
    # Check if partial match
    for valid_sector in VALID_SECTORS:
        if valid_sector in sector_normalized or sector_normalized in valid_sector:
            return valid_sector
    
    # If no match, return normalized version (allow flexibility)
    return sector_normalized

@app.get("/", response_class=PlainTextResponse)
async def root():
    """Health check endpoint"""
    return "Trade Opportunities API - Health Check OK"

@app.get(
    "/analyze/{sector}",
    response_model=AnalyzeResponse,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        422: {"model": ErrorResponse}
    }
)
async def analyze_sector(
    sector: str,
    api_key: Annotated[str, Depends(verify_api_key)]
):
    """
    Analyze trade opportunities for a given sector in India
    
    - **sector**: Sector name (e.g., pharmaceuticals, technology)
    - Returns structured markdown report with market analysis
    """
    try:
        # Validate sector
        validated_sector = validate_sector(sector)
        
        # Check rate limit
        is_allowed, remaining = rate_limiter.check_rate_limit(api_key)
        if not is_allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_WINDOW} seconds."
            )
        
        # Get or create session
        session_id = session_manager.get_or_create_session(api_key)
        session_manager.track_analysis(session_id, validated_sector)
        
        # Fetch market data
        market_data = await fetch_india_market_data(validated_sector)
        
        # Analyze with LLM
        report = await analyze_with_llm(validated_sector, market_data)
        
        # Cleanup expired sessions periodically
        session_manager.cleanup_expired()
        
        return AnalyzeResponse(
            sector=validated_sector,
            report=report,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/health")
async def health():
    """Health check with system status"""
    return {
        "status": "healthy",
        "rate_limit": {
            "max_requests": settings.RATE_LIMIT_REQUESTS,
            "window_seconds": settings.RATE_LIMIT_WINDOW
        },
        "sessions_active": len(session_manager.sessions)
    }

