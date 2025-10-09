import os
import json
import requests
import time
from pathlib import Path

# Pexels API Key
API_KEY = "QbZ7FqndljpYDP3H993N5DTooL3RLDCmqdodjTT35JjmrybXF8XJV6DW"

# Base directory
BASE_DIR = r"C:\Users\movemin\Desktop\새 폴더\FBC"
DATA_DIR = os.path.join(BASE_DIR, "data")

# JSON files to process
JSON_FILES = [
    "hero.json",
    "headlines.json",
    "fashion.json",
    "beauty.json",
    "life.json",
    "districts.json"
]

# Search keywords mapping (based on content type)
KEYWORDS_MAP = {
    "hero": "seoul city architecture culture",
    "headlines": "fashion lifestyle culture seoul",
    "fashion": "fashion model clothing style",
    "beauty": "beauty makeup skincare cosmetics",
    "life": "lifestyle cafe culture seoul",
    "districts": "seoul district street culture"
}


def create_folders():
    """Create necessary folder structure"""
    folders = [
        "img/hero",
        "img/headlines",
        "img/fashion",
        "img/beauty",
        "img/life",
        "img/districts"
    ]
    for folder in folders:
        full_path = os.path.join(BASE_DIR, folder)
        os.makedirs(full_path, exist_ok=True)
        print(f"✓ Folder ready: {full_path}")


def download_from_pexels(keyword, save_path, orientation="landscape"):
    """Download image from Pexels API"""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": API_KEY}
    params = {
        "query": keyword,
        "per_page": 1,
        "orientation": orientation,
        "size": "large"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                image_url = data['photos'][0]['src']['large']

                # Download image
                img_response = requests.get(image_url, timeout=10)
                if img_response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(img_response.content)
                    return True
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def extract_images_from_json(json_file):
    """Extract image paths from JSON file"""
    file_path = os.path.join(DATA_DIR, json_file)

    if not os.path.exists(file_path):
        print(f"⚠ File not found: {file_path}")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        images = []

        # Handle different JSON structures
        if isinstance(data, list):
            for item in data:
                # Direct image field
                if 'image' in item:
                    images.append(item['image'])
                # Featured stories (for districts.json)
                if 'featured_stories' in item:
                    for story in item['featured_stories']:
                        if 'image' in story:
                            images.append(story['image'])
        elif isinstance(data, dict):
            # Single object with image
            if 'image' in data:
                images.append(data['image'])

        return images
    except Exception as e:
        print(f"✗ Error reading {json_file}: {e}")
        return []


def get_keyword_for_image(image_path, json_file):
    """Generate keyword based on image path and JSON file"""
    base_name = os.path.basename(image_path)
    file_type = json_file.replace('.json', '')

    # Get base keyword from map
    base_keyword = KEYWORDS_MAP.get(file_type, "korea fashion lifestyle")

    # Add specific keywords based on path
    if 'seongsu' in image_path:
        base_keyword += " industrial factory aesthetic"
    elif 'hannam' in image_path:
        base_keyword += " luxury sophisticated premium"
    elif 'hongdae' in image_path:
        base_keyword += " street youth trendy"
    elif 'myeongdong' in image_path:
        base_keyword += " shopping tourism beauty"

    if 'cafe' in image_path:
        base_keyword += " cafe coffee interior"
    elif 'street' in image_path:
        base_keyword += " street urban city"
    elif 'gallery' in image_path:
        base_keyword += " gallery art exhibition"
    elif 'nail' in image_path:
        base_keyword += " nail art manicure salon"
    elif 'hair' in image_path:
        base_keyword += " hair salon hairstyle"
    elif 'food' in image_path or 'restaurant' in image_path:
        base_keyword += " food restaurant dining"

    return base_keyword


def main():
    print("=" * 70)
    print("FBC Creators Image Download Script (Pexels API)")
    print("=" * 70)
    print()

    # Step 1: Create folders
    print("Step 1: Creating folder structure...")
    create_folders()
    print()

    # Step 2: Collect all image paths from JSON files
    print("Step 2: Collecting image paths from JSON files...")
    all_images = {}

    for json_file in JSON_FILES:
        images = extract_images_from_json(json_file)
        if images:
            all_images[json_file] = images
            print(f"  ✓ {json_file}: {len(images)} images found")

    total_images = sum(len(imgs) for imgs in all_images.values())
    print(f"\nTotal images to download: {total_images}")
    print()

    # Step 3: Download images
    print("Step 3: Downloading images from Pexels...")
    print()

    success_count = 0
    skip_count = 0
    fail_count = 0
    download_count = 0

    for json_file, image_paths in all_images.items():
        print(f"\n📁 Processing {json_file}...")

        for idx, image_path in enumerate(image_paths, 1):
            full_path = os.path.join(BASE_DIR, image_path)

            # Skip if file already exists
            if os.path.exists(full_path):
                print(f"  [{idx}/{len(image_paths)}] ⊙ Skip (exists): {image_path}")
                skip_count += 1
                success_count += 1
                continue

            # Create directory if not exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            # Generate keyword
            keyword = get_keyword_for_image(image_path, json_file)

            print(f"  [{idx}/{len(image_paths)}] Downloading: {image_path}")
            print(f"    Keyword: {keyword}")

            # Download image
            if download_from_pexels(keyword, full_path):
                print(f"    ✓ Downloaded successfully")
                success_count += 1
                download_count += 1
            else:
                print(f"    ✗ Download failed")
                fail_count += 1

            # API rate limit: Wait 1 second between requests
            time.sleep(1.2)

    # Step 4: Summary
    print()
    print("=" * 70)
    print("Download Summary")
    print("=" * 70)
    print(f"Total: {total_images}")
    print(f"Success: {success_count} (New: {download_count}, Skipped: {skip_count})")
    print(f"Failed: {fail_count}")
    print()

    if fail_count > 0:
        print("⚠ Some images failed to download. Please check your API key and internet connection.")
    else:
        print("✓ All images downloaded successfully!")


if __name__ == "__main__":
    main()
