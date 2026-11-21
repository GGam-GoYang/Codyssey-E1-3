import math
from performance import print_performance
from calculator import calculate_mac, decide_label

def run_user():
    """파라미터 없음. 필터 A/B와 패턴을 입력받고 계산·판정·시간을 출력한다. 반환: None."""
    filter_a = read_matrix("필터 A")
    filter_b = read_matrix("필터 B")

    print("필터 저장 완료")
    pattern = read_matrix("패턴")

    a_score = calculate_mac(pattern, filter_a)
    b_score = calculate_mac(pattern, filter_b)
    print(f"필터 A 점수 : {a_score}, 필터 B 점수 : {b_score}")
    label = decide_label(a_score, b_score, "A", "B")

    print("판정 결과 :", "판정 불가" if label == "UNDECIDED" else label)
    print_performance({3: (pattern, filter_a, filter_b)}, labels=("A", "B"))

def read_matrix(name):
    """name: 안내용 이름. 반환: 3x3 실수 배열. 숫자·열 개수 오류는 같은 행을 재입력."""
    res = []
    print(f"{name} 입력")

    for x in range(3):
        while True:
            try:
                inp = [float(j) for j in input(f"{x+1}번째 행 입력 (공백으로 구분) : ").split()]

            except ValueError:
                print("숫자만 입력할 수 있습니다!")
                continue

            if len(inp) != 3:
                print("숫자는 3개를 입력해야 합니다!")
                continue

            if not all(math.isfinite(value) for value in inp):
                print("유한한 숫자를 입력해주세요!")
                continue

            res.append(inp)
            break

    return res

