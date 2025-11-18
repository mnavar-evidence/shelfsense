"""Quick test script for ShelfSense MCP Server"""
import asyncio
import os
import sys
from server import ShelfSenseClient


async def test_mcp_client(api_url):
    """Test MCP client connection to API"""
    print(f"Testing ShelfSense MCP Client with API at {api_url}\n")

    client = ShelfSenseClient(api_url)

    tests = [
        ("Get Locations", client.get_locations()),
        ("Get Products", client.get_products()),
        ("Get Pick List", client.get_pick_list("loc_westin_sf")),
        ("Get Analytics", client.get_analytics_summary()),
    ]

    passed = 0
    failed = 0

    for name, coro in tests:
        try:
            result = await coro
            if result:
                print(f"✅ {name}: OK ({type(result).__name__})")
                passed += 1
            else:
                print(f"❌ {name}: No data returned")
                failed += 1
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")

    if failed == 0:
        print("\n🎉 All tests passed! MCP client is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the API server connection.")
        return 1


if __name__ == "__main__":
    api_url = sys.argv[1] if len(sys.argv) > 1 else os.getenv("SHELFSENSE_API_URL", "http://localhost:8000")
    exit_code = asyncio.run(test_mcp_client(api_url))
    sys.exit(exit_code)
