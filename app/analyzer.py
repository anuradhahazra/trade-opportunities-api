import os
import httpx
from typing import Dict, Optional
from app.config import settings

async def analyze_with_llm(sector: str, market_data: Dict) -> str:
    """
    Analyze market data using Google Gemini API
    Falls back to mock analysis if API key not available
    """
    api_key = settings.GEMINI_API_KEY
    
    if not api_key:
        return _generate_mock_analysis(sector, market_data)
    
    try:
        # Prepare prompt
        headlines = "\n".join([f"- {h}" for h in market_data.get("headlines", [])])
        snippets = "\n".join([f"- {s}" for s in market_data.get("snippets", [])])
        
        prompt = f"""Analyze the following India-specific market data for the {sector} sector and generate a structured markdown report.

Headlines:
{headlines}

News Snippets:
{snippets}

Generate a comprehensive markdown report with the following sections:
1. Executive Summary
2. Market Overview
3. Key Trends
4. Opportunities
5. Risks
6. Recommendations

Focus on India-specific insights and trade opportunities."""

        # Call Gemini API
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            response = await client.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
                    return content
        
        # Fallback to mock if API call fails
        return _generate_mock_analysis(sector, market_data)
    
    except Exception as e:
        # Fallback to mock on error
        return _generate_mock_analysis(sector, market_data)

def _generate_mock_analysis(sector: str, market_data: Dict) -> str:
    """Generate mock analysis when Gemini API is not available"""
    headlines = market_data.get("headlines", [])
    snippets = market_data.get("snippets", [])
    
    report = f"""# Trade Opportunities Analysis: {sector.title()} Sector (India)

## Executive Summary

The {sector} sector in India shows promising growth potential with increasing market activity and regulatory support. Recent developments indicate strong investor interest and expanding market opportunities.

## Market Overview

Based on recent market data:
"""
    
    if headlines:
        report += "\n### Recent Headlines\n"
        for headline in headlines[:3]:
            report += f"- {headline}\n"
    
    if snippets:
        report += "\n### Key Insights\n"
        for snippet in snippets[:3]:
            report += f"- {snippet}\n"
    
    report += f"""
## Key Trends

1. **Market Growth**: The {sector} sector in India is experiencing steady growth driven by domestic demand and export opportunities.
2. **Regulatory Environment**: Favorable government policies are supporting sector development.
3. **Investment Activity**: Increased foreign and domestic investment in the sector.

## Opportunities

1. **Domestic Market Expansion**: Growing middle-class consumption creates opportunities for market penetration.
2. **Export Potential**: India's competitive advantage in {sector} presents export opportunities.
3. **Technology Integration**: Digital transformation offers efficiency gains and new business models.
4. **Infrastructure Development**: Government infrastructure projects create demand for {sector} products/services.

## Risks

1. **Regulatory Changes**: Potential policy shifts could impact sector dynamics.
2. **Market Volatility**: Economic fluctuations may affect demand patterns.
3. **Competition**: Increasing competition from domestic and international players.
4. **Supply Chain**: Dependencies on global supply chains may pose risks.

## Recommendations

1. **Short-term**: Monitor regulatory updates and market sentiment closely.
2. **Medium-term**: Focus on building strong distribution networks and partnerships.
3. **Long-term**: Invest in technology and innovation to maintain competitive edge.

---
*Report generated based on market data analysis. This is a mock analysis for demonstration purposes.*
"""
    
    return report

