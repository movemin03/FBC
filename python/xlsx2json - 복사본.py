import json
import random


def add_views_to_json(filename):
    """
    JSON 파일에 각 항목의 마지막에 views 필드를 추가
    """
    # 파일 읽기
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 각 항목에 views 추가 (0 ~ 100,000 사이 랜덤 값)
    for item in data:
        item['views'] = random.randint(0, 100000)

    # 파일 저장 (들여쓰기 2칸, 한글 유지)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ {filename} - views 추가 완료 ({len(data)}개 항목)")

    # 샘플 출력
    if len(data) > 0:
        print(f"  예시: {data[0].get('id', 'N/A')} - views: {data[0]['views']:,}")


# 파일 목록
files = ['fashion.json', 'beauty.json', 'life.json', 'districts.json']

print("=" * 60)
print("JSON 파일에 views 필드 추가")
print("=" * 60)
print()

# 각 파일 처리
for filename in files:
    try:
        add_views_to_json(filename)
    except FileNotFoundError:
        print(f"✗ {filename} - 파일을 찾을 수 없습니다")
    except Exception as e:
        print(f"✗ {filename} - 오류 발생: {e}")
    print()

print("=" * 60)
print("완료!")
print("=" * 60)
