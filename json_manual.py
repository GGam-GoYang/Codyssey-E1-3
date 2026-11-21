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

        

def run_json():
    data = load_json(path)
    if data is None:
         return