import os
import json
import requests
import time
import hashlib
import random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# API Keys
PEXELS_API_KEY = "QbZ7FqndljpYDP3H993N5DTooL3RLDCmqdodjTT35JjmrybXF8XJV6DW"
UNSPLASH_ACCESS_KEY = "cFhxdsT6vbgINEatl0RAQCdaq_4puV6db3YTvlFRYw8"

# Base directory
BASE_DIR = r"C:\Users\movemin\Desktop\FBC"
DATA_DIR = os.path.join(BASE_DIR, "data")

# JSON files to process
JSON_FILES = [
    "fashion.json",
    "beauty.json",
    "life.json",
    "districts.json"
]

# Thread-safe hash tracking
downloaded_hashes = {}
hash_lock = Lock()

# Thread-safe counters
stats = {
    'success': 0,
    'skip': 0,
    'fail': 0,
    'download': 0,
    'fallback_used': 0,
    'pexels_count': 0,
    'unsplash_count': 0
}
stats_lock = Lock()


def get_file_hash(file_path):
    """Calculate hash of a file to detect duplicates"""
    if not os.path.exists(file_path):
        return None

    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def clear_existing_images():
    """Ask user if they want to delete existing images"""
    print("=" * 70)
    print("Existing Image Management")
    print("=" * 70)
    print()
    print("Options:")
    print("  1. Keep existing images (skip already downloaded)")
    print("  2. Delete ALL images and re-download everything")
    print()

    while True:
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            print("\n✓ Keeping existing images. Only downloading missing ones.")
            return False
        elif choice == "2":
            confirm = input("\n⚠ Are you sure you want to DELETE ALL images? (yes/no): ").strip().lower()
            if confirm == "yes":
                img_folders = [
                    os.path.join(BASE_DIR, "img/fashion"),
                    os.path.join(BASE_DIR, "img/beauty"),
                    os.path.join(BASE_DIR, "img/life"),
                    os.path.join(BASE_DIR, "img/districts")
                ]

                deleted_count = 0
                for folder in img_folders:
                    if os.path.exists(folder):
                        for file in os.listdir(folder):
                            file_path = os.path.join(folder, file)
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                                deleted_count += 1

                print(f"\n✓ Deleted {deleted_count} existing images.")
                return True
            else:
                print("\n✓ Keeping existing images.")
                return False
        else:
            print("Invalid choice. Please enter 1 or 2.")


def create_folders():
    """Create necessary folder structure"""
    folders = [
        "img/fashion",
        "img/beauty",
        "img/life",
        "img/districts"
    ]
    for folder in folders:
        full_path = os.path.join(BASE_DIR, folder)
        os.makedirs(full_path, exist_ok=True)


def try_download_from_unsplash(keyword, save_path, page=1):
    """Try to download from Unsplash API"""
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {
        "query": keyword,
        "per_page": 10,
        "page": page,
        "orientation": "landscape"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)

        if response.status_code == 429:  # Rate limit
            time.sleep(2)
            return False

        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                photos = data['results']
                random.shuffle(photos)

                for photo in photos:
                    image_url = photo['urls']['regular']

                    temp_path = save_path + ".tmp"
                    img_response = requests.get(image_url, timeout=15)

                    if img_response.status_code == 200:
                        with open(temp_path, 'wb') as f:
                            f.write(img_response.content)

                        img_hash = get_file_hash(temp_path)

                        with hash_lock:
                            if img_hash in downloaded_hashes:
                                os.remove(temp_path)
                                continue

                            os.rename(temp_path, save_path)
                            downloaded_hashes[img_hash] = save_path

                        return True

        time.sleep(0.3)

    except Exception as e:
        pass

    return False


def try_download_from_pexels(keyword, save_path, page=1):
    """Try to download from Pexels API"""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": keyword,
        "per_page": 10,
        "page": page,
        "orientation": "landscape",
        "size": "large"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)

        if response.status_code == 429:  # Rate limit
            time.sleep(2)
            return False

        if response.status_code == 200:
            data = response.json()
            if data.get('photos'):
                photos = data['photos']
                random.shuffle(photos)

                for photo in photos:
                    image_url = photo['src']['large']

                    temp_path = save_path + ".tmp"
                    img_response = requests.get(image_url, timeout=15)

                    if img_response.status_code == 200:
                        with open(temp_path, 'wb') as f:
                            f.write(img_response.content)

                        img_hash = get_file_hash(temp_path)

                        with hash_lock:
                            if img_hash in downloaded_hashes:
                                os.remove(temp_path)
                                continue

                            os.rename(temp_path, save_path)
                            downloaded_hashes[img_hash] = save_path

                        return True

        time.sleep(0.3)

    except Exception as e:
        pass

    return False


def download_from_dual_sources(keyword, save_path, fallback_keywords, attempt=1):
    """
    Try to download from both Pexels and Unsplash with multiple fallback strategies
    """
    max_pages = 3

    # Randomly choose which API to try first
    apis = ['pexels', 'unsplash']
    random.shuffle(apis)

    # Strategy 1: Try both APIs with original keyword
    for api in apis:
        for page in range(1, max_pages + 1):
            if api == 'pexels':
                if try_download_from_pexels(keyword, save_path, page):
                    with stats_lock:
                        stats['pexels_count'] += 1
                    return True, f"{api}-original"
            else:
                if try_download_from_unsplash(keyword, save_path, page):
                    with stats_lock:
                        stats['unsplash_count'] += 1
                    return True, f"{api}-original"

    # Strategy 2: Keyword variations with both APIs
    if attempt == 1:
        variations = generate_keyword_variations(keyword)
        for var_keyword in variations:
            for api in apis:
                for page in range(1, 2):
                    if api == 'pexels':
                        if try_download_from_pexels(var_keyword, save_path, page):
                            with stats_lock:
                                stats['pexels_count'] += 1
                            return True, f"{api}-variation"
                    else:
                        if try_download_from_unsplash(var_keyword, save_path, page):
                            with stats_lock:
                                stats['unsplash_count'] += 1
                            return True, f"{api}-variation"

    # Strategy 3: Fallback keywords with both APIs
    for fallback_keyword in fallback_keywords:
        for api in apis:
            for page in range(1, 2):
                if api == 'pexels':
                    if try_download_from_pexels(fallback_keyword, save_path, page):
                        with stats_lock:
                            stats['pexels_count'] += 1
                        return True, f"{api}-fallback"
                else:
                    if try_download_from_unsplash(fallback_keyword, save_path, page):
                        with stats_lock:
                            stats['unsplash_count'] += 1
                        return True, f"{api}-fallback"

    # Strategy 4: Generic keywords with both APIs
    generic_keywords = ["korea", "korean culture", "asian style", "modern design"]
    for generic in generic_keywords:
        for api in apis:
            if api == 'pexels':
                if try_download_from_pexels(generic, save_path, 1):
                    with stats_lock:
                        stats['pexels_count'] += 1
                    return True, f"{api}-generic"
            else:
                if try_download_from_unsplash(generic, save_path, 1):
                    with stats_lock:
                        stats['unsplash_count'] += 1
                    return True, f"{api}-generic"

    return False, "failed"


def generate_keyword_variations(keyword):
    """Generate variations of the keyword"""
    variations = []
    words = keyword.split()

    if len(words) > 2:
        for i in range(len(words)):
            variation = " ".join(words[:i] + words[i + 1:])
            variations.append(variation)

    if len(words) >= 2:
        shuffled = words.copy()
        random.shuffle(shuffled)
        variations.append(" ".join(shuffled))

    if len(words) > 3:
        variations.append(" ".join(words[:len(words) // 2]))

    return variations[:3]


def load_district_meta():
    """Load district_meta.json for district_id mapping"""
    meta_path = os.path.join(DATA_DIR, "district_meta.json")

    if not os.path.exists(meta_path):
        return {}

    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta_data = json.load(f)

        # Create mapping: district_id -> name_en
        district_map = {}
        for district in meta_data:
            district_map[district['district_id']] = district['name_en'].lower()

        return district_map
    except Exception as e:
        print(f"Warning: Could not load district_meta.json: {e}")
        return {}


def extract_images_from_json(json_file, district_map):
    """Extract image paths and their metadata from JSON file"""
    file_path = os.path.join(DATA_DIR, json_file)

    if not os.path.exists(file_path):
        print(f"  ✗ File not found: {file_path}")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        images = []

        if isinstance(data, list):
            for item in data:
                if 'image' in item:
                    # Extract district_id if exists
                    district_id = item.get('district_id')
                    district_name = district_map.get(district_id, None) if district_id else None

                    images.append({
                        'path': item['image'],
                        'district_name': district_name,
                        'title_en': item.get('title_en', ''),
                        'desc_en': item.get('desc_en', ''),
                        'category': item.get('category', '')
                    })

        return images
    except Exception as e:
        print(f"  ✗ Error reading {json_file}: {e}")
        return []


def extract_keywords_from_text(text):
    """Extract meaningful keywords from text"""
    # Remove common words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                  'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                  'can', 'could', 'may', 'might', 'must', 'that', 'this', 'these', 'those'}

    # Split and filter
    words = text.lower().split()
    keywords = [w.strip('.,!?;:') for w in words if w.lower() not in stop_words and len(w) > 2]

    return ' '.join(keywords[:5])  # Take first 5 meaningful words


def get_keyword_for_image(image_info, json_file):
    """Generate keyword based on image info using title_en and desc_en"""
    file_type = json_file.replace('.json', '')

    # Primary keywords from title_en and desc_en
    title_keywords = extract_keywords_from_text(image_info.get('title_en', ''))
    desc_keywords = extract_keywords_from_text(image_info.get('desc_en', ''))

    # Combine keywords
    primary_keyword = f"{title_keywords} {desc_keywords}".strip()

    # If no keywords extracted, use category-based fallback
    if not primary_keyword:
        category = image_info.get('category', '').lower()
        if category:
            primary_keyword = category
        else:
            primary_keyword = file_type

    # Add district-specific context
    district_name = image_info.get('district_name')
    if district_name:
        if 'seongsu' in district_name:
            primary_keyword += " industrial urban seoul"
        elif 'hannam' in district_name:
            primary_keyword += " luxury sophisticated seoul"
        elif 'hongdae' in district_name:
            primary_keyword += " street youth seoul"
        elif 'myeongdong' in district_name:
            primary_keyword += " shopping seoul"
    else:
        primary_keyword += " korea korean"

    return primary_keyword


def generate_fallback_keywords(image_info, json_file):
    """Generate fallback keywords"""
    file_type = json_file.replace('.json', '')
    category = image_info.get('category', '').lower()

    fallbacks = []

    # Category-based fallbacks
    if 'fashion' in file_type or 'fashion' in category:
        fallbacks.extend(["fashion style", "trendy clothing", "korean fashion", "stylish outfit"])
    elif 'beauty' in file_type or 'beauty' in category:
        fallbacks.extend(["beauty makeup", "skincare", "cosmetics", "korean beauty"])
    elif 'life' in file_type or 'cafe' in category:
        fallbacks.extend(["lifestyle cafe", "modern living", "urban culture", "seoul cafe"])
    elif 'district' in file_type:
        fallbacks.extend(["seoul street", "urban neighborhood", "city culture", "korean district"])

    # Generic fallbacks
    fallbacks.extend(["korea", "korean style", "asian culture", "modern seoul"])

    return fallbacks[:5]


def load_existing_hashes():
    """Load hashes of existing images"""
    img_folders = [
        os.path.join(BASE_DIR, "img/fashion"),
        os.path.join(BASE_DIR, "img/beauty"),
        os.path.join(BASE_DIR, "img/life"),
        os.path.join(BASE_DIR, "img/districts")
    ]

    count = 0
    for folder in img_folders:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path) and not file.endswith('.tmp'):
                    file_hash = get_file_hash(file_path)
                    if file_hash:
                        downloaded_hashes[file_hash] = file_path
                        count += 1

    if count > 0:
        print(f"✓ Loaded {count} existing image hashes")


def download_single_image(task):
    """Download a single image with dual-source fallback strategies"""
    json_file, image_info, index, total = task
    image_path = image_info['path']
    full_path = os.path.join(BASE_DIR, image_path)
    file_type = json_file.replace('.json', '')

    # Skip if exists
    if os.path.exists(full_path):
        with stats_lock:
            stats['skip'] += 1
            stats['success'] += 1
        return {
            'status': 'skip',
            'path': image_path,
            'index': index,
            'total': total
        }

    # Create directory
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Generate keyword from title_en and desc_en
    keyword = get_keyword_for_image(image_info, json_file)
    fallback_keywords = generate_fallback_keywords(image_info, json_file)

    # Try download from both sources
    success, strategy = download_from_dual_sources(keyword, full_path, fallback_keywords)

    if success:
        with stats_lock:
            stats['success'] += 1
            stats['download'] += 1
            if 'fallback' in strategy or 'variation' in strategy or 'generic' in strategy:
                stats['fallback_used'] += 1

        return {
            'status': 'success',
            'path': image_path,
            'keyword': keyword,
            'strategy': strategy,
            'index': index,
            'total': total
        }
    else:
        with stats_lock:
            stats['fail'] += 1
        return {
            'status': 'fail',
            'path': image_path,
            'keyword': keyword,
            'index': index,
            'total': total
        }


def main():
    print("=" * 70)
    print("FBC Creators Image Download Script")
    print("Dual Source: Pexels + Unsplash")
    print("=" * 70)
    print()

    # Ask about existing images
    cleared = clear_existing_images()
    print()

    # Create folders
    print("Step 1: Creating folder structure...")
    create_folders()
    print("✓ Folders ready")
    print()

    # Load existing hashes
    if not cleared:
        print("Step 2: Loading existing image hashes...")
        load_existing_hashes()
        print()

    # Load district metadata
    print(f"Step {3 if not cleared else 2}: Loading district metadata...")
    district_map = load_district_meta()
    if district_map:
        print(f"✓ Loaded {len(district_map)} district mappings")
    print()

    # Collect all image paths
    print(f"Step {4 if not cleared else 3}: Collecting image paths from JSON files...")
    all_tasks = []

    for json_file in JSON_FILES:
        images = extract_images_from_json(json_file, district_map)
        if images:
            print(f"  ✓ {json_file}: {len(images)} images")
            for img_info in images:
                all_tasks.append((json_file, img_info, len(all_tasks) + 1, 0))
        else:
            print(f"  ⚠ {json_file}: No images found")

    # Update total count
    total = len(all_tasks)
    all_tasks = [(j, i, idx, total) for j, i, idx, _ in all_tasks]

    print(f"\nTotal images to process: {total}")
    print()

    # Check if there are any images to download
    if total == 0:
        print("=" * 70)
        print("⚠ No images to download.")
        print("=" * 70)
        print()
        print("Possible reasons:")
        print("  - All images already exist (skipped)")
        print("  - JSON files are empty or missing")
        print("  - JSON files are not in the correct format")
        print()
        input("Press Enter to exit...")
        return

    # Download with ThreadPoolExecutor
    print(f"Step {5 if not cleared else 4}: Downloading images (using {min(6, total)} parallel threads)...")
    print("Note: Using title_en & desc_en for intelligent keyword generation")
    print()

    max_workers = min(2, total)
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_single_image, task): task for task in all_tasks}

        for future in as_completed(futures):
            result = future.result()

            if result['status'] == 'skip':
                print(f"[{result['index']}/{result['total']}] ⊙ Skip: {result['path']}")
            elif result['status'] == 'success':
                strategy = result.get('strategy', '')
                source = "Pexels" if 'pexels' in strategy else "Unsplash"

                strategy_info = ""
                if 'fallback' in strategy:
                    strategy_info = f" [{source} - fallback]"
                elif 'variation' in strategy:
                    strategy_info = f" [{source} - variation]"
                elif 'generic' in strategy:
                    strategy_info = f" [{source} - generic]"
                else:
                    strategy_info = f" [{source}]"

                print(f"[{result['index']}/{result['total']}] ✓ Success: {result['path']}{strategy_info}")
            else:
                print(f"[{result['index']}/{result['total']}] ✗ Failed: {result['path']}")

    elapsed_time = time.time() - start_time

    # Summary
    print()
    print("=" * 70)
    print("Download Summary")
    print("=" * 70)
    print(f"Total: {total}")
    print(f"Success: {stats['success']} (New: {stats['download']}, Skipped: {stats['skip']})")
    print(f"Failed: {stats['fail']}")
    print(f"Fallback strategies used: {stats['fallback_used']} times")
    print(f"")
    print(f"Source breakdown:")
    print(f"  - Pexels: {stats['pexels_count']} images")
    print(f"  - Unsplash: {stats['unsplash_count']} images")
    print(f"")
    print(f"Unique images: {len(downloaded_hashes)}")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Average speed: {total / elapsed_time:.2f} images/sec")
    print()

    if stats['fail'] > 0:
        print(f"⚠ {stats['fail']} images failed after all retry strategies.")
    else:
        print("✓ All images downloaded successfully!")

    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
