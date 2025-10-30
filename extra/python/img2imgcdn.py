import os
from pathlib import Path
from supabase import create_client, Client

# Supabase 설정
SUPABASE_URL = "https://ipcibnhhegkhdwyxeqjs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlwY2libmhoZWdraGR3eXhlcWpzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDczMzI3NiwiZXhwIjoyMDc2MzA5Mjc2fQ.EI135Z7IvPq2Z5q8emBlL9JMhnHIRes0RiLYfLKbKHM"
# Supabase 클라이언트 생성
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 이미지 디렉토리 경로
IMAGE_DIR = r"C:\Users\movemin\Desktop\FBC\img\contents"
BUCKET_NAME = "fbc-images"  # Supabase Storage 버킷 이름


def create_bucket_if_not_exists():
    """버킷이 없으면 생성"""
    try:
        buckets = supabase.storage.list_buckets()
        bucket_names = [bucket.name for bucket in buckets]

        if BUCKET_NAME not in bucket_names:
            supabase.storage.create_bucket(BUCKET_NAME, options={"public": True})
            print(f"✅ 버킷 '{BUCKET_NAME}' 생성 완료")
        else:
            print(f"✅ 버킷 '{BUCKET_NAME}' 이미 존재")
    except Exception as e:
        print(f"❌ 버킷 생성 오류: {e}")


def upload_images():
    """이미지 파일들을 Supabase Storage에 업로드"""
    image_path = Path(IMAGE_DIR)

    if not image_path.exists():
        print(f"❌ 디렉토리를 찾을 수 없습니다: {IMAGE_DIR}")
        return

    # webp 파일들만 가져오기
    image_files = list(image_path.glob("*.webp"))

    if not image_files:
        print(f"❌ {IMAGE_DIR}에 .webp 파일이 없습니다")
        return

    print(f"📁 총 {len(image_files)}개의 이미지 파일 발견")

    uploaded_count = 0
    failed_count = 0

    for image_file in image_files:
        file_name = image_file.name
        item_id = image_file.stem  # 확장자 제외한 파일명 (예: fs00001)

        try:
            # 파일 읽기
            with open(image_file, 'rb') as f:
                file_data = f.read()

            # Supabase Storage에 업로드
            storage_path = f"contents/{file_name}"

            # 기존 파일이 있으면 삭제
            try:
                supabase.storage.from_(BUCKET_NAME).remove([storage_path])
            except:
                pass

            # 새 파일 업로드
            supabase.storage.from_(BUCKET_NAME).upload(
                storage_path,
                file_data,
                {"content-type": "image/webp"}
            )

            # Public URL 생성
            public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(storage_path)

            # content_items 테이블 업데이트
            update_data = {
                "image": public_url,
                "image_delete_url": None  # Supabase Storage는 삭제 URL이 따로 없음
            }

            result = supabase.table("content_items").update(update_data).eq("id", item_id).execute()

            if result.data:
                print(f"✅ {file_name} → {item_id} 업데이트 완료")
                uploaded_count += 1
            else:
                print(f"⚠️  {file_name} → DB에 {item_id} 없음")
                failed_count += 1

        except Exception as e:
            print(f"❌ {file_name} 업로드 실패: {e}")
            failed_count += 1

    print(f"\n📊 업로드 완료: {uploaded_count}개 성공, {failed_count}개 실패")


def remove_image_origin_url_column():
    """image_origin_url 컬럼 제거 (SQL 실행)"""
    try:
        # Supabase Python 클라이언트는 ALTER TABLE을 직접 지원하지 않으므로
        # Supabase Dashboard에서 SQL Editor를 통해 실행하거나
        # psycopg2로 직접 연결해야 합니다

        print("\n⚠️  image_origin_url 컬럼 제거는 Supabase Dashboard에서 수동으로 실행해주세요:")
        print("SQL Editor에서 다음 쿼리 실행:")
        print("ALTER TABLE content_items DROP COLUMN IF EXISTS image_origin_url;")

    except Exception as e:
        print(f"❌ 컬럼 제거 오류: {e}")


def main():
    print("🚀 FBC 이미지 업로드 시작\n")

    # 1. 버킷 생성
    create_bucket_if_not_exists()

    # 2. 이미지 업로드 및 DB 업데이트
    upload_images()

    # 3. 컬럼 제거 안내
    remove_image_origin_url_column()

    print("\n✅ 모든 작업 완료!")


if __name__ == "__main__":
    main()
