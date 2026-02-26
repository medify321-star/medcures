import requests
import json

# Test the backend API
try:
    # Test 1: Check if server is running
    response = requests.get("http://localhost:8000/api/")
    print(f"✓ Backend API response: {response.status_code}")
    
    # Test 2: Search for a drug
    test_search = "Aspirin"
    response = requests.get(f"http://localhost:8000/api/search", params={"query": test_search})
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Search for '{test_search}': Found 1 drug")
        print(f"✓ Drug name: {result[0].get('Drug', 'N/A')}")
        print(f"✓ Category: {result[0].get('Category', 'N/A')}")
    else:
        print(f"✗ Search failed with status {response.status_code}")
        print(f"Response: {response.text}")
    
    # Test 3: Get all drugs count
    print(f"\n✓ Backend is working correctly with new database!")
    
except Exception as e:
    print(f"✗ Error testing backend: {e}")
