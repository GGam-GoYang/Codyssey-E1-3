import json
from bonus import compare_flat
from pathlib import Path
from performance import print_performance, prepare_samples
from calculator import calculate_mac, decide_label, normalize_label, check_matrix

DATA_PATH = Path(__file__).with_name("data.json")


def load_json(path):
    """파일을 UTF-8로 읽는다. path: 파일 경로. 반환: Python 객체. 읽기 오류는 호출자에게 전달."""
    with open(path, "r", encoding="utf-8-sig") as file:
        return json.load(file)

def load_filters(raw_filters):
    """raw_filters: JSON filters 값. 반환: (정상 필터 딕셔너리, 크기별 오류 딕셔너리). 오류 크기만 제외하고 계속 처리."""
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


def get_pattern_size(case_id):
    """case_id: size_N_번호 문자열. 반환: 양의 정수 N. 잘못된 형식은 ValueError."""
    if not isinstance(case_id, str):
        raise ValueError("패턴 키는 문자열이어야 합니다!")

    parts = case_id.split("_")

    if len(parts) != 3:
        raise ValueError("패턴 키는 size_N_번호 형식이어야 합니다!")

    if parts[0] != "size":
        raise ValueError("패턴 키는 size로 시작해야 합니다!")

    try:
        n = int(parts[1])
        index = int(parts[2])
    except ValueError:
        raise ValueError("크기와 번호는 정수여야 합니다!")

    if n <= 0 or index <= 0:
        raise ValueError("크기와 번호는 양의 정수여야 합니다!")

    return n



def analyze_case(case_id, case, filters, errors):
    """패턴 하나를 계산한다.

    파라미터: case_id는 패턴 키, case는 input/expected 딕셔너리,
        filters는 크기별 정상 필터, errors는 크기별 오류 문자열.
    반환: 점수·판정·expected·통과 여부·실패 사유를 담은 딕셔너리.
    예외: 키/크기/라벨/필터가 잘못되면 ValueError.
    """
    n = get_pattern_size(case_id)
    if n in errors:
        raise ValueError("필터 오류: " + errors[n])
    if n not in filters:
        raise ValueError(f"size_{n} 필터가 없습니다!")
    if not isinstance(case, dict) or "input" not in case or "expected" not in case:
        raise ValueError("input과 expected가 필요합니다!")

    pattern = case["input"]
    check_matrix(pattern, n)
    expected = normalize_label(case["expected"])
    cross_score = calculate_mac(pattern, filters[n]["Cross"])
    x_score = calculate_mac(pattern, filters[n]["X"])
    prediction = decide_label(cross_score, x_score, "Cross", "X")
    passed = prediction == expected
    reason = ""
    if prediction == "UNDECIDED":
        reason = "동점(UNDECIDED)으로 expected와 불일치"
    elif not passed:
        reason = "판정과 expected 불일치"
    return {"id": case_id, "n": n, "cross_score": cross_score,
            "x_score": x_score, "prediction": prediction,
            "expected": expected, "passed": passed, "reason": reason}


def run_json(path=DATA_PATH):
    """JSON 모드 실행. path: 입력 경로. 반환: 케이스 결과 리스트, 파일/최상위 구조 오류 시 None."""
    try:
        data = load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print("JSON 로드 실패:", error)
        return
    if not isinstance(data, dict) or not isinstance(data.get("patterns"), dict):
        print("JSON 구조 오류: 최상위 객체와 patterns는 딕셔너리여야 합니다.")
        return

    filters, errors = load_filters(data.get("filters"))
    for n in (5, 13, 25):
        if n in errors:
            print(f"size_{n}: 필터 오류 - {errors[n]}")
        else:
            print(f"size_{n}: 필터 로드 완료 (Cross, X)")

    results = []
    samples = {}
    for case_id, case in data["patterns"].items():
        print(f"\n[{case_id}]")
        try:
            result = analyze_case(case_id, case, filters, errors)
            print("Cross 점수:", result["cross_score"])
            print("X 점수:", result["x_score"])
            print(f"판정: {result['prediction']} | expected: {result['expected']}")
            # 동점 케이스도 배열 자체가 정상이면 시간 측정에 사용할 수 있다.
            n = result["n"]
            if n not in samples:
                samples[n] = (case["input"], filters[n]["Cross"], filters[n]["X"])
        except ValueError as error:
            result = {"id": case_id, "passed": False, "reason": str(error)}
        results.append(result)
        print("PASS" if result["passed"] else "FAIL: " + result["reason"])

    samples = prepare_samples(samples)
    print_performance(samples)
    compare_flat(samples)
    failed = [result for result in results if not result["passed"]]
    print(f"\n전체: {len(results)} | 통과: {len(results) - len(failed)} | 실패: {len(failed)}")
    for result in failed:
        print(f"- {result['id']}: {result['reason']}")
    return results
