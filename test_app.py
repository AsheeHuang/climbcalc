#!/usr/bin/env python3
import requests
import json

def test_api():
    base_url = "http://127.0.0.1:5000"
    
    # Test locations endpoint
    print("Testing /api/locations...")
    response = requests.get(f"{base_url}/api/locations")
    if response.status_code == 200:
        locations = response.json()
        print(f"✓ Found {len(locations)} locations")
        print(f"Sample locations: {locations[:5]}")
    else:
        print("✗ Failed to get locations")
        return
    
    # Test calculate endpoint
    print("\nTesting /api/calculate...")
    test_data = {
        "start": "水里",
        "end": "玉山主峰"
    }
    
    response = requests.post(
        f"{base_url}/api/calculate",
        headers={"Content-Type": "application/json"},
        data=json.dumps(test_data)
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Path found from {test_data['start']} to {test_data['end']}")
        print(f"Time: {result['time_formatted']}")
        print(f"Path: {' → '.join(result['path'])}")
    else:
        print("✗ Failed to calculate path")
        print(response.json())

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Flask app. Make sure it's running on http://127.0.0.1:5000")