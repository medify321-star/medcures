#!/usr/bin/env python
"""
Simple test server to verify database and drug search functionality
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from pathlib import Path

# Load drugs database
with open('pharmacopoeia.json', 'r', encoding='utf-8') as f:
    DRUGS = json.load(f)

class DrugsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/api/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "Medcures API is running",
                "total_drugs": len(DRUGS),
                "first_drug": DRUGS[0]["name"] if DRUGS else None
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif parsed_path.path == '/api/drugs':
            # Return all drugs
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"drugs": DRUGS, "count": len(DRUGS)}).encode())
            
        elif parsed_path.path.startswith('/api/search'):
            # Search for a drug
            query_params = urllib.parse.parse_qs(parsed_path.query)
            query = query_params.get('q', query_params.get('query', ['']))[0].lower()
            
            results = []
            if query:
                for drug in DRUGS:
                    if query in drug["name"].lower():
                        results.append(drug)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"query": query, "results": results, "count": len(results)}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress default logging

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), DrugsHandler)
    print(f"✓ Simple test server started on http://localhost:8000")
    print(f"✓ Database loaded: {len(DRUGS)} drugs")
    print(f"✓ Endpoints:")
    print(f"  - GET /api/ - Server status")
    print(f"  - GET /api/drugs - All drugs")
    print(f"  - GET /api/search?q=aspirin - Search drugs")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
