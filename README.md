# Instagram Location Extractor

A Python script that extracts location data from your Instagram saved posts/collections and exports them to CSV format for easy import into Google Maps.

## Features

- 🔐 Secure login with Instagram credentials
- 📍 Extracts location data from saved Instagram posts
- 📊 Exports to CSV format compatible with Google My Maps
- 🗺️ Easy import into Google Maps for visualization
- 📝 Includes post URLs, dates, and captions

## Prerequisites

- Python 3.7 or higher
- An Instagram account
- Saved posts with location tags

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install instaloader
```

## Usage

1. Run the script:

```bash
python instagram_location_extractor.py
```

2. Enter your Instagram username and password when prompted

3. The script will:
   - Log in to your Instagram account
   - Access your saved posts
   - Extract all posts that have location tags
   - Export them to a CSV file (e.g., `instagram_locations_20250116_123456.csv`)

## Importing into Google Maps

Once you have the CSV file:

1. Go to [Google My Maps](https://www.google.com/maps/d/)
2. Click **"Create a New Map"**
3. Click **"Import"** in the left panel
4. Select your CSV file
5. Choose which columns to use for:
   - **Position columns**: Latitude, Longitude
   - **Marker title**: Name
   - **Marker description**: Description
6. Click **"Finish"**

Your Instagram locations will now be displayed on the map!

## Output Format

The CSV file contains the following columns:

- **Name**: Location name from Instagram
- **Latitude**: Geographic latitude
- **Longitude**: Geographic longitude
- **Description**: Caption from the post (first 100 characters)
- **URL**: Direct link to the Instagram post
- **Date**: Date the post was created

## Important Notes

### Instagram API Limitations

Due to Instagram's API restrictions:
- The script extracts locations from **ALL** your saved posts (not individual collections)
- Instagram doesn't expose collection names through their API
- You may need to wait between requests to avoid rate limiting

### Authentication

- The script uses direct username/password login
- Your credentials are **NOT** stored anywhere
- If you have 2FA enabled, you may need to:
  - Temporarily disable it, OR
  - Use Instagram's session file (advanced usage)

### Privacy & Security

- This script only accesses **YOUR** saved posts
- No data is sent to any third party
- All processing is done locally on your machine
- Consider using a virtual environment to isolate dependencies

## Troubleshooting

### Login Failed

- **Invalid credentials**: Double-check your username and password
- **2FA enabled**: Temporarily disable two-factor authentication
- **Rate limited**: Wait a few hours before trying again

### No Locations Found

This can happen if:
- None of your saved posts have location tags
- The posts are from accounts that removed location data
- Instagram's API is blocking access

### Rate Limiting

If you encounter rate limiting:
- Wait several hours before running again
- Process fewer posts at a time
- Consider using Instagram's official API (requires app registration)

## Advanced Usage

### Custom Output Filename

Edit the script to specify a custom filename:

```python
extractor.export_to_csv(locations, filename='my_custom_locations.csv')
```

### Filter by Date Range

You can modify the `extract_locations_from_saved()` method to filter posts by date:

```python
from datetime import datetime, timedelta

# Only get locations from the last 30 days
cutoff_date = datetime.now() - timedelta(days=30)

for post in saved_posts:
    if post.date_local >= cutoff_date and post.location:
        # ... rest of the code
```

## Dependencies

- **instaloader**: Python library for downloading Instagram content

## License

This script is provided as-is for personal use. Please respect Instagram's Terms of Service and API usage policies.

## Disclaimer

- This tool is for personal use only
- Use responsibly and respect Instagram's rate limits
- The author is not responsible for any account restrictions that may result from excessive API usage
- Always comply with Instagram's Terms of Service

## Contributing

Feel free to fork and improve this script! Some ideas for enhancements:

- [ ] Support for session file authentication (bypass 2FA issues)
- [ ] Export to KML/GeoJSON formats
- [ ] Filter locations by date range or keyword
- [ ] Interactive map preview before export
- [ ] Support for downloading post images alongside locations

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Ensure you're using the latest version of `instaloader`
3. Check Instagram's current API status and policies
