from __future__ import annotations
from typing import List, Tuple
import math


def _find_r_for_n(n: int) -> int:
    """
    Знаходимо r так, що 2^r <= n <= 2^(r+1)
    """
    if n <= 0:
        raise ValueError("n має бути > 0.")
    r = 0
    # поки 2^(r+1) < n, збільшуємо r
    while (2 ** (r + 1)) < n:
        r += 1
    # тепер 2^r <= n <= 2^(r+1) повинно виконуватись
    return r


def build_intervals(sample: List[int]) -> Tuple[List[Tuple[float, float]], List[float], List[int], List[float]]:
    """
    Створює інтервальний ряд для цілих даних.

    Повертає:
      intervals: [(a0,a1), (a1,a2), ..., останній - закритий]
      zi:        середини інтервалів (a_{i-1}+a_i)/2
      ni:        абсолютні частоти
      wi:        відносні частоти
    """
    if len(sample) == 0:
        raise ValueError("Порожня вибірка.")
    n = len(sample)

    r = _find_r_for_n(n)
    k = r + 1  # за вимогою

    mn = sample[0]
    mx = sample[0]
    for x in sample:
        if x < mn:
            mn = x
        if x > mx:
            mx = x

    # Ширина:
    if k <= 0:
        raise ValueError("k <= 0.")
    width = (mx - mn) / float(k)
    if width == 0:
        # всі значення однакові -> робимо один "інтервал" ширини 1
        width = 1.0

    # Межі інтервалів
    bounds: List[float] = [float(mn)]
    for i in range(1, k + 1):
        bounds.append(float(mn) + width * i)

    intervals: List[Tuple[float, float]] = []
    zi: List[float] = []
    ni: List[int] = [0 for _ in range(k)]

    for i in range(k):
        a0 = bounds[i]
        a1 = bounds[i + 1]
        intervals.append((a0, a1))
        zi.append((a0 + a1) / 2.0)

    # Підрахунок ni:
    # [a_{i-1}, a_i) для всіх, а останній інтервал включає праву межу.
    for x in sample:
        placed = False
        xf = float(x)
        for i in range(k):
            a0, a1 = intervals[i]
            if i < k - 1:
                if (xf >= a0) and (xf < a1):
                    ni[i] += 1
                    placed = True
                    break
            else:
                if (xf >= a0) and (xf <= a1):
                    ni[i] += 1
                    placed = True
                    break
        if not placed:
            ni[k - 1] += 1

    wi: List[float] = []
    for f in ni:
        wi.append(f / n)

    return intervals, zi, ni, wi


def simplified_mode_interval(zi: List[float], ni: List[int]) -> List[float]:
    """
    Спрощена Mo для інтервального: повертає ВСІ моди як середини інтервалів z_i,
    для яких n_i максимальна.
    """
    if len(zi) == 0:
        raise ValueError("Немає інтервалів.")
    if len(zi) != len(ni):
        raise ValueError("zi і ni різної довжини.")

    # 1) max частота
    max_f = ni[0]
    for f in ni:
        if f > max_f:
            max_f = f

    # 2) усі z_i з max частотою
    res: List[float] = []
    for i in range(len(ni)):
        if ni[i] == max_f:
            res.append(zi[i])

    return res


def simplified_median_interval(zi: List[float], ni: List[int]) -> float:
    """Спрощена Me для інтервального: середина медіанного інтервалу."""
    n = 0
    for f in ni:
        n += f
    if n == 0:
        raise ValueError("n=0.")
    half = n / 2.0

    cum = 0
    for i in range(len(ni)):
        cum += ni[i]
        if cum >= half:
            return zi[i]
    return zi[-1]


def empirical_cdf_grouped(intervals: List[Tuple[float, float]], ni: List[int]) -> Tuple[List[float], List[float]]:
    n = 0
    for f in ni:
        n += f
    if n == 0:
        raise ValueError("n=0.")

    # стартова точка: ліва межа першого інтервалу, F=0
    x0 = intervals[0][0]
    xs: List[float] = [x0]
    Fs: List[float] = [0.0]

    cum = 0
    for i in range(len(intervals)):
        cum += ni[i]
        right = intervals[i][1]
        xs.append(right)
        Fs.append(cum / n)

    return xs, Fs