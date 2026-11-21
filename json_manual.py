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

def load_filters(raw_filters):
    filters = {}
    errors = {}

    for n in [5, 13, 25]:
        try:
            if not isinstance(raw_filters, dict):
                raise ValueError("filters는 딕셔너리 형태여야 합니다!")

            filte = raw_filters.get(f"size_{n}")

            if not isinstance(filte, dict):
                raise ValueError("필터 그룹은 딕셔너리 형태여야 합니다!")

            converted = {}

            for label, value in filte.items():
                name = normalize_label(label)

                if name in converted:
                    raise ValueError("같은 라벨의 필터가 중복됐습니다!")

                check_matrix(value, n)
                converted[name] = value

            if "Cross" not in converted or "X" not in converted:
                raise ValueError("Cross와 X 필터가 모두 필요합니다!")

            filters[n] = converted 

        except ValueError as e:
            errors[n] = str(e)

    return filters, errors             
     

def run_json():
    data = load_json(path)
    filters, errors = load_filters(data.get("filters"))
    print(filters.keys()) 
    print(errors)        
    if data is None:
         return