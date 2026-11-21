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
    

def check_matrix(matrix, n):
    if not isinstance(matrix, list):
        raise ValueError("matrix는 리스트 자료형이어야 합니다!")

    if not (len(matrix) == n and all(isinstance(x, list) and len(x) == n for x in matrix)):
        raise ValueError(f"리스트의 행, 열의 길이는 모두 {n}이어야 합니다!")
   
    for i in matrix:
        for j in i:
            if isinstance(j, bool) or not isinstance(j, (int, float)):
                raise ValueError("모든 원소는 숫자여야 합니다!")


    return
             
     

def run_json():
    data = load_json(path)
    if data is None:
         return