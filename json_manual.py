import json
path = "data.json"

def load_json(path):
    try:
        with open(path, "r", encoding="UTF-8") as file:
            try:
                data = json.load(file)
                print("JSON 로드 완료")
                return data
            except json.JSONDecodeError:
                        print("불러온 JSON 파일의 문법에 오류가 있습니다!")
                        return
        
    except FileNotFoundError:
        print("지정된 경로의 파일을 찾을 수 없습니다!")
        return

def normalize_label(label):
    if not isinstance(label, str):
        raise ValueError("문자열만 가능합니다!")

    label = label.strip().lower()

    cross = ["Cross", "cross", "+"]
    x = ["X", "x"]

    if label not in cross and label not in x:
         raise ValueError("지원하지 않는 라벨입니다!")

    return cross[0] if label in cross else x[0]
    

def run_json():
    data = load_json(path)
    if data is None:
         return