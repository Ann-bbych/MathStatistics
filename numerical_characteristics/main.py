from __future__ import annotations

import os
from datetime import datetime
import matplotlib.pyplot as plt
from output import DualOutput
from generation import generate_sample
from discrete import build_variation_series, empirical_cdf_discrete
from grouped import build_intervals, empirical_cdf_grouped
from report import (
    print_discrete_table,
    print_grouped_table,
    print_characteristics_discrete,
    print_characteristics_grouped,
) 
from plots import (
    plot_frequency_polygon,
    plot_relative_frequency_polygon,
    plot_empirical_cdf_discrete,
    plot_histogram_density,
    plot_empirical_cdf_grouped,
)

SHOW_PLOTS = True  

# Базова папка проекту
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Папка output
OUTPUT_ROOT = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_ROOT, exist_ok=True)


def main() -> None:
    # Створюємо унікальну папку для кожного запуску
    run_name = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    RUN_DIR = os.path.join(OUTPUT_ROOT, run_name)
    os.makedirs(RUN_DIR, exist_ok=True)
    
    # Ввід
    print("РЕКОМЕНДАЦІЯ:\nмає виконуватись b - a <= 10\n")

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

    print_characteristics_discrete(out, sorted_sample, values, freq, sample)

    # Графіки
    plot_frequency_polygon(
        values,
        freq,
        "Полігон частот",
        os.path.join(RUN_DIR, "frequency_polygon.png"),
        SHOW_PLOTS
    )
    plot_relative_frequency_polygon(
        values,
        rel_freq,
        "Полігон відносних частот",
        os.path.join(RUN_DIR, "relative_frequency_polygon.png"),
        SHOW_PLOTS
    )
    x_left, x_right, segments = empirical_cdf_discrete(values, freq)

    plot_empirical_cdf_discrete(
        x_left,
        x_right,
        segments,
        "Емпірична ФР (дискретна)",
        os.path.join(RUN_DIR, "cdf_discrete.png"),
        SHOW_PLOTS
    )


    # Інтервальна частина -------------------------------------------------
    out.line("ЗАВДАННЯ 2. ІНТЕРВАЛЬНИЙ РОЗПОДІЛ\n")
    intervals, zi, ni, wi = build_intervals(sample)
    print_grouped_table(out, intervals, zi, ni, wi)

    print_characteristics_grouped(out, zi, ni, wi, sample)

    # Гістограма (з wi)
    plot_histogram_density(
    intervals,
    wi,
    "Гістограма",
    os.path.join(RUN_DIR, "histogram.png"),
    SHOW_PLOTS
    )

    # Емпірична ФР (інтервальна)
    xs_g, Fs_g = empirical_cdf_grouped(intervals, ni)
    
    a_int = intervals[0][0]      # ліва межа першого інтервалу
    b_int = intervals[-1][1]     # права межа останнього інтервалу
    
    plot_empirical_cdf_grouped(
    xs_g, Fs_g,
    "Емпірична ФР (інтервальна)",
    os.path.join(RUN_DIR, "cdf_grouped.png"),
    a_int, b_int,
    SHOW_PLOTS
    )
    
    # Показати графіки інтерактивно
    if SHOW_PLOTS:
        plt.show()
        plt.close("all")
        
    out.close()

if __name__ == "__main__":
    main()