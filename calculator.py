import math

EPSILON = 1e-9

def calculate_mac(pattern, weights):
    """같은 위치의 곱을 누적한다. pattern/weights: 검증된 동일 크기 2차원 배열. 반환: float 점수."""
    res = 0.0
    for i, j in zip(pattern, weights):
        for k, l in zip(i, j):
            res += k*l

    if not math.isfinite(res):
        raise ValueError("MAC 결과가 유한한 숫자가 아닙니다!")
    return res


def decide_label(a_score, b_score, a_label, b_label, epsilon=EPSILON):
    """점수 차이로 판정한다. a_score/b_score: 점수, a_label/b_label: 이름, epsilon: 허용오차. 반환: 이름 또는 UNDECIDED."""
    if abs(a_score-b_score) < epsilon:
        return "UNDECIDED"

    return a_label if a_score > b_score else b_label

def normalize_label(label):
    """label: 원본 문자열. 반환: Cross 또는 X. 문자열/지원 라벨이 아니면 ValueError."""
    if not isinstance(label, str):
        raise ValueError("문자열만 가능합니다!")

    label = label.strip().lower()

    cross = ["Cross", "cross", "+"]
    x = ["X", "x"]

    if label not in cross and label not in x:
         raise ValueError("지원하지 않는 라벨입니다!")

    return cross[0] if label in cross else x[0]


def check_matrix(matrix, n):
    """matrix: 검사할 배열, n: 행/열 개수. 반환: None. 크기·자료형·유한 숫자가 아니면 ValueError."""
    if not isinstance(matrix, list):
        raise ValueError("matrix는 리스트 자료형이어야 합니다!")

    if not (len(matrix) == n and all(isinstance(x, list) and len(x) == n for x in matrix)):
        raise ValueError(f"리스트의 행, 열의 길이는 모두 {n}이어야 합니다!")
   
    for i in matrix:
        for j in i:
            if isinstance(j, bool) or not isinstance(j, (int, float)):
                raise ValueError("모든 원소는 숫자여야 합니다!")
            try:
                finite = math.isfinite(j)
            except OverflowError:
                finite = False
            if not finite:
                raise ValueError("유한한 숫자가 필요합니다!")

    return

