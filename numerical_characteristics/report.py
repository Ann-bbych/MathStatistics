from __future__ import annotations
from typing import List, Tuple, Dict
from output import DualOutput, format_num
from calculations import (
    arithmetic_mean,
    sample_range,
    median,
    modes,
    dispersion_D,
    variance_S2,
    standard_S,
    variation,
    initial_moment,
    central_moment,
    asymmetry,
    excess,
)
from grouped import (
    simplified_mode_interval,
    simplified_median_interval,
)


# ------------------ Таблиці --------------------------------------------------------------------------------
def print_discrete_table(out: DualOutput, values: List[int], freq: List[int], rel_freq: List[float]) -> None:
    out.line("Частотна таблиця:")
    out.line("варіанти\t\tабсолютні частоти\tвідносні частоти")
    out.line("x_i\t\t\tn_i\t\t\tw_i")

    for i in range(len(values)):
        out.line(f"{values[i]}\t\t\t{freq[i]}\t\t\t{format_num(rel_freq[i])}")

    out.line()


def print_grouped_table(out: DualOutput,
                        intervals: List[Tuple[float, float]],
                        zi: List[float],
                        ni: List[int],
                        wi: List[float]) -> None:
    out.line("Таблиця інтервального розподілу:")
    out.line(f"{'інтервали':<18} {'середини інтервалів':<20} {'абсолютні частоти':<20} {'відносні частоти':<18}")
    out.line(f"{'[a_{i-1}; a_i)':<18} {'z_i':<20} {'n_i':<20} {'w_i':<18}")

    last = len(intervals) - 1
    for i in range(len(intervals)):
        a0, a1 = intervals[i]
        if i == last:
            inter = f"[{format_num(a0)}; {format_num(a1)}]"
        else:
            inter = f"[{format_num(a0)}; {format_num(a1)})"

        out.line(f"{inter:<18} {format_num(zi[i]):<20} {ni[i]:<20} {format_num(wi[i]):<18}")

    out.line()


# ---------- Розрахунок і друк числових характеристик --------------------------------------------------------
def print_characteristics_discrete(out: DualOutput,
                                   sample_sorted: List[int],
                                   values: List[int],
                                   freq: List[int],
                                   sample: List[int]) -> None:
    values_f = [float(x) for x in values]
    n = len(sample)

    xbar = arithmetic_mean(values_f, freq)
    rho = sample_range(sample)
    Mo_list = modes(values_f, freq)
    Me = median(sample_sorted)

    D = dispersion_D(values_f, freq, xbar)
    S2 = variance_S2(values_f, freq, xbar, n)
    S = standard_S(S2)
    v = variation(S, xbar)

    m: Dict[int, float] = {}
    mu: Dict[int, float] = {}
    for k in range(1, 5):
        m[k] = initial_moment(values_f, freq, k)
        mu[k] = central_moment(values_f, freq, xbar, k)

    A = asymmetry(mu[2], mu[3])
    E = excess(mu[2], mu[4])

    out.line("Статистики локації:")
    out.line("  Mo = " + ", ".join(format_num(x) for x in Mo_list))
    out.line(f"  Me = {format_num(Me)}")
    out.line(f"  x̄  = {format_num(xbar)}")
    out.line()

    out.line("Статистики розсіювання:")
    out.line(f"  ρ  = {rho}")
    out.line(f"  D  = {format_num(D)}")
    out.line(f"  S² = {format_num(S2)}")
    out.line(f"  S  = {format_num(S)}")
    out.line(f"  v  = {format_num(v)}")
    out.line()

    out.line("Моменти статистичної зміни:")
    for k in range(1, 5):
        out.line(f"  m{k}  = {format_num(m[k])}")
    for k in range(1, 5):
        out.line(f"  μ{k}  = {format_num(mu[k])}")
    out.line()

    out.line("Статистики форми:")
    out.line(f"  A = {format_num(A)}")
    out.line(f"  E = {format_num(E)}")
    out.line()


def print_characteristics_grouped(out: DualOutput,
                                  zi: List[float],
                                  ni: List[int],
                                  wi: List[float],
                                  sample: List[int]) -> None:
    n = 0
    for f in ni:
        n += f

    xbar = arithmetic_mean(zi, ni)
    rho = sample_range(sample)

    Mo_list = simplified_mode_interval(zi, ni)
    Me = simplified_median_interval(zi, ni)
    
    D = dispersion_D(zi, ni, xbar)
    S2 = variance_S2(zi, ni, xbar, n)
    S = standard_S(S2)
    v = variation(S, xbar)

    m: Dict[int, float] = {}
    mu: Dict[int, float] = {}
    for k in range(1, 5):
        m[k] = initial_moment(zi, ni, k)
        mu[k] = central_moment(zi, ni, xbar, k)

    A = asymmetry(mu[2], mu[3])
    E = excess(mu[2], mu[4])

    out.line("Статистики локації:")
    out.line("  Mo = " + ", ".join(format_num(x) for x in Mo_list))
    out.line(f"  Me = {format_num(Me)}")
    out.line(f"  x̄  = {format_num(xbar)}")
    out.line()

    out.line("Статистики розсіювання:")
    out.line(f"  ρ  = {rho}")
    out.line(f"  D  = {format_num(D)}")
    out.line(f"  S² = {format_num(S2)}")
    out.line(f"  S  = {format_num(S)}")
    out.line(f"  v  = {format_num(v)}")
    out.line()

    out.line("Моменти статистичної зміни:")
    for k in range(1, 5):
        out.line(f"  m{k}  = {format_num(m[k])}")
    for k in range(1, 5):
        out.line(f"  μ{k}  = {format_num(mu[k])}")
    out.line()

    out.line("Статистики форми:")
    out.line(f"  A = {format_num(A)}")
    out.line(f"  E = {format_num(E)}")
    out.line()