import json
import os

# 파일 경로 설정
base_folder = r"C:\Users\movemin\Desktop\FBC\img\test"
imgbb_file = r"C:\Users\movemin\Desktop\FBC\img\test\imgbb_webp_upload_results.json"
json_files = ["life.json", "fashion.json", "beauty.json", "districts.json"]

# imgbb 업로드 결과 파일 읽기
with open(imgbb_file, 'r', encoding='utf-8') as f:
    imgbb_data = json.load(f)

# imgbb 데이터를 relative_path 기반으로 매핑 생성
imgbb_map = {}
for item in imgbb_data:
    # relative_path를 normalize (백슬래시를 슬래시로)
    relative_path = item['relative_path'].replace('\\', '/')
    imgbb_map[relative_path] = {
        'url': item['url'],
        'display_url': item['display_url'],
        'delete_url': item['delete_url']
    }

print(f"imgbb_map에 {len(imgbb_map)}개의 항목이 로드되었습니다.\n")


# 이미지 경로를 업데이트하는 함수
def update_image_links(data_list, category_name):
    updated_count = 0
    not_found = []

    for item in data_list:
        if 'image' in item:
            old_image_path = item['image']
            # "img/" 제거하고 경로 normalize
            relative_path = old_image_path.replace('img/', '')

            if relative_path in imgbb_map:
                # 기존 image를 old_image_url로 백업
                item['old_image_url'] = old_image_path
                # 새로운 URL로 업데이트
                item['image'] = imgbb_map[relative_path]['url']
                item['image_display_url'] = imgbb_map[relative_path]['display_url']
                item['image_delete_url'] = imgbb_map[relative_path]['delete_url']
                updated_count += 1
            else:
                not_found.append(relative_path)

    print(f"{category_name}:")
    print(f"  - 업데이트된 항목: {updated_count}개")
    if not_found:
        print(f"  - 찾을 수 없는 이미지: {len(not_found)}개")
        print(f"    예시: {not_found[:3]}")
    print()

    return updated_count


# 각 JSON 파일 처리
total_updated = 0
for json_file in json_files:
    # 파일 읽기
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 이미지 링크 업데이트
    updated = update_image_links(data, json_file)
    total_updated += updated

    # 업데이트된 파일을 지정된 폴더에 저장
    output_path = os.path.join(base_folder, json_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ {json_file} 저장 완료: {output_path}\n")

print(f"=== 작업 완료 ===")
print(f"총 {total_updated}개의 항목이 업데이트되었습니다.")

# 샘플 데이터 확인
with open(os.path.join(base_folder, 'life.json'), 'r', encoding='utf-8') as f:
    sample_data = json.load(f)

print("\n=== 업데이트 결과 샘플 (life.json 첫 번째 항목) ===")
sample = sample_data[0]
print(f"ID: {sample['id']}")
print(f"Title: {sample['title_kor']}")
print(f"Old Image URL: {sample.get('old_image_url', 'N/A')}")
print(f"New Image URL: {sample['image']}")
print(f"Display URL: {sample['image_display_url']}")
print(f"Delete URL: {sample['image_delete_url']}")
