from supabase import create_client, Client

# ============================================
# Configuration
# ============================================
SUPABASE_URL = 'https://ipcibnhhegkhdwyxeqjs.supabase.co'
SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlwY2libmhoZWdraGR3eXhlcWpzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDczMzI3NiwiZXhwIjoyMDc2MzA5Mjc2fQ.EI135Z7IvPq2Z5q8emBlL9JMhnHIRes0RiLYfLKbKHM'  # Service Role Key!


# Supabase 클라이언트
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# ============================================
# URL 매핑 데이터
# ============================================
URL_MAPPINGS = {
    'lf00030': 'https://i.ibb.co/QFHNdW6m/lf00030.webp',
    'lf00029': 'https://i.ibb.co/Q3J6FTym/lf00029.webp',
    'lf00028': 'https://i.ibb.co/KpWY5kCc/lf00028.webp',
    'lf00027': 'https://i.ibb.co/tP2R1m73/lf00027.webp',
    'lf00026': 'https://i.ibb.co/cSkZDGcq/lf00026.webp',
    'lf00025': 'https://i.ibb.co/4n1QMKQt/lf00025.webp',
    'lf00024': 'https://i.ibb.co/kVrbyVKS/lf00024.webp',
    'lf00023': 'https://i.ibb.co/1tVzXj0x/lf00023.webp',
    'lf00022': 'https://i.ibb.co/cSJDVbJc/lf00022.webp',
    'lf00021': 'https://i.ibb.co/4wNnfqYG/lf00021.webp',
    'lf00020': 'https://i.ibb.co/tTpfX5Pd/lf00020.webp',
    'lf00019': 'https://i.ibb.co/Q3D4FVrv/lf00019.webp',
    'lf00018': 'https://i.ibb.co/j7pxmGj/lf00018.webp',
    'lf00017': 'https://i.ibb.co/qLm651dy/lf00017.webp',
    'lf00016': 'https://i.ibb.co/hxB6c6Qs/lf00016.webp',
    'lf00015': 'https://i.ibb.co/XrWHNnBW/lf00015.webp',
    'lf00014': 'https://i.ibb.co/rGNQ2ZDr/lf00014.webp',
    'lf00013': 'https://i.ibb.co/zhqgkzGt/lf00013.webp',
    'lf00012': 'https://i.ibb.co/CKxbhSBW/lf00012.webp',
    'lf00011': 'https://i.ibb.co/2Yqqmb8v/lf00011.webp',
    'lf00010': 'https://i.ibb.co/KJ0RMcM/lf00010.webp',
    'lf00009': 'https://i.ibb.co/KcdK1BnY/lf00009.webp',
    'lf00008': 'https://i.ibb.co/9H7LVvtb/lf00008.webp',
    'lf00007': 'https://i.ibb.co/wFsB1gGR/lf00007.webp',
    'lf00006': 'https://i.ibb.co/dJJSTb4s/lf00006.webp',
    'lf00005': 'https://i.ibb.co/Nd19nYT0/lf00005.webp',
    'lf00004': 'https://i.ibb.co/gMwZfdtG/lf00004.webp',
    'lf00003': 'https://i.ibb.co/fGn4HTwZ/lf00003.webp',
    'lf00002': 'https://i.ibb.co/6RTjspxr/lf00002.webp',
    'lf00001': 'https://i.ibb.co/LdMg6ZZ3/lf00001.webp',
    'fs00030': 'https://i.ibb.co/jZk1rwMw/fs00030.webp',
    'fs00029': 'https://i.ibb.co/0dpr7Mb/fs00029.webp',
    'fs00028': 'https://i.ibb.co/twrshRfK/fs00028.webp',
    'fs00027': 'https://i.ibb.co/MyDhD3Dx/fs00027.webp',
    'fs00026': 'https://i.ibb.co/wZg7vQWv/fs00026.webp',
    'fs00025': 'https://i.ibb.co/cSw6hPv2/fs00025.webp',
    'fs00024': 'https://i.ibb.co/XfpvZ73C/fs00024.webp',
    'fs00023': 'https://i.ibb.co/JwSMZ4WR/fs00023.webp',
    'fs00022': 'https://i.ibb.co/847qzRSG/fs00022.webp',
    'fs00021': 'https://i.ibb.co/xtGx4WYv/fs00021.webp',
    'fs00020': 'https://i.ibb.co/rGwf0jTL/fs00020.webp',
    'fs00019': 'https://i.ibb.co/qMDj6NkG/fs00019.webp',
    'fs00018': 'https://i.ibb.co/mCHYyQT4/fs00018.webp',
    'fs00017': 'https://i.ibb.co/DDRM0Cxt/fs00017.webp',
    'fs00016': 'https://i.ibb.co/Fq0LVqsQ/fs00016.webp',
    'fs00015': 'https://i.ibb.co/3YNzqs6C/fs00015.webp',
    'fs00014': 'https://i.ibb.co/cKP6Tmbs/fs00014.webp',
    'fs00013': 'https://i.ibb.co/DfQZq1H3/fs00013.webp',
    'fs00012': 'https://i.ibb.co/Cs5X512C/fs00012.webp',
    'fs00011': 'https://i.ibb.co/5gncR6BG/fs00011.webp',
    'fs00010': 'https://i.ibb.co/XrX8YbsJ/fs00010.webp',
    'fs00009': 'https://i.ibb.co/qF5BPwbp/fs00009.webp',
    'fs00008': 'https://i.ibb.co/Q7Ngyc8d/fs00008.webp',
    'fs00007': 'https://i.ibb.co/N6zGgD9M/fs00007.webp',
    'fs00006': 'https://i.ibb.co/BHnTyKgb/fs00006.webp',
    'fs00005': 'https://i.ibb.co/PvFjbx8H/fs00005.webp',
    'fs00004': 'https://i.ibb.co/WvCN0sTw/fs00004.webp',
    'fs00003': 'https://i.ibb.co/qFsXNYWp/fs00003.webp',
    'fs00002': 'https://i.ibb.co/BHhWRrT8/fs00002.webp',
    'fs00001': 'https://i.ibb.co/wFntHdPn/fs00001.webp',
    'ds00030': 'https://i.ibb.co/4nyzCdth/ds00030.webp',
    'ds00029': 'https://i.ibb.co/KxpwZmJd/ds00029.webp',
    'ds00028': 'https://i.ibb.co/ynKgPT6p/ds00028.webp',
    'ds00027': 'https://i.ibb.co/svYWH0NG/ds00027.webp',
    'ds00026': 'https://i.ibb.co/21KTjWyL/ds00026.webp',
    'ds00025': 'https://i.ibb.co/v4z3x15X/ds00025.webp',
    'ds00024': 'https://i.ibb.co/mFMXNtHw/ds00024.webp',
    'ds00023': 'https://i.ibb.co/MkhKYFRy/ds00023.webp',
    'ds00022': 'https://i.ibb.co/fYmpscQM/ds00022.webp',
    'ds00021': 'https://i.ibb.co/DDYk1pNq/ds00021.webp',
    'ds00020': 'https://i.ibb.co/35n7zrMw/ds00020.webp',
    'ds00019': 'https://i.ibb.co/8DFyZM37/ds00019.webp',
    'ds00018': 'https://i.ibb.co/GvqC0zmk/ds00018.webp',
    'ds00017': 'https://i.ibb.co/Z6zqJMK9/ds00017.webp',
    'ds00016': 'https://i.ibb.co/LdhJ8XYG/ds00016.webp',
    'ds00015': 'https://i.ibb.co/V0N5wnyq/ds00015.webp',
    'ds00014': 'https://i.ibb.co/YFQcVt4L/ds00014.webp',
    'ds00013': 'https://i.ibb.co/nNfx4RWz/ds00013.webp',
    'ds00012': 'https://i.ibb.co/jkH25Njg/ds00012.webp',
    'ds00011': 'https://i.ibb.co/d4srm0JW/ds00011.webp',
    'ds00010': 'https://i.ibb.co/kgBNGKny/ds00010.webp',
    'ds00009': 'https://i.ibb.co/7dhhYWhT/ds00009.webp',
    'ds00008': 'https://i.ibb.co/Sw6PC5tj/ds00008.webp',
    'ds00007': 'https://i.ibb.co/MTFytt7/ds00007.webp',
    'ds00006': 'https://i.ibb.co/VpBpn5tn/ds00006.webp',
    'ds00005': 'https://i.ibb.co/v4mmCnCC/ds00005.webp',
    'ds00004': 'https://i.ibb.co/PsNVwgG1/ds00004.webp',
    'ds00003': 'https://i.ibb.co/bRPG6Vgw/ds00003.webp',
    'ds00002': 'https://i.ibb.co/DgY7wyWW/ds00002.webp',
    'ds00001': 'https://i.ibb.co/FqsvqCKt/ds00001.webp',
    'by00030': 'https://i.ibb.co/C3qzSh1G/by00030.webp',
    'by00029': 'https://i.ibb.co/8nZZBfff/by00029.webp',
    'by00028': 'https://i.ibb.co/Ngd4n9xB/by00028.webp',
    'by00027': 'https://i.ibb.co/p6pTJB16/by00027.webp',
    'by00026': 'https://i.ibb.co/gMVTzFq7/by00026.webp',
    'by00025': 'https://i.ibb.co/RGbzWYvv/by00025.webp',
    'by00024': 'https://i.ibb.co/TMxkfQmd/by00024.webp',
    'by00023': 'https://i.ibb.co/3ZpHh2m/by00023.webp',
    'by00022': 'https://i.ibb.co/p6wR6pL2/by00022.webp',
    'by00021': 'https://i.ibb.co/Xx8x3mFm/by00021.webp',
    'by00020': 'https://i.ibb.co/zHQfTLTt/by00020.webp',
    'by00019': 'https://i.ibb.co/ZRTqx1jY/by00019.webp',
    'by00018': 'https://i.ibb.co/T6kJ3x8/by00018.webp',
    'by00017': 'https://i.ibb.co/KkQ7gjN/by00017.webp',
    'by00016': 'https://i.ibb.co/YSCr67n/by00016.webp',
    'by00015': 'https://i.ibb.co/BKg4DhM7/by00015.webp',
    'by00014': 'https://i.ibb.co/7dh9M3vT/by00014.webp',
    'by00013': 'https://i.ibb.co/kgz3WWw6/by00013.webp',
    'by00012': 'https://i.ibb.co/rfZgMq67/by00012.webp',
    'by00011': 'https://i.ibb.co/d4KRk5V9/by00011.webp',
    'by00010': 'https://i.ibb.co/zTt9H3sC/by00010.webp',
    'by00009': 'https://i.ibb.co/6RJ458Kp/by00009.webp',
    'by00008': 'https://i.ibb.co/LDSqZmLb/by00008.webp',
    'by00007': 'https://i.ibb.co/WNpb9gBZ/by00007.webp',
    'by00006': 'https://i.ibb.co/r2TSrwVN/by00006.webp',
    'by00005': 'https://i.ibb.co/rKrcNFC3/by00005.webp',
    'by00004': 'https://i.ibb.co/MkggVyyD/by00004.webp',
    'by00003': 'https://i.ibb.co/CsNm7PRk/by00003.webp',
    'by00002': 'https://i.ibb.co/4wBk9ykv/by00002.webp',
    'by00001': 'https://i.ibb.co/ycY9t3Gx/by00001.webp'
}


# ============================================
# Main Process
# ============================================
def main():
    print("🔧 Supabase 이미지 필드 업데이트 시작...\n")

    # Step 1: 필드명 변경 (SQL로 실행)
    print("📋 Step 1: image_display_url → image_origin_url 필드명 변경")
    print("   ⚠️  Supabase SQL Editor에서 수동 실행 필요:")
    print("   ALTER TABLE content_items RENAME COLUMN image_display_url TO image_origin_url;\n")

    input("   위 SQL을 실행한 후 Enter를 누르세요...")

    # Step 2: URL 업데이트
    print("\n🔄 Step 2: image_origin_url 업데이트 중...\n")

    updated_count = 0
    failed_count = 0

    for article_id, new_url in URL_MAPPINGS.items():
        try:
            response = supabase.table('content_items') \
                .update({'image_origin_url': new_url}) \
                .eq('id', article_id) \
                .execute()

            if hasattr(response, 'data') and response.data:
                print(f"✅ {article_id}: {new_url}")
                updated_count += 1
            else:
                print(f"⚠️  {article_id}: 업데이트 응답 없음")
                failed_count += 1

        except Exception as e:
            print(f"❌ {article_id}: {e}")
            failed_count += 1

    print(f"\n" + "=" * 60)
    print(f"✅ 성공: {updated_count}개")
    print(f"❌ 실패: {failed_count}개")
    print(f"=" * 60)


if __name__ == '__main__':
    main()
