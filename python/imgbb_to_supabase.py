import os
import requests
import json
from pathlib import Path
from supabase import create_client, Client

# ============================================
# 설정
# ============================================
IMGBB_API_KEY = '4a0d69744fa47d8de59028ec369b7abc'
SUPABASE_URL = 'https://ipcibnhhegkhdwyxeqjs.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlwY2libmhoZWdraGR3eXhlcWpzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA3MzMyNzYsImV4cCI6MjA3NjMwOTI3Nn0.LKjw1dqgjs39shvGpxcfFPutA7p1yR9eOb4zhomSBS8';
IMG_FOLDER = r'C:\Users\kwony\Desktop\FBC\img'

# Supabase 클라이언트 생성
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# 이미지 업로드 함수
# ============================================
def upload_to_imgbb(image_path):
    """이미지를 ImgBB에 업로드하고 URL 반환"""
    try:
        with open(image_path, 'rb') as file:
            payload = {
                'key': IMGBB_API_KEY,
                'image': file
            }
            response = requests.post('https://api.imgbb.com/1/upload', files={'image': file}, data={'key': IMGBB_API_KEY})

            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    return {
                        'url': data['data']['url'],
                        'delete_url': data['data']['delete_url'],
                        'filename': os.path.basename(image_path)
                    }
            return None
    except Exception as e:
        print(f"❌ Error uploading {image_path}: {e}")
        return None

# ============================================
# 파일명으로 매칭하는 함수
# ============================================
def extract_filename_from_url(url):
    """ImgBB URL에서 원본 파일명 추출"""
    # 예: https://i.ibb.co/xxxxx/filename.jpg
    if 'ibb.co' in url:
        parts = url.split('/')
        if len(parts) > 0:
            return parts[-1]  # filename.jpg
    return None

# ============================================
# 메인 프로세스
# ============================================
def main():
    print("🚀 이미지 재업로드 및 Supabase 업데이트 시작...\n")

    # 1. 로컬 이미지 파일 목록 가져오기
    img_files = [f for f in os.listdir(IMG_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]
    print(f"📁 발견된 이미지: {len(img_files)}개\n")

    # 2. 각 이미지를 ImgBB에 업로드
    upload_results = {}
    for idx, filename in enumerate(img_files, 1):
        print(f"[{idx}/{len(img_files)}] 업로드 중: {filename}...", end=" ")
        image_path = os.path.join(IMG_FOLDER, filename)
        result = upload_to_imgbb(image_path)

        if result:
            upload_results[filename] = result
            print(f"✅ 성공")
        else:
            print(f"❌ 실패")

    print(f"\n✅ 업로드 완료: {len(upload_results)}/{len(img_files)}개\n")

    # 3. Supabase content_items 테이블 업데이트
    print("🔄 Supabase content_items 업데이트 중...\n")

    try:
        # 모든 content_items 가져오기
        response = supabase.table('content_items').select('*').execute()
        items = response.data

        updated_count = 0
        for item in items:
            current_url = item.get('image')
            if not current_url:
                continue

            # 현재 URL에서 파일명 추출
            old_filename = extract_filename_from_url(current_url)
            if not old_filename:
                continue

            # 새로 업로드된 이미지 중 매칭되는 것 찾기
            if old_filename in upload_results:
                new_data = upload_results[old_filename]

                # 업데이트
                update_response = supabase.table('content_items').update({
                    'image': new_data['url']
                }).eq('id', item['id']).execute()

                print(f"✅ {item['id']}: {old_filename} → 새 URL 적용")
                updated_count += 1

        print(f"\n✅ content_items 업데이트 완료: {updated_count}개\n")

    except Exception as e:
        print(f"❌ Supabase 업데이트 오류: {e}")

    # 4. 결과 요약 저장
    result_file = os.path.join(os.path.dirname(IMG_FOLDER), 'upload_results.json')
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(upload_results, f, indent=2, ensure_ascii=False)

    print(f"📄 업로드 결과 저장: {result_file}\n")
    print("🎉 모든 작업 완료!")

if __name__ == '__main__':
    main()
