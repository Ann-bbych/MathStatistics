# =========================
# file: discrete.py
# =========================
from __future__ import annotations
from typing import Dict, List, Tuple


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

    sorted_sample = sorted(sample)

    # Підрахунок частот вручну (без Counter — теж можна, але так прозоріше)
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

    n = len(sorted_sample)
    rel_freq: List[float] = []
    for f in freq:
        rel_freq.append(f / n)

    return sorted_sample, values, rel_freq, freq


def empirical_cdf_discrete(values: List[int], freq: List[int]) -> Tuple[List[int], List[float]]:
    """
    Емпірична ФР для дискретного ряду:
    Повертає точки (x, F(x)) у вигляді списків.
    Тут F(x_i) = (Σ_{j<=i} n_j) / n.
    """
    n = 0
    for f in freq:
        n += f
    if n == 0:
        raise ValueError("n=0.")

    xs: List[int] = []
    Fs: List[float] = []
    cum = 0
    for i in range(len(values)):
        cum += freq[i]
        xs.append(values[i])
        Fs.append(cum / n)
    return xs, Fs