from __future__ import annotations
from typing import List, Tuple
import math


# допоміжна функція для підрахунку суми частот
def _total_n(freq: List[int]) -> int:
    s = 0
    for f in freq:
        s += f
    return s


# -------------- Локаційні ----------------------------------------
def arithmetic_mean(values: List[float], freq: List[int]) -> float:
    """
    x̄ = (1/n) * Σ n_i * x_i
    """
    n = _total_n(freq)
    if n == 0:
        raise ValueError("НЕМА частот (n=0).")

    s = 0.0
    for i in range(len(values)):
        s += float(freq[i]) * float(values[i])
    return s / float(n)


def median(sorted_sample: List[int]) -> float:
    """
    Me для впорядкованої вибірки:
      n=2m+1 => x_{m+1}
      n=2m   => (x_m + x_{m+1})/2
    """
    n = len(sorted_sample)
    if n == 0:
        raise ValueError("Порожня вибірка.")

    if n % 2 == 1:
        return float(sorted_sample[n // 2])
    else:
        left = sorted_sample[n // 2 - 1]
        right = sorted_sample[n // 2]
        return (float(left) + float(right)) / 2.0


def modes(values: List[float], freq: List[int]) -> List[float]:
    """
    Повертає ВСІ моди (всі x_i з максимальною частотою).
    """
    if len(values) == 0:
        raise ValueError("Немає значень для моди.")
    if len(values) != len(freq):
        raise ValueError("values і freq різної довжини.")

    # 1) максимальна частота
    max_f = freq[0]
    for f in freq:
        if f > max_f:
            max_f = f

    # 2) усі значення з цією частотою
    res: List[float] = []
    for i in range(len(freq)):
        if freq[i] == max_f:
            res.append(float(values[i]))

    return res


# -------------- Розсіювання ----------------------------------------
def sample_range(sample: List[int]) -> int:
    """
    ρ = max(x) - min(x) 
    """
    if len(sample) == 0:
        raise ValueError("Порожня вибірка.")
    mn = sample[0]
    mx = sample[0]
    for x in sample:
        if x < mn:
            mn = x
        if x > mx:
            mx = x
    return mx - mn


def dispersion_D(values: List[float], freq: List[int], mean: float) -> float:
    """
    D = (1/n) * Σ n_i (x_i - x̄)^2
    """
    n = _total_n(freq)
    if n == 0:
        raise ValueError("n=0.")

    s = 0.0
    for i in range(len(values)):
        d = float(values[i]) - mean
        s += float(freq[i]) * d * d
    return s / float(n)


def variance_S2(values: List[float], freq: List[int], mean: float, n: int) -> float:
    """
    S^2 = (1/(n-1)) * Σ n_i (x_i - x̄)^2   (виправлена вибіркова дисперсія)
    
    """
    if n <= 1:
        raise ValueError("Для S^2 потрібно n>1.")

    s = 0.0
    for i in range(len(values)):
        d = float(values[i]) - mean
        s += float(freq[i]) * d * d
    return s / float(n - 1)


def standard_S(s2: float) -> float:
    """S = sqrt(S^2) (беремо додатній корінь) стандарт"""
    if s2 < 0: 
        if s2 > -1e-12:
            s2 = 0.0
        else:
            raise ValueError("S^2 < 0, перевірте обчислення.")
    return math.sqrt(s2)


def variation(s: float, mean: float) -> float:
    """v = s / x̄ """
    if mean == 0:
        raise ValueError("якщо x̄ = 0, v = s/x̄ не визначена.")
    return s / mean


# -------------- Моменти ------------------------------------------------
def initial_moment(values: List[float], freq: List[int], k: int) -> float:
    """
    m_k = (1/n) * Σ n_i * x_i^k
    """
    if k < 0:
        raise ValueError("Порядок моменту k має бути >= 0.")
    n = _total_n(freq)
    if n == 0:
        raise ValueError("n=0.")

    s = 0.0
    for i in range(len(values)):
        s += float(freq[i]) * (float(values[i]) ** k)
    return s / float(n)


def central_moment(values: List[float], freq: List[int], mean: float, k: int) -> float:
    """
    μ_k = (1/n) * Σ n_i * (x_i - x̄)^k
    """
    if k < 0:
        raise ValueError("Порядок моменту k має бути >= 0.")
    n = _total_n(freq)
    if n == 0:
        raise ValueError("n=0.")

    s = 0.0
    for i in range(len(values)):
        d = float(values[i]) - mean
        s += float(freq[i]) * (d ** k)
    return s / float(n)


# -------------- Форма -----------------------------------
def asymmetry(mu2: float, mu3: float) -> float:
    """
    A = μ3 / μ2^(3/2)
    """
    if mu2 == 0:
        raise ValueError("μ2 = 0, асиметрія не визначена.")
    denom = mu2 ** 1.5
    return mu3 / denom


def excess(mu2: float, mu4: float) -> float:
    """
    E = μ4 / μ2^2 - 3
    """
    if mu2 == 0:
        raise ValueError("μ2 = 0, ексцес не визначений.")
    return (mu4 / (mu2 * mu2)) - 3.0