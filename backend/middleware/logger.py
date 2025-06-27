from flask import request, g
import time
from datetime import datetime


def logger():
    """Logger middleware for Flask"""
    def log_request():
        g.start_time = time.time()
        
    def log_response(response):
        # Calculate duration
        duration = time.time() - g.start_time if hasattr(g, 'start_time') else 0
        duration_ms = round(duration * 1000, 2)
        
        # Get response message if it's JSON
        response_message = "N/A"
        try:
            if response.is_json:
                response_data = response.get_json()
                if response_data and isinstance(response_data, dict):
                    response_message = response_data.get("message", "N/A")
        except:
            pass
        
        # Log the request
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] {request.method} {request.url} {response.status_code} {response_message} - {duration_ms}ms")
        
        return response
    
    return log_request, log_response