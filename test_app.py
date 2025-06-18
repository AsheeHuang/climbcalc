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
    
    # Test calculate endpoint with segment times
    print("\nTesting /api/calculate...")
    test_cases = [
        {"start": "水里", "end": "和社"},
        {"start": "水里", "end": "排雲管理站"}
    ]
    
    for test_data in test_cases:
        print(f"\nTesting route: {test_data['start']} → {test_data['end']}")
        response = requests.post(
            f"{base_url}/api/calculate",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Path found from {test_data['start']} to {test_data['end']}")
            print(f"Total Time: {result['time_formatted']} ({result['time']} minutes)")
            print(f"Path: {' → '.join(result['path'])}")
            
            # Test segment times
            if 'segment_times' in result and 'segment_times_formatted' in result:
                print("✓ Segment times included in response")
                print(f"Segment times: {result['segment_times']} minutes")
                print(f"Formatted: {result['segment_times_formatted']}")
                
                # Verify segment times sum to total time
                if sum(result['segment_times']) == result['time']:
                    print("✓ Segment times sum correctly to total time")
                else:
                    print(f"✗ Segment times sum ({sum(result['segment_times'])}) != total time ({result['time']})")
            else:
                print("✗ Segment times missing from response")
        else:
            print(f"✗ Failed to calculate path: {response.json()}")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Flask app. Make sure it's running on http://127.0.0.1:5000")