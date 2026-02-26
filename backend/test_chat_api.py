import requests
import json

# Test the backend chat API
try:
    # Test 1: Check if server is running
    response = requests.get("http://localhost:8000/api/")
    print(f"✓ Backend API response: {response.status_code}")
    
    # Test 2: Send a chat message asking about a drug
    chat_payload = {
        "message": "Tell me about Aspirin"
    }
    response = requests.post("http://localhost:8000/api/chat/send", json=chat_payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Chat API returned: {response.status_code}")
        print(f"✓ Response length: {len(result.get('response', ''))} characters")
        print(f"✓ Session ID created: {result.get('session_id', 'N/A')[:8]}...")
        print(f"\n📝 Sample response (first 200 chars):")
        print(result.get('response', '')[:200])
    else:
        print(f"✗ Chat API failed with status {response.status_code}")
        print(f"Error: {response.text}")
    
except Exception as e:
    print(f"✗ Error testing backend: {e}")
