import os
import requests
from urllib.parse import quote
import time

# 이미지 다운로드 설정
IMAGE_LIST = [
    # Hero Section
    {"filename": "hero-main.jpg", "folder": "img/hero",
     "keyword": "ballet dancer artistic photography dark background elegant"},

    # Headlines Section
    {"filename": "hdl00001.jpg", "folder": "img/headlines",
     "keyword": "myeongdong seoul street shopping tourism korea"},
    {"filename": "hdl00003.jpg", "folder": "img/headlines", "keyword": "korean drama filming location cheongju city"},
    {"filename": "hdl00004.jpg", "folder": "img/headlines", "keyword": "olive young store k-beauty products korea"},
    {"filename": "hdl00005.jpg", "folder": "img/headlines", "keyword": "seongsu industrial fashion aesthetic korea"},
    {"filename": "hdl00007.jpg", "folder": "img/headlines", "keyword": "hongdae street fashion young people seoul"},
    {"filename": "hdl00008.jpg", "folder": "img/headlines", "keyword": "seoul night market street food korea"},
    {"filename": "hdl00009.jpg", "folder": "img/headlines", "keyword": "korean medical spa wellness nature"},
    {"filename": "hdl00010.jpg", "folder": "img/headlines", "keyword": "k-drama location fan pilgrimage korea"},
    {"filename": "hdl00011.jpg", "folder": "img/headlines", "keyword": "korean fashion export global trend"},

    # Districts Section
    {"filename": "seongsu-cafe-01.jpg", "folder": "img/districts",
     "keyword": "seongsu cafe industrial interior seoul korea"},
    {"filename": "seongsu-street-01.jpg", "folder": "img/districts",
     "keyword": "seongsu dong street fashion photography seoul"},

    # Fashion Section
    {"filename": "fs00001.jpg", "folder": "img/fashion", "keyword": "workwear fashion industrial aesthetic"},
    {"filename": "fs00002.jpg", "folder": "img/fashion", "keyword": "minimal leather bag fashion accessory"},
    {"filename": "fs00003.jpg", "folder": "img/fashion", "keyword": "vintage denim jeans fashion style"},
    {"filename": "fs00004.jpg", "folder": "img/fashion", "keyword": "white sneakers street fashion"},
    {"filename": "fs00005.jpg", "folder": "img/fashion", "keyword": "seoul fashion week runway model"},
    {"filename": "fs00006.jpg", "folder": "img/fashion", "keyword": "hongdae street style young fashion seoul"},
    {"filename": "fs00007.jpg", "folder": "img/fashion", "keyword": "fall knitwear sweater styling"},

    # Beauty Section
    {"filename": "by00001.jpg", "folder": "img/beauty", "keyword": "natural glow makeup korean beauty"},
    {"filename": "by00002.jpg", "folder": "img/beauty", "keyword": "aesthetic nail salon interior minimal"},
    {"filename": "by00003.jpg", "folder": "img/beauty", "keyword": "fall skincare products autumn beauty"},
    {"filename": "by00004.jpg", "folder": "img/beauty", "keyword": "minimal hairstyle short hair trend"},
    {"filename": "by00005.jpg", "folder": "img/beauty", "keyword": "korean beauty routine skincare steps"},
    {"filename": "by00006.jpg", "folder": "img/beauty", "keyword": "fall makeup warm tone cosmetics"},

    # Life Section
    {"filename": "lf00001.jpg", "folder": "img/life", "keyword": "seongsu cafe industrial design interior seoul"},
]


def create_folders():
    """필요한 폴더 구조 생성"""
    folders = set([item['folder'] for item in IMAGE_LIST])
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✓ Created folder: {folder}")




def download_from_pexels(keyword, save_path):
    """Pexels API를 사용한 이미지 다운로드"""
    # Pexels API 키 (무료, https://www.pexels.com/api/ 에서 발급)
    API_KEY = "QbZ7FqndljpYDP3H993N5DTooL3RLDCmqdodjTT35JjmrybXF8XJV6DW"  # 여기에 본인의 키 입력

    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": API_KEY}
    params = {
        "query": keyword,
        "per_page": 1,
        "orientation": "landscape"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                image_url = data['photos'][0]['src']['large']

                # 이미지 다운로드
                img_response = requests.get(image_url)
                with open(save_path, 'wb') as f:
                    f.write(img_response.content)
                return True
        print(f"  ✗ Failed to fetch from Pexels: {response.status_code}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def download_placeholder(save_path, width=1920, height=1080):
    """플레이스홀더 이미지 다운로드 (API 없이 사용 가능)"""
    url = f"https://placehold.co/{width}x{height}/e5e7eb/9ca3af?text=FBC+Placeholder"
    try:
        response = requests.get(url)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"  ✗ Error downloading placeholder: {e}")
        return False


def main():
    print("=" * 60)
    print("FBC Creators Image Download Script")
    print("=" * 60)
    print()

    # 1. 폴더 생성
    print("Step 1: Creating folder structure...")
    create_folders()
    print()

    # 2. 이미지 다운로드
    print("Step 2: Downloading images...")
    print()

    success_count = 0
    fail_count = 0

    for idx, item in enumerate(IMAGE_LIST, 1):
        filename = item['filename']
        folder = item['folder']
        keyword = item['keyword']
        save_path = os.path.join(folder, filename)

        # 이미 존재하는 파일 스킵
        if os.path.exists(save_path):
            print(f"[{idx}/{len(IMAGE_LIST)}] ⊙ Skipped (already exists): {save_path}")
            success_count += 1
            continue

        print(f"[{idx}/{len(IMAGE_LIST)}] Downloading: {filename}")
        print(f"  Keyword: {keyword}")

        # Unsplash 시도
        # Pexels 시도
        if download_from_pexels(keyword, save_path):
            print(f"  ✓ Downloaded from Pexels: {save_path}")
            success_count += 1
        # 플레이스홀더 사용
        else:
            if download_placeholder(save_path):
                print(f"  ⚠ Using placeholder: {save_path}")
                success_count += 1
            else:
                print(f"  ✗ Failed: {save_path}")
                fail_count += 1

        # API 호출 제한 방지
        time.sleep(1)
        print()

    # 3. 결과 요약
    print("=" * 60)
    print("Download Summary")
    print("=" * 60)
    print(f"Total: {len(IMAGE_LIST)}")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")
    print()
    print("✓ Image download complete!")


if __name__ == "__main__":
    main()
