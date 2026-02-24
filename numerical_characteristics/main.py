# =========================
# file: main.py
# =========================
from __future__ import annotations
from typing import List, Tuple
import matplotlib.pyplot as plt

from output import DualOutput, format_num
from generation import generate_sample
from discrete import build_variation_series, empirical_cdf_discrete
from grouped import (
    build_intervals,
    simplified_mode_interval,
    simplified_median_interval,
    empirical_cdf_grouped,
)
from calculations import (
    arithmetic_mean,
    sample_range,
    median,
    mode,
    dispersion_D,
    variance_S2,
    standard_S,
    variation,
    initial_moment,
    central_moment,
    asymmetry,
    excess,
)


# ---------- Графіки ----------
def plot_frequency_polygon(values: List[int], freq: List[int], title: str) -> None:
    plt.figure()
    plt.plot(values, freq, marker="o")
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("n_i")
    plt.grid(True)


def plot_relative_frequency_polygon(values: List[int], rel_freq: List[float], title: str) -> None:
    plt.figure()
    plt.plot(values, rel_freq, marker="o")
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("w_i")
    plt.grid(True)


def plot_empirical_cdf(xs: List[float], Fs: List[float], title: str) -> None:
    plt.figure()
    # для дискретної зручно робити ступінчастий графік:
    plt.step(xs, Fs, where="post")
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("F_n(x)")
    plt.ylim(0.0, 1.05)
    plt.grid(True)


def plot_histogram_counts(intervals: List[Tuple[float, float]], ni: List[int], title: str) -> None:
    plt.figure()
    lefts = []
    widths = []
    for (a0, a1) in intervals:
        lefts.append(a0)
        widths.append(a1 - a0)

    # стовпчики за інтервалами: висота = ni
    plt.bar(lefts, ni, width=widths, align="edge")
    plt.title(title)
    plt.xlabel("Інтервали (ліва межа)")
    plt.ylabel("n_i")
    plt.grid(True)


# ---------- Вивід таблиць ----------
def print_discrete_table(out: DualOutput, values: List[int], freq: List[int], rel_freq: List[float]) -> None:
    out.line("Частотна таблиця (дискретна):")
    out.line("x_i\t\tn_i\t\tw_i")
    for i in range(len(values)):
        out.line(f"{values[i]}\t\t{freq[i]}\t\t{format_num(rel_freq[i])}")
    out.line()


def print_grouped_table(out: DualOutput, intervals: List[Tuple[float, float]], zi: List[float], ni: List[int], wi: List[float]) -> None:
    out.line("Інтервальна таблиця (згруповані дані):")
    out.line("[a_{i-1}; a_i)\t\tz_i\t\tn_i\t\tw_i")
    for i in range(len(intervals)):
        a0, a1 = intervals[i]
        out.line(f"[{format_num(a0)}; {format_num(a1)})\t\t{format_num(zi[i])}\t\t{ni[i]}\t\t{format_num(wi[i])}")
    out.line()


# ---------- Розрахунок і друк характеристик ----------
def print_characteristics_discrete(out: DualOutput, sample_sorted: List[int], values: List[int], freq: List[int], sample: List[int]) -> None:
    # Для calculations використовуємо values як float
    values_f = [float(x) for x in values]
    n = len(sample)

    xbar = arithmetic_mean(values_f, freq)
    rho = sample_range(sample)
    Mo = mode(values_f, freq)
    Me = median(sample_sorted)

    D = dispersion_D(values_f, freq, xbar)
    S2 = variance_S2(values_f, freq, xbar, n)
    S = standard_S(S2)
    v = variation(S, xbar)

    # моменти m1..m4, μ1..μ4 (через суму)
    m = {}
    mu = {}
    for k in range(1, 5):
        m[k] = initial_moment(values_f, freq, k)
        mu[k] = central_moment(values_f, freq, xbar, k)

    A = asymmetry(mu[2], mu[3])
    E = excess(mu[2], mu[4])

    out.line("Статистики локації:")
    out.line(f"  Mo = {format_num(Mo)}")
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

    # повернемо для аналізу (не обов'язково, але зручно)
    return {
        "xbar": xbar, "rho": rho, "Mo": Mo, "Me": Me,
        "D": D, "S2": S2, "S": S, "v": v,
        "m": m, "mu": mu, "A": A, "E": E
    }


def print_characteristics_grouped(out: DualOutput, zi: List[float], ni: List[int], wi: List[float], sample: List[int]) -> None:
    # "Спрощено": трактуємо (z_i, n_i) як дискретний ряд
    n = 0
    for f in ni:
        n += f

    xbar = arithmetic_mean(zi, ni)
    rho = sample_range(sample)  # за домовленістю по реальній вибірці

    Mo = simplified_mode_interval(zi, ni)
    Me = simplified_median_interval(zi, ni)

    D = dispersion_D(zi, ni, xbar)
    S2 = variance_S2(zi, ni, xbar, n)
    S = standard_S(S2)
    v = variation(S, xbar)

    m = {}
    mu = {}
    for k in range(1, 5):
        m[k] = initial_moment(zi, ni, k)
        mu[k] = central_moment(zi, ni, xbar, k)

    A = asymmetry(mu[2], mu[3])
    E = excess(mu[2], mu[4])

    out.line("Статистики локації (згруповані дані, спрощено):")
    out.line(f"  Mo_int = {format_num(Mo)}")
    out.line(f"  Me_int = {format_num(Me)}")
    out.line(f"  x̄_int  = {format_num(xbar)}")
    out.line()

    out.line("Статистики розсіювання (згруповані дані):")
    out.line(f"  ρ  = {rho}")
    out.line(f"  D  = {format_num(D)}")
    out.line(f"  S² = {format_num(S2)}")
    out.line(f"  S  = {format_num(S)}")
    out.line(f"  v  = {format_num(v)}")
    out.line()

    out.line("Моменти статистичної зміни (згруповані дані):")
    for k in range(1, 5):
        out.line(f"  m{k}  = {format_num(m[k])}")
    for k in range(1, 5):
        out.line(f"  μ{k}  = {format_num(mu[k])}")
    out.line()

    out.line("Статистики форми (згруповані дані):")
    out.line(f"  A = {format_num(A)}")
    out.line(f"  E = {format_num(E)}")
    out.line()

    return {
        "xbar": xbar, "rho": rho, "Mo": Mo, "Me": Me,
        "D": D, "S2": S2, "S": S, "v": v,
        "m": m, "mu": mu, "A": A, "E": E
    }


def print_analysis(out: DualOutput, disc: dict, grp: dict) -> None:
    """
    Аналіз результатів (скелет).
    Ти зможеш доповнити, або я розширю з урахуванням конкретних чисел.
    """
    out.line("АНАЛІЗ РЕЗУЛЬТАТІВ (скелет):")
    out.line("1) Порівняння локації:")
    out.line(f"   Дискретно: x̄={format_num(disc['xbar'])}, Me={format_num(disc['Me'])}, Mo={format_num(disc['Mo'])}")
    out.line(f"   Інтервально: x̄≈{format_num(grp['xbar'])}, Me≈{format_num(grp['Me'])}, Mo≈{format_num(grp['Mo'])}")
    out.line("   Пояснення: інтервальні оцінки наближені, бо використовують середини інтервалів z_i.")
    out.line()

    out.line("2) Розсіювання:")
    out.line(f"   ρ (по вибірці) = {disc['rho']}")
    out.line(f"   S (дискретно) = {format_num(disc['S'])}, S (інтервально) ≈ {format_num(grp['S'])}")
    out.line("   Якщо S інтервально трохи відрізняється — це нормально через групування.")
    out.line()

    out.line("3) Форма розподілу:")
    out.line(f"   A (асиметрія): дискретно {format_num(disc['A'])}, інтервально ≈ {format_num(grp['A'])}")
    out.line(f"   E (ексцес):    дискретно {format_num(disc['E'])}, інтервально ≈ {format_num(grp['E'])}")
    out.line("   Інтерпретація: знак A показує напрям асиметрії, E — “гостровершинність/плосковершинність” відносно нормального.")
    out.line()


def main() -> None:
    # 1) Ввід
    print("Рекомендація: для кращої наочності бажано, щоб b - a <= 10 (це не є обмеженням).")
    n = int(input("Введіть n (>=100): ").strip())
    a = int(input("Введіть a (ліва межа, ціле): ").strip())
    b = int(input("Введіть b (права межа, ціле): ").strip())

    file_path = input("Введіть назву файлу для результатів (наприклад result.txt), або Enter щоб пропустити: ").strip()
    if file_path == "":
        file_path = "result.txt"  # можна залишити за замовчуванням, або зробити None

    out = DualOutput(file_path)

    # 2) Генерація
    sample = generate_sample(n, a, b)
    out.line("Input (згенеровані дані):")
    out.line(f"n={n}, a={a}, b={b}")
    out.line("Перші 30 елементів вибірки (для контролю):")
    preview = sample[:30]
    out.line(" ".join(str(x) for x in preview))
    out.line()

    # 3) Дискретна частина
    out.line("========================================")
    out.line("ЧАСТИНА 1. ДИСКРЕТНИЙ РОЗПОДІЛ")
    out.line("========================================")
    sorted_sample, values, rel_freq, freq = build_variation_series(sample)

    out.line("Варіаційний ряд (перші 50 значень):")
    out.line(" ".join(str(x) for x in sorted_sample[:50]))
    out.line()

    print_discrete_table(out, values, freq, rel_freq)

    disc_stats = print_characteristics_discrete(out, sorted_sample, values, freq, sample)

    # Графіки (дискретні)
    plot_frequency_polygon(values, freq, "Полігон частот (дискретний)")
    plot_relative_frequency_polygon(values, rel_freq, "Полігон відносних частот (дискретний)")
    xs_d, Fs_d = empirical_cdf_discrete(values, freq)
    plot_empirical_cdf([float(x) for x in xs_d], Fs_d, "Емпірична ФР (дискретна)")

    # 4) Інтервальна частина
    out.line("========================================")
    out.line("ЧАСТИНА 2. ІНТЕРВАЛЬНИЙ (ЗГРУПОВАНИЙ) РОЗПОДІЛ")
    out.line("========================================")
    intervals, zi, ni, wi = build_intervals(sample)
    print_grouped_table(out, intervals, zi, ni, wi)

    grp_stats = print_characteristics_grouped(out, zi, ni, wi, sample)

    # Гістограма (за ni — як ти вирішила)
    plot_histogram_counts(intervals, ni, "Гістограма частот (n_i)")

    # Емпірична ФР (інтервальна)
    xs_g, Fs_g = empirical_cdf_grouped(intervals, ni)
    plot_empirical_cdf(xs_g, Fs_g, "Емпірична ФР (інтервальна)")

    # 5) Аналіз
    out.line("========================================")
    out.line("АНАЛІЗ")
    out.line("========================================")
    print_analysis(out, disc_stats, grp_stats)

    out.close()

    # Показати графіки
    plt.show()


if __name__ == "__main__":
    main()