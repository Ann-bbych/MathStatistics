from __future__ import annotations

import os
from datetime import datetime
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
SHOW_PLOTS = True  

# Базова папка проекту (там де лежить main.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Папка output
OUTPUT_ROOT = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_ROOT, exist_ok=True)


# ---------- Графіки ---------------------------------------------------
def plot_frequency_polygon(values, freq, title, save_path):
    plt.figure()
    plt.plot(values, freq, marker="o")
    plt.title(title)
    plt.xlabel(r"$x_i$")
    plt.ylabel(r"$n_i$")
    plt.grid(True)
    plt.savefig(save_path)
    if not SHOW_PLOTS:
        plt.close()


def plot_relative_frequency_polygon(values, rel_freq, title, save_path):
    plt.figure()
    plt.plot(values, rel_freq, marker="o")
    plt.title(title)
    plt.xlabel(r"$x_i$")
    plt.ylabel(r"$w_i$")
    plt.grid(True)
    plt.savefig(save_path)
    if not SHOW_PLOTS:
        plt.close()


def plot_empirical_cdf(xs, Fs, title, save_path):
    plt.figure()
    plt.step(xs, Fs, where="post")
    plt.title(title)
    plt.xlabel(r"$x_i$")
    plt.ylabel(r"$\tilde{F}(x)$")
    plt.ylim(0.0, 1.05)
    plt.grid(True)
    plt.savefig(save_path)
    if not SHOW_PLOTS:
        plt.close()


def plot_histogram_density(intervals, wi, title, save_path):
    plt.figure()

    lefts = []
    widths = []
    heights = []

    for i in range(len(intervals)):
        a0, a1 = intervals[i]
        width = a1 - a0

        lefts.append(a0)
        widths.append(width)
        heights.append(wi[i] / width)   # hi

    plt.bar(lefts, heights, width=widths, align="edge")

    plt.title(title)
    plt.xlabel(r"$a_i$")
    plt.ylabel(r"$h_i=\dfrac{w_i}{a_i-a_{i-1}}$")
    plt.grid(True)

    plt.savefig(save_path)

    if not SHOW_PLOTS:
        plt.close()


def plot_empirical_cdf_grouped(xs, Fs, title, save_path):
    plt.figure()
    plt.plot(xs, Fs, marker="o")   # лінійна огіва
    plt.title(title)
    plt.xlabel(r"$x_i$")
    plt.ylabel(r"$\tilde{F}(x)$")
    plt.ylim(0.0, 1.05)
    plt.grid(True)
    plt.savefig(save_path)
    if not SHOW_PLOTS:
        plt.close()


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


# ---------- Розрахунок і друк числових характеристик ---------------------------------------------------------------------------------------
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

    # моменти через суму
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

    # поверне для аналізу
    return {
        "xbar": xbar, "rho": rho, "Mo": Mo, "Me": Me,
        "D": D, "S2": S2, "S": S, "v": v,
        "m": m, "mu": mu, "A": A, "E": E
    }


def print_characteristics_grouped(out: DualOutput, zi: List[float], ni: List[int], wi: List[float], sample: List[int]) -> None:
    # трактуємо (z_i, n_i) як дискретний ряд
    n = 0
    for f in ni:
        n += f

    xbar = arithmetic_mean(zi, ni)
    rho = sample_range(sample)  

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

    return {
        "xbar": xbar, "rho": rho, "Mo": Mo, "Me": Me,
        "D": D, "S2": S2, "S": S, "v": v,
        "m": m, "mu": mu, "A": A, "E": E
    }

# -------- Аналіз результатів -------------------------------------------------------------------------------------------------------
def print_analysis(out: DualOutput, disc: dict, grp: dict) -> None:
    """
    Аналіз результатів: порівняння дискретного та інтервального розподілу, інтерпретація статистик.
    """
    out.line("АНАЛІЗ РЕЗУЛЬТАТІВ:")
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
    # Створюємо унікальну папку для кожного запуску
    run_name = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    RUN_DIR = os.path.join(OUTPUT_ROOT, run_name)
    os.makedirs(RUN_DIR, exist_ok=True)
    
    # Ввід
    print("РЕКОМЕНДАЦІЯ:\nдля кращої наочності має виконуватись\nb - a <= 10\n")

    while True:
        try:
            n = int(input("Введіть n (>=100): ").strip())
            a = int(input("Введіть a (ліва межа, ціле): ").strip())
            b = int(input("Введіть b (права межа, ціле): ").strip())
            # Генерація
            sample = generate_sample(n, a, b)  # кидає ValueError
            break 

        except ValueError as e:
            print(f"Помилка вводу: {e}")
            print("Спробуйте ще раз.\n")
    
    # result.txt автоматично в папці run
    result_path = os.path.join(RUN_DIR, "result.txt")
    out = DualOutput(result_path)
    
    out.line("\nЗГЕНЕРОВАНА ВИБІРКА:")
    out.line("(перші 30 елементів для контролю)")
    preview = sample[:30]
    out.line(" ".join(str(x) for x in preview))
    out.line()

    # Дискретна частина ----------------------------------------------------------------
    out.line("ЗАВДАННЯ 1. ДИСКРЕТНИЙ РОЗПОДІЛ\n")
    sorted_sample, values, rel_freq, freq = build_variation_series(sample)

    out.line("Варіаційний ряд (перші 50 елементів):")
    out.line(" ".join(str(x) for x in sorted_sample[:50]))
    out.line()

    print_discrete_table(out, values, freq, rel_freq)

    disc_stats = print_characteristics_discrete(out, sorted_sample, values, freq, sample)

    # Графіки
    plot_frequency_polygon(
        values,
        freq,
        "Полігон частот",
        os.path.join(RUN_DIR, "frequency_polygon.png")
    )
    plot_relative_frequency_polygon(
        values,
        rel_freq,
        "Полігон відносних частот",
        os.path.join(RUN_DIR, "relative_frequency_polygon.png")
    )
    xs_d, Fs_d = empirical_cdf_discrete(values, freq)
    plot_empirical_cdf(
        [float(x) for x in xs_d],
        Fs_d,
        "Емпірична ФР (дискретна)",
        os.path.join(RUN_DIR, "cdf_discrete.png")
    )


    # Інтервальна частина -------------------------------------------------
    out.line("ЗАВДАННЯ 2. ІНТЕРВАЛЬНИЙ РОЗПОДІЛ\n")
    intervals, zi, ni, wi = build_intervals(sample)
    print_grouped_table(out, intervals, zi, ni, wi)

    grp_stats = print_characteristics_grouped(out, zi, ni, wi, sample)

    # Гістограма (з wi)
    plot_histogram_density(
    intervals,
    wi,
    "Гістограма",
    os.path.join(RUN_DIR, "histogram.png")
)

    # Емпірична ФР (інтервальна)
    xs_g, Fs_g = empirical_cdf_grouped(intervals, ni)

    plot_empirical_cdf_grouped(
        xs_g,
        Fs_g,
        "Емпірична ФР (інтервальна)",
        os.path.join(RUN_DIR, "cdf_grouped.png")
    )
    
    # Аналіз ------------------------------------------------------------
    print_analysis(out, disc_stats, grp_stats)
    
    # Показати графіки інтерактивно
    if SHOW_PLOTS:
        plt.show()
        plt.close("all")
        
    out.close()

if __name__ == "__main__":
    main()