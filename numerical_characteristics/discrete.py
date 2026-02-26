from __future__ import annotations
from typing import List, Tuple


def build_variation_series(sample: List[int]) -> Tuple[List[int], List[int], List[float], List[int]]:
    """
    Повертає:
      sorted_sample — варіаційний ряд (впорядкована вибірка)
      values        — унікальні значення (за зростанням)
      rel_freq      — відносні частоти w_i
      freq          — абсолютні частоти n_i
    """
    if len(sample) == 0:
        raise ValueError("Порожня вибірка.")

    sorted_sample = sorted(sample) # Timsort = merge + insertion, O(n log n)

    # Підрахунок абсолютних частот (вручну без Counter з collections)
    values: List[int] = []
    freq: List[int] = []

    current = sorted_sample[0]
    count = 1
    for i in range(1, len(sorted_sample)):
        if sorted_sample[i] == current:
            count += 1
        else:
            values.append(current)
            freq.append(count)
            current = sorted_sample[i]
            count = 1
    values.append(current)
    freq.append(count)

    # Підрахунок відносних частот
    n = len(sorted_sample)
    rel_freq: List[float] = []
    for f in freq:
        rel_freq.append(f / n)

    return sorted_sample, values, rel_freq, freq


def empirical_cdf_discrete(values: List[int], freq: List[int]) -> Tuple[float, float, List[Tuple[float, float, float]]]:
    """
    Емпірична ФР для дискретного розподілу:
    повертає:
      x_left, x_right — межі для "хвостів" 0 і 1
      segments — список горизонтальних відрізків (x0, x1, y)
    де:
      - на [x_left, x1] рівень 0
      - на [x_i, x_{i+1}] рівень F_i
      - на [x_k, x_right] рівень 1
    """
    n = 0
    for f in freq:
        n += f
    if n == 0:
        raise ValueError("n = 0")

    # кумулятивні відносні частоти F_i
    cum: List[float] = []
    s = 0.0
    for f in freq:
        s += f / n
        cum.append(s)

    x_first = float(values[0])
    x_last = float(values[-1])

    # невеликі "поля" зліва/справа, щоб було видно 0 і 1
    left_pad = 1.0
    right_pad = 1.0
    x_left = x_first - left_pad
    x_right = x_last + right_pad

    segments: List[Tuple[float, float, float]] = []

    # 0 до першого значення
    segments.append((x_left, x_first, 0.0))

    # основні сходинки
    for i in range(len(values)):
        x0 = float(values[i])
        y = cum[i]
        if i < len(values) - 1:
            x1 = float(values[i + 1])
        else:
            x1 = x_right  # після останнього
        segments.append((x0, x1, y))

    return x_left, x_right, segments