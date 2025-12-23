import httpx
from typing import List, Dict
import re

async def fetch_india_market_data(sector: str) -> Dict[str, List[str]]:
    """
    Fetch India-specific market/news data for given sector
    Uses DuckDuckGo search as fallback
    """
    try:
        # Search for India-specific sector news
        query = f"{sector} India market news 2024"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Use DuckDuckGo HTML search
            url = "https://html.duckduckgo.com/html/"
            params = {"q": query}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = await client.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                # Simple HTML parsing for titles and snippets
                html = response.text
                titles = re.findall(r'<a[^>]*class="result__a"[^>]*>([^<]+)</a>', html)
                snippets = re.findall(r'<a[^>]*class="result__snippet"[^>]*>([^<]+)</a>', html)
                
                # Filter for India-relevant content
                india_keywords = ['india', 'indian', 'mumbai', 'delhi', 'bse', 'nse', 'rupee', 'rs']
                filtered_titles = [
                    t for t in titles[:10]
                    if any(kw in t.lower() for kw in india_keywords)
                ] or titles[:5]
                
                filtered_snippets = [
                    s for s in snippets[:10]
                    if any(kw in s.lower() for kw in india_keywords)
                ] or snippets[:5]
                
                return {
                    "headlines": filtered_titles[:5],
                    "snippets": filtered_snippets[:5],
                    "source": "DuckDuckGo"
                }
    except Exception as e:
        pass
    
    # Fallback: Return mock data structure
    return {
        "headlines": [
            f"{sector.title()} sector shows growth in Indian market",
            f"India {sector} industry trends 2024",
            f"Recent developments in Indian {sector} sector"
        ],
        "snippets": [
            f"Indian {sector} market experiencing positive momentum",
            f"Key players in India's {sector} industry report strong performance",
            f"Regulatory updates impact {sector} sector in India"
        ],
        "source": "Mock data"
    }

