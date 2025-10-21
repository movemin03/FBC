import json
from supabase import create_client, Client

# ============================================
# FBC Supabase 마이그레이션 스크립트
# ============================================

# Supabase 설정
SUPABASE_URL = "https://ipcibnhhegkhdwyxeqjs.supabase.co"
SUPABASE_KEY = "sbp_91e0c87002a76b5219dfec5c3279a78b1bc0ab4b"  # ⚠️ Service Role Key로 교체 필수!

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("=" * 50)
print("FBC 데이터 마이그레이션 시작")
print("=" * 50)
print()

# ============================================
# 1. district_meta 마이그레이션
# ============================================
print("📍 1/4: district_meta.json 마이그레이션 중...")
try:
    with open('district_meta.json', 'r', encoding='utf-8') as f:
        districts = json.load(f)

    for district in districts:
        result = supabase.table('district_meta').insert(district).execute()

    print(f"   ✅ {len(districts)}개 지역 데이터 삽입 완료")
except Exception as e:
    print(f"   ❌ 에러: {e}")

print()

# ============================================
# 2. content_items 마이그레이션 (4개 파일 통합)
# ============================================
files_to_migrate = [
    ('fashion.json', 'fashion'),
    ('beauty.json', 'beauty'),
    ('life.json', 'life'),
    ('districts.json', 'districts')
]

total_items = 0

for filename, source_type in files_to_migrate:
    print(f"📦 2/4: {filename} → content_items 마이그레이션 중...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            items = json.load(f)

        for item in items:
            content_data = {
                'id': item['id'],
                'source_type': source_type,
                'district_id': item.get('district_id'),
                'title_kor': item['title_kor'],
                'title_en': item['title_en'],
                'desc_kor': item.get('desc_kor'),
                'desc_en': item.get('desc_en'),
                'category': item['category'],
                'image': item.get('image'),
                'tags': item.get('tags', []),
                'cultural_badge': item.get('cultural_badge'),
                'date': item['date'],
                'author': item.get('author'),
                'views': item.get('views', 0),
                'image_display_url': item.get('image_display_url'),
                'image_delete_url': item.get('image_delete_url')
            }

            result = supabase.table('content_items').insert(content_data).execute()
            total_items += 1

        print(f"   ✅ {len(items)}개 아이템 삽입 완료")
    except Exception as e:
        print(f"   ❌ 에러: {e}")

print(f"   📊 총 {total_items}개 content_items 삽입 완료")
print()

# ============================================
# 3. articles 마이그레이션
# ============================================
print("📝 3/4: article.json → articles 마이그레이션 중...")
try:
    with open('article.json', 'r', encoding='utf-8') as f:
        articles_data = json.load(f)

    for article in articles_data:
        article_data = {
            'id': article['id'],
            'article_html_ko': article['article_html_ko'],
            'article_html_en': article['article_html_en']
        }

        result = supabase.table('articles').insert(article_data).execute()

    print(f"   ✅ {len(articles_data)}개 아티클 HTML 삽입 완료")
except Exception as e:
    print(f"   ❌ 에러: {e}")

print()

# ============================================
# 4. featured_content 마이그레이션
# ============================================
print("⭐ 4/4: pinned.json → featured_content 마이그레이션 중...")
try:
    with open('pinned.json', 'r', encoding='utf-8') as f:
        pinned = json.load(f)

    total_featured = 0
    for section_type, items in pinned.items():
        for idx, item in enumerate(items):
            featured_data = {
                'section_type': section_type,
                'article_id': item['id'],
                'display_order': idx,
                'active': True
            }

            result = supabase.table('featured_content').insert(featured_data).execute()
            total_featured += 1

    print(f"   ✅ {total_featured}개 featured content 삽입 완료")
except Exception as e:
    print(f"   ❌ 에러: {e}")

print()
print("=" * 50)
print("🎉 마이그레이션 완료!")
print("=" * 50)

# ============================================
# 데이터 확인
# ============================================
print("\n데이터 확인 중...")
try:
    # 테이블별 row count
    districts_count = len(supabase.table('district_meta').select('district_id').execute().data)
    content_count = len(supabase.table('content_items').select('id').execute().data)
    articles_count = len(supabase.table('articles').select('id').execute().data)
    featured_count = len(supabase.table('featured_content').select('id').execute().data)

    print(f"\n📊 최종 통계:")
    print(f"   - district_meta: {districts_count}개")
    print(f"   - content_items: {content_count}개")
    print(f"   - articles: {articles_count}개")
    print(f"   - featured_content: {featured_count}개")
except Exception as e:
    print(f"   ❌ 데이터 확인 중 에러: {e}")
