from time import perf_counter
from calculator import calculate_mac

REPEATS = 10


def average_time(pattern, weights, repeats=REPEATS, function=calculate_mac):
    """MAC 평균 ms 반환. pattern/weights: 검증된 배열, repeats: 양의 반복 수, function: 계산 함수.
    입력·검증·변환·출력은 호출 전에 끝낸다. 타이머는 함수 호출 구간만 감싼다.
    """
    if isinstance(repeats, bool) or not isinstance(repeats, int) or repeats <= 0:
        raise ValueError("반복 횟수는 양의 정수여야 합니다.")
    total_seconds = 0.0
    for _ in range(repeats):
        start = perf_counter()
        function(pattern, weights)
        total_seconds += perf_counter() - start
    return total_seconds / repeats * 1000


def print_performance(samples, labels=("Cross", "X"), repeats=REPEATS):
    """크기별·필터별 평균 시간 출력. samples: {n: (패턴, 필터A, 필터B)}. 반환: 측정 행 리스트."""
    print(f"\n[성능 분석 / 각 {repeats}회 평균 / 필터 한 개당 N^2 MAC]")
    print("크기 | 필터 | 평균 시간(ms) | MAC 횟수")
    rows = []
    for n in sorted(samples):
        pattern, filter_a, filter_b = samples[n]
        for label, weights in zip(labels, (filter_a, filter_b)):
            elapsed = average_time(pattern, weights, repeats)
            rows.append((n, label, elapsed, n * n))
            print(f"{n}x{n} | {label} | {elapsed:.6f} | {n*n}")
    return rows


def prepare_samples(samples):
    """JSON 성능 표용 자료 보완. samples: 정상 배열 묶음. 반환: 3/5/13/25 크기 자료.
    자료가 없는 크기는 1로 채운 측정 전용 배열을 쓴다. 케이스 판정에는 넣지 않는다.
    """
    prepared = dict(samples)
    for n in (3, 5, 13, 25):
        if n not in prepared:
            pattern = [[1.0] * n for _ in range(n)]
            weights = [[1.0] * n for _ in range(n)]
            prepared[n] = (pattern, weights, weights)
            print(f"size_{n}: 측정 전용 배열 사용 (판정 집계 제외)")
    return prepared
