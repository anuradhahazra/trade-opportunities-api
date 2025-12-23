import time
from typing import Dict, Optional
from datetime import datetime

class SessionManager:
    def __init__(self, timeout: int = 3600):
        self.sessions: Dict[str, dict] = {}
        self.timeout = timeout
    
    def get_or_create_session(self, api_key: str) -> str:
        """Get existing session or create new one for API key"""
        session_id = f"session_{api_key[:8]}"
        
        if session_id in self.sessions:
            session = self.sessions[session_id]
            if time.time() - session['last_activity'] < self.timeout:
                session['last_activity'] = time.time()
                session['request_count'] += 1
                return session_id
        
        # Create new session
        self.sessions[session_id] = {
            'api_key': api_key,
            'created_at': time.time(),
            'last_activity': time.time(),
            'request_count': 1,
            'sectors_analyzed': []
        }
        return session_id
    
    def track_analysis(self, session_id: str, sector: str):
        """Track sector analysis for session"""
        if session_id in self.sessions:
            if sector not in self.sessions[session_id]['sectors_analyzed']:
                self.sessions[session_id]['sectors_analyzed'].append(sector)
    
    def get_session_info(self, session_id: str) -> Optional[dict]:
        """Get session information"""
        return self.sessions.get(session_id)
    
    def cleanup_expired(self):
        """Remove expired sessions"""
        current_time = time.time()
        expired = [
            sid for sid, session in self.sessions.items()
            if current_time - session['last_activity'] >= self.timeout
        ]
        for sid in expired:
            del self.sessions[sid]

session_manager = SessionManager()

