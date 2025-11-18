"""Quick test script for ShelfSense Mock API"""
import requests
import sys


def test_api(base_url="http://localhost:8000"):
    """Test basic API endpoints"""
    print(f"Testing ShelfSense Mock API at {base_url}\n")

    tests = [
        ("Health Check", f"{base_url}/health"),
        ("Root", f"{base_url}/"),
        ("Locations", f"{base_url}/api/locations"),
        ("Products", f"{base_url}/api/products"),
        ("Pick List", f"{base_url}/api/pick-list?location_id=loc_westin_sf"),
        ("Analytics", f"{base_url}/api/analytics/summary"),
    ]

    passed = 0
    failed = 0

    for name, url in tests:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: OK")
                passed += 1
            else:
                print(f"❌ {name}: Failed (Status {response.status_code})")
                failed += 1
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")

    if failed == 0:
        print("\n🎉 All tests passed! API is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the API server.")
        return 1


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    exit_code = test_api(url)
    sys.exit(exit_code)
