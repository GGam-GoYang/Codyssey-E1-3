def run_user():
    filter_a = read_matrix("필터 A")
    filter_b = read_matrix("필터 B")

    print("필터 저장 완료")

    pattern = read_matrix("패턴")

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