import math
from calculator import calculate_mac, EPSILON
from performance import average_time


def flatten_matrix(matrix):
    """matrix: 2차원 리스트. 반환: 행 순서대로 펼친 새 1차원 리스트. 원본은 변경하지 않는다."""
    return [value for row in matrix for value in row]


def calculate_mac_flat(pattern, weights):
    """pattern/weights: 같은 길이의 1차원 리스트. 반환: float MAC 점수. 크기 검증은 호출 전에 한다."""
    total = 0.0
    for value, weight in zip(pattern, weights):
        total += value * weight
    if not math.isfinite(total):
        raise ValueError("MAC 결과가 유한한 숫자가 아닙니다!")
    return total


def compare_flat(samples, repeats=1000):
    """samples: {n: (패턴, 필터A, 필터B)}, repeats: 양쪽에 동일한 반복 수.
    반환: 비교 결과 딕셔너리 리스트. 변환 시간은 제외하고 별도로 표시한다.
    """
    from time import perf_counter
    print(f"\n[보너스 / 2차원 vs 1차원 / 각 {repeats}회 평균]")
    print("크기 | 필터 | 2차원 ms | 1차원 ms | 변환 ms | 점수 일치")
    rows = []
    for n in sorted(samples):
        pattern, filter_a, filter_b = samples[n]
        for label, weights in zip(("Cross", "X"), (filter_a, filter_b)):
            start = perf_counter()
            flat_pattern = flatten_matrix(pattern)
            flat_weights = flatten_matrix(weights)
            conversion_ms = (perf_counter() - start) * 1000
            a = calculate_mac(pattern, weights)
            b = calculate_mac_flat(flat_pattern, flat_weights)
            equal = abs(a - b) < EPSILON
            original = average_time(pattern, weights, repeats)
            flattened = average_time(flat_pattern, flat_weights, repeats, calculate_mac_flat)
            rows.append({"n": n, "label": label, "original_ms": original,
                         "flat_ms": flattened, "conversion_ms": conversion_ms, "equal": equal})
            print(f"{n}x{n} | {label} | {original:.6f} | {flattened:.6f} | {conversion_ms:.6f} | {equal}")
    return rows
