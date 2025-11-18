#!/usr/bin/env python3
"""
Integration Test: Instagram Location Extraction
Tests the full workflow with real Instagram credentials stored in .env file

Success Criteria:
- Successfully authenticate with Instagram
- Extract at least 5 locations from saved posts
- Export data to CSV
"""

import os
import sys
from pathlib import Path
from instagram_location_extractor import InstagramLocationExtractor


def load_credentials():
    """Load credentials from .env file"""
    env_file = Path(__file__).parent / '.env'

    if not env_file.exists():
        print("✗ ERROR: .env file not found!")
        print(f"  Expected location: {env_file}")
        print("\nCreate a .env file with:")
        print("  INSTAGRAM_USERNAME=your_username")
        print("  INSTAGRAM_PASSWORD=your_password")
        return None, None

    credentials = {}
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    credentials[key.strip()] = value.strip()

    username = credentials.get('INSTAGRAM_USERNAME')
    password = credentials.get('INSTAGRAM_PASSWORD')

    if not username or not password:
        print("✗ ERROR: Missing credentials in .env file")
        print(f"  Found: {list(credentials.keys())}")
        return None, None

    return username, password


def run_integration_test():
    """Run the full integration test"""
    print("=" * 70)
    print("Instagram Location Extractor - Integration Test")
    print("=" * 70)

    # Load credentials
    print("\n[1/5] Loading credentials from .env file...")
    username, password = load_credentials()

    if not username or not password:
        return False

    print(f"✓ Loaded credentials for: {username}")

    # Initialize extractor
    print("\n[2/5] Initializing Instagram extractor...")
    extractor = InstagramLocationExtractor()
    print("✓ Extractor initialized")

    # Login
    print(f"\n[3/5] Logging in to Instagram as {username}...")
    if not extractor.login(username, password):
        print("✗ TEST FAILED: Could not authenticate with Instagram")
        return False

    # Extract locations
    print("\n[4/5] Extracting locations from saved posts...")
    try:
        locations = extractor.extract_locations_from_saved()
    except Exception as e:
        print(f"✗ TEST FAILED: Error during extraction: {e}")
        return False

    # Verify minimum count
    print(f"\n[5/5] Verifying results...")
    location_count = len(locations)
    minimum_required = 5

    print(f"\nResults:")
    print(f"  Locations found: {location_count}")
    print(f"  Minimum required: {minimum_required}")

    if location_count < minimum_required:
        print(f"\n✗ TEST FAILED: Only found {location_count} locations, need at least {minimum_required}")
        print("\nPossible reasons:")
        print("  - Account has fewer than 5 saved posts with location tags")
        print("  - Saved posts don't have location data")
        print("  - Instagram API restrictions")
        return False

    # Success! Export to CSV
    print(f"\n✓ SUCCESS: Found {location_count} locations (>= {minimum_required})")

    # Export test results
    print("\n[Bonus] Exporting to CSV...")
    test_output = 'test_integration_output.csv'
    extractor.export_to_csv(locations, filename=test_output)

    # Show sample locations
    print("\nSample locations found:")
    for i, loc in enumerate(locations[:5], 1):
        print(f"  {i}. {loc['name']} ({loc['latitude']}, {loc['longitude']})")

    if location_count > 5:
        print(f"  ... and {location_count - 5} more")

    print("\n" + "=" * 70)
    print("✓ INTEGRATION TEST PASSED!")
    print("=" * 70)
    return True


if __name__ == "__main__":
    print("\n🔒 Security Note: Credentials are loaded from .env (not in git)\n")

    success = run_integration_test()

    if success:
        print("\n✅ All tests passed! The Instagram location extractor is working.")
        sys.exit(0)
    else:
        print("\n❌ Test failed. Please check the errors above.")
        sys.exit(1)
