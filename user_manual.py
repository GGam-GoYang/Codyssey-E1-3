def run_user():
    filter_a = read_matrix("필터 A")
    filter_b = read_matrix("필터 B")

    print("필터 저장 완료")
    pattern = read_matrix("패턴")

    a_score = calculate_mac(pattern, filter_a)
    b_score = calculate_mac(pattern, filter_b)
    print(f"필터 A 점수 : {a_score}, 필터 B 점수 : {b_score}")
    label = decide_label(a_score, b_score, "A", "B")

    print(f"판정 결과 : {label}")

def read_matrix(name):
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

            res.append(inp)
            break

    return res

def calculate_mac(pattern, weights):
    res = 0
    for i, j in zip(pattern, weights):
        for k, l in zip(i, j):
            res += k*l

    return res

def decide_label(a_score, b_score, a_label, b_label, epsilon=1e-9):
    if abs(a_score-b_score) < epsilon:
        return "판정 불가"

    return a_label if a_score > b_score else b_label
