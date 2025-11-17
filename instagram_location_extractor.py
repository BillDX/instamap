#!/usr/bin/env python3
"""
Instagram Collection Location Extractor
Extracts location data from Instagram saved collections and exports to CSV for Google Maps
"""

import instaloader
import csv
import sys
import re
from datetime import datetime
from typing import List, Dict, Optional
import getpass


class InstagramLocationExtractor:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        self.profile = None

    @staticmethod
    def extract_urls_from_text(text: str) -> List[str]:
        """Extract all URLs from a text string"""
        if not text:
            return []
        # URL pattern - matches http://, https://, and www. URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        return urls

    def login(self, username: str, password: str) -> bool:
        """Login to Instagram with username and password"""
        try:
            print(f"Logging in as {username}...")
            self.loader.login(username, password)
            print("✓ Login successful!")
            return True
        except instaloader.exceptions.BadCredentialsException:
            print("✗ Login failed: Invalid username or password")
            return False
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            print("✗ Two-factor authentication required. Please disable 2FA temporarily or use session file.")
            return False
        except Exception as e:
            print(f"✗ Login failed: {e}")
            return False

    def get_saved_collections(self) -> List[str]:
        """Get list of saved collection names"""
        try:
            print("\nFetching your saved collections...")
            collections = []

            # Get saved posts (collections are accessed through saved posts)
            profile = instaloader.Profile.from_username(self.loader.context, self.loader.context.username)

            # Note: Instaloader provides access to saved posts, but Instagram's API
            # doesn't directly expose collection names. We'll work with all saved posts.
            saved_posts = profile.get_saved_posts()

            print("✓ Accessing saved posts...")
            return saved_posts

        except Exception as e:
            print(f"✗ Error fetching collections: {e}")
            return []

    def extract_locations_from_saved(self) -> List[Dict[str, any]]:
        """Extract location data from saved posts"""
        locations = []

        try:
            profile = instaloader.Profile.from_username(self.loader.context, self.loader.context.username)
            saved_posts = profile.get_saved_posts()

            print("\nExtracting locations from saved posts...")
            post_count = 0
            location_count = 0

            for post in saved_posts:
                post_count += 1

                if post.location:
                    # Get full caption text
                    full_caption = post.caption if post.caption else ''

                    # Extract URLs from caption
                    caption_urls = self.extract_urls_from_text(full_caption)

                    # Extract hashtags
                    hashtags = ' '.join([f'#{tag}' for tag in post.caption_hashtags]) if post.caption_hashtags else ''

                    # Extract mentions
                    mentions = ' '.join([f'@{mention}' for mention in post.caption_mentions]) if post.caption_mentions else ''

                    location_data = {
                        'name': post.location.name,
                        'latitude': post.location.lat,
                        'longitude': post.location.lng,
                        'post_url': f"https://www.instagram.com/p/{post.shortcode}/",
                        'date': post.date_local.strftime('%Y-%m-%d %H:%M:%S'),
                        'caption': full_caption,
                        'caption_urls': ', '.join(caption_urls) if caption_urls else '',
                        'hashtags': hashtags,
                        'mentions': mentions,
                        'owner_username': post.owner_username,
                        'likes': post.likes,
                        'comments': post.comments,
                        'is_video': post.is_video,
                        'video_url': post.video_url if post.is_video else ''
                    }
                    locations.append(location_data)
                    location_count += 1
                    print(f"  [{location_count}] Found: {post.location.name}")

                # Show progress every 10 posts
                if post_count % 10 == 0:
                    print(f"  Processed {post_count} posts, found {location_count} locations...")

            print(f"\n✓ Extraction complete: {location_count} locations from {post_count} posts")
            return locations

        except Exception as e:
            print(f"✗ Error extracting locations: {e}")
            return locations

    def export_to_csv(self, locations: List[Dict[str, any]], filename: str = None) -> str:
        """Export locations to CSV format for Google Maps import"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'instagram_locations_{timestamp}.csv'

        try:
            # Extended field names to capture all post data
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'Name', 'Latitude', 'Longitude', 'Description', 'URL', 'Date',
                    'Caption_Full', 'Caption_URLs', 'Hashtags', 'Mentions',
                    'Owner_Username', 'Likes', 'Comments', 'Is_Video', 'Video_URL'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for loc in locations:
                    writer.writerow({
                        'Name': loc['name'],
                        'Latitude': loc['latitude'],
                        'Longitude': loc['longitude'],
                        'Description': loc['caption'][:200] if loc['caption'] else '',  # Truncated for Google Maps display
                        'URL': loc['post_url'],
                        'Date': loc['date'],
                        'Caption_Full': loc['caption'],
                        'Caption_URLs': loc['caption_urls'],
                        'Hashtags': loc['hashtags'],
                        'Mentions': loc['mentions'],
                        'Owner_Username': loc['owner_username'],
                        'Likes': loc['likes'],
                        'Comments': loc['comments'],
                        'Is_Video': 'Yes' if loc['is_video'] else 'No',
                        'Video_URL': loc['video_url']
                    })

            print(f"\n✓ Exported {len(locations)} locations to: {filename}")
            print(f"\nCSV includes:")
            print(f"  - Full caption text (Caption_Full column)")
            print(f"  - Extracted URLs from captions (Caption_URLs column)")
            print(f"  - Hashtags and mentions")
            print(f"  - Owner username, likes, comments")
            print(f"  - Video URLs (if applicable)")
            print(f"\nTo import into Google Maps:")
            print(f"1. Go to https://www.google.com/maps/d/")
            print(f"2. Click 'Create a New Map'")
            print(f"3. Click 'Import' and select: {filename}")
            print(f"4. Map columns: Name, Latitude, Longitude, Description")

            return filename

        except Exception as e:
            print(f"✗ Error exporting to CSV: {e}")
            return None


def main():
    print("=" * 60)
    print("Instagram Collection Location Extractor")
    print("=" * 60)

    extractor = InstagramLocationExtractor()

    # Get credentials
    print("\nEnter your Instagram credentials:")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")

    # Login
    if not extractor.login(username, password):
        sys.exit(1)

    # Note: Instagram API limitations mean we can't easily list collection names
    # So we'll extract from all saved posts
    print("\nNote: Due to Instagram API limitations, this will extract locations")
    print("from ALL your saved posts (across all collections).")

    proceed = input("\nProceed? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Cancelled.")
        sys.exit(0)

    # Extract locations
    locations = extractor.extract_locations_from_saved()

    if not locations:
        print("\n⚠ No locations found in your saved posts.")
        print("This could mean:")
        print("  - None of your saved posts have location tags")
        print("  - There was an error accessing the data")
        sys.exit(0)

    # Export to CSV
    extractor.export_to_csv(locations)

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
