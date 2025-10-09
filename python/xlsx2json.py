import pandas as pd
import json

# Excel 파일 경로
file_path = r"C:\Users\movemin\Desktop\FBC\tables\headlines.xlsx"

# Excel 파일 읽기
df = pd.read_excel(file_path)

# JSON 파일로 저장 (방법 1: 기본 형식)
output_path_1 = r"C:\Users\movemin\Desktop\FBC\tables\headlines.json"
df.to_json(output_path_1, orient='records', force_ascii=False, indent=2)

# JSON 파일로 저장 (방법 2: 한글 깨짐 방지 및 예쁘게 포맷팅)
with open(output_path_1, 'w', encoding='utf-8') as f:
    json.dump(df.to_dict(orient='records'), f, ensure_ascii=False, indent=2)

print(f"✅ JSON 변환 완료: {output_path_1}")
print(f"총 {len(df)}개의 데이터가 변환되었습니다.")
