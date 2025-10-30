from datetime import datetime


def generate_sitemap_index():
    """Sitemap Index 파일 생성"""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    sitemaps = ['main', 'fashion', 'beauty', 'life', 'districts']
    today = datetime.now().strftime('%Y-%m-%d')

    for sitemap_name in sitemaps:
        xml += f'''  <sitemap>
    <loc>https://fbc-pink.vercel.app/sitemap-{sitemap_name}.xml</loc>
    <lastmod>{today}</lastmod>
  </sitemap>
'''

    xml += '</sitemapindex>'

    with open('sitemap-index.xml', 'w', encoding='utf-8') as f:
        f.write(xml)

    print(f"✅ sitemap-index.xml 생성 완료")


def generate_main_sitemap():
    """메인/카테고리 페이지 sitemap 생성"""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    today = datetime.now().strftime('%Y-%m-%d')

    pages = [
        ('/', 'daily', '1.0'),
        ('/index.html', 'daily', '1.0'),
        ('/fashion/index.html', 'daily', '0.9'),
        ('/beauty/index.html', 'daily', '0.9'),
        ('/life/index.html', 'daily', '0.9'),
        ('/districts/index.html', 'daily', '0.9'),
        ('/about/index.html', 'monthly', '0.7'),
    ]

    for path, changefreq, priority in pages:
        xml += f'''  <url>
    <loc>https://fbc-pink.vercel.app{path}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
'''

    xml += '</urlset>'

    with open('sitemap-main.xml', 'w', encoding='utf-8') as f:
        f.write(xml)

    print(f"✅ sitemap-main.xml 생성 완료")


def generate_category_sitemap(category_name, prefix, count):
    """카테고리별 아티클 sitemap 생성"""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    today = datetime.now().strftime('%Y-%m-%d')

    for i in range(1, count + 1):
        article_id = f"{prefix}{i:05d}"
        xml += f'''  <url>
    <loc>https://fbc-pink.vercel.app/article/index.html?category={category_name}&amp;id={article_id}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
'''

    xml += '</urlset>'

    with open(f'sitemap-{category_name}.xml', 'w', encoding='utf-8') as f:
        f.write(xml)

    print(f"✅ sitemap-{category_name}.xml 생성 완료 ({count}개 아티클)")


def main():
    """전체 sitemap 생성"""
    print("🚀 Sitemap 생성 시작...\n")

    # 카테고리 설정 (카테고리명, prefix, 개수)
    categories = [
        ('fashion', 'fs', 30),
        ('beauty', 'by', 30),
        ('life', 'lf', 30),
        ('districts', 'ds', 30),
    ]

    # Sitemap Index 생성
    generate_sitemap_index()

    # Main Sitemap 생성
    generate_main_sitemap()

    # 카테고리별 Sitemap 생성
    for category_name, prefix, count in categories:
        generate_category_sitemap(category_name, prefix, count)

    print(f"\n✨ 총 {len(categories) + 2}개의 sitemap 파일 생성 완료!")
    print(f"📝 총 {sum(c[2] for c in categories) + 7}개의 URL이 등록되었습니다.")


if __name__ == "__main__":
    main()
