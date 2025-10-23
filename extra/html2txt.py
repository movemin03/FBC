import os
from pathlib import Path
from bs4 import BeautifulSoup

# 기본 경로 설정
base_path = Path(r"C:\Users\movemin\Desktop\FBC")
output_path = base_path / "html2txt"

# 출력 폴더가 없으면 생성
output_path.mkdir(parents=True, exist_ok=True)

# 변환된 파일 목록 저장
converted_files = []

# FBC 폴더 내의 모든 HTML 파일 찾기
for html_file in base_path.rglob("*.html"):
    try:
        # 상위 폴더명 가져오기
        parent_folder = html_file.parent.name

        # 원본 파일명 (확장자 제외)
        file_stem = html_file.stem

        # 새 파일명 생성: 상위폴더명_파일명_html.txt
        new_filename = f"{parent_folder}_{file_stem}_html.txt"
        output_file = output_path / new_filename

        # HTML 파일 읽기
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # BeautifulSoup으로 HTML 파싱하여 텍스트 추출
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text(separator='\n', strip=True)

        # 텍스트 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text_content)

        converted_files.append({
            'original': str(html_file.relative_to(base_path)),
            'converted': new_filename
        })

        print(f"변환 완료: {html_file.name} -> {new_filename}")

    except Exception as e:
        print(f"Error processing {html_file}: {str(e)}")

print(f"\n총 {len(converted_files)}개의 HTML 파일을 변환했습니다.")
print(f"출력 경로: {output_path}")
