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


def empirical_cdf_discrete(values: List[int], freq: List[int]) -> Tuple[List[float], List[float]]:
    # n = сума частот
    n = 0
    for f in freq:
        n += f
    if n == 0:
        raise ValueError("n = 0")

    # cum [ω_i = n_i / n] - перелік значень F(x) (кумулятивні сума відносних частот)
    cum = []
    s = 0.0
    for f in freq:
        s += f / n
        cum.append(s)

    # Побудова точок функції: x<=x1 => 0, x1<x<=x2 => ω1, ...
    xs: List[float] = [float(values[0])] + [float(v) for v in values]
    Fs: List[float] = [0.0] + cum
    return xs, Fs