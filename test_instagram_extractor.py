#!/usr/bin/env python3
"""
Test script for Instagram Location Extractor
Creates mock data to test the CSV export functionality
"""

from instagram_location_extractor import InstagramLocationExtractor
from datetime import datetime


def test_csv_export():
    """Test the CSV export functionality with mock data"""
    print("=" * 60)
    print("Testing Instagram Location Extractor - CSV Export")
    print("=" * 60)

    # Create an instance
    extractor = InstagramLocationExtractor()

    # Create mock location data with all new fields
    mock_locations = [
        {
            'name': 'Golden Gate Bridge',
            'latitude': 37.8199,
            'longitude': -122.4783,
            'post_url': 'https://www.instagram.com/p/TEST001/',
            'date': '2024-01-15 10:30:00',
            'caption': 'Beautiful morning walk across the bridge! Check out more at https://example.com/sf-trip',
            'caption_urls': 'https://example.com/sf-trip',
            'hashtags': '#sanfrancisco #goldengatebridge #travel',
            'mentions': '@travel_buddy @photography_lover',
            'owner_username': 'traveler123',
            'likes': 245,
            'comments': 18,
            'is_video': False,
            'video_url': ''
        },
        {
            'name': 'Times Square',
            'latitude': 40.7580,
            'longitude': -73.9855,
            'post_url': 'https://www.instagram.com/p/TEST002/',
            'date': '2024-02-20 18:45:00',
            'caption': 'The city that never sleeps ✨ Full blog post: https://myblog.com/nyc-nights #nyc #timessquare',
            'caption_urls': 'https://myblog.com/nyc-nights',
            'hashtags': '#nyc #timessquare',
            'mentions': '',
            'owner_username': 'cityexplorer',
            'likes': 532,
            'comments': 43,
            'is_video': False,
            'video_url': ''
        },
        {
            'name': 'Grand Canyon National Park',
            'latitude': 36.1069,
            'longitude': -112.1129,
            'post_url': 'https://www.instagram.com/p/TEST003/',
            'date': '2024-03-10 14:20:00',
            'caption': 'Absolutely breathtaking views! Nature at its finest. This is a much longer caption that goes into detail about the entire hiking experience, the weather conditions, the wildlife we saw along the trail, and all the amazing memories we made during this incredible adventure at one of the most spectacular natural wonders in the world.',
            'caption_urls': '',
            'hashtags': '#grandcanyon #hiking #nature #adventure',
            'mentions': '@hiking_partner',
            'owner_username': 'nature_lover_99',
            'likes': 789,
            'comments': 56,
            'is_video': False,
            'video_url': ''
        },
        {
            'name': 'Space Needle',
            'latitude': 47.6205,
            'longitude': -122.3493,
            'post_url': 'https://www.instagram.com/p/TEST004/',
            'date': '2024-04-05 12:00:00',
            'caption': 'Seattle skyline from the top 🌆 Amazing 360° views! Video tour: https://youtube.com/watch?v=example',
            'caption_urls': 'https://youtube.com/watch?v=example',
            'hashtags': '#seattle #spaceneedle #skyline',
            'mentions': '@seattle_tourism',
            'owner_username': 'pacific_nw_adventures',
            'likes': 421,
            'comments': 29,
            'is_video': True,
            'video_url': 'https://instagram.com/reel/TEST004/video.mp4'
        },
        {
            'name': 'Statue of Liberty',
            'latitude': 40.6892,
            'longitude': -74.0445,
            'post_url': 'https://www.instagram.com/p/TEST005/',
            'date': '2024-05-18 16:30:00',
            'caption': 'Icon of freedom and democracy 🗽 Read the full history: https://nps.gov/stli https://example.com/liberty-facts',
            'caption_urls': 'https://nps.gov/stli, https://example.com/liberty-facts',
            'hashtags': '#statueofliberty #nyc #history #america',
            'mentions': '',
            'owner_username': 'history_buff',
            'likes': 1024,
            'comments': 87,
            'is_video': False,
            'video_url': ''
        }
    ]

    print(f"\n📍 Created {len(mock_locations)} mock locations")

    # Test CSV export
    test_filename = 'test_instagram_locations.csv'
    print(f"\n🔄 Testing CSV export to: {test_filename}")

    result = extractor.export_to_csv(mock_locations, filename=test_filename)

    if result:
        print(f"\n✅ TEST PASSED: CSV export successful!")

        # Read back and verify
        print(f"\n📄 Verifying CSV content:")
        with open(test_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"  - Total lines: {len(lines)} (1 header + {len(mock_locations)} data rows)")
            print(f"  - Header: {lines[0].strip()}")
            print(f"\n  First data row:")
            print(f"  {lines[1].strip()}")

        print(f"\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        return True
    else:
        print(f"\n❌ TEST FAILED: CSV export failed")
        return False


def test_class_initialization():
    """Test that the class can be initialized"""
    print("\n🔄 Testing class initialization...")
    try:
        extractor = InstagramLocationExtractor()
        print("✅ InstagramLocationExtractor initialized successfully")
        print(f"  - Loader object: {type(extractor.loader).__name__}")
        return True
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False


if __name__ == "__main__":
    print("\nRunning automated tests...\n")

    # Test 1: Class initialization
    test1 = test_class_initialization()

    # Test 2: CSV export
    test2 = test_csv_export()

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Class Initialization: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"CSV Export:           {'✅ PASS' if test2 else '❌ FAIL'}")
    print("=" * 60)

    if test1 and test2:
        print("\n🎉 All tests passed! The script is ready to use.")
        print("\nNext steps:")
        print("1. Run: ./venv/bin/python instagram_location_extractor.py")
        print("2. Enter your Instagram credentials when prompted")
        print("3. The script will extract and export your locations")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
