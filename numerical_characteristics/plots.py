from __future__ import annotations

import matplotlib.pyplot as plt


def plot_frequency_polygon(values, freq, title, save_path, show_plots: bool):
    plt.figure()
    plt.plot(values, freq, marker="o")
    plt.title(title)
    plt.xlabel(r"$x_i$")
    plt.ylabel(r"$n_i$")
    plt.grid(True)
    plt.savefig(save_path)
    if not show_plots:
        plt.close()


def plot_relative_frequency_polygon(values, rel_freq, title, save_path, show_plots: bool):
    plt.figure()
    plt.plot(values, rel_freq, marker="o")
    plt.title(title)
    plt.xlabel(r"$x_i$")
    plt.ylabel(r"$w_i$")
    plt.grid(True)
    plt.savefig(save_path)
    if not show_plots:
        plt.close()


def plot_empirical_cdf_discrete(x_left, x_right, segments, title, save_path, show_plots: bool):
    plt.figure()
    plt.title(title)
    plt.xlabel(r"$x_i$")
    plt.ylabel(r"$\tilde{F}(x)$")
    plt.ylim(0.0, 1.05)
    plt.grid(True)
    
    # чорна точка старту (0-й рівень)
    x_first_real = segments[0][1]   # перше значення вибірки
    plt.plot([x_first_real], [0.0],
            marker="o",
            markersize=6,
            markerfacecolor="black",
            markeredgecolor="black")
    
    for i, (x0, x1, y) in enumerate(segments):
        plt.hlines(y, x0, x1, linewidth=2)

        if i == 0:
            continue

        if i == len(segments) - 1:
            plt.plot([x0], [y], marker="o", markersize=6,
                    markerfacecolor="white", markeredgecolor="black")
            continue

        # лівий — відкритий
        plt.plot([x0], [y], marker="o", markersize=6,
                markerfacecolor="white", markeredgecolor="black")

        # правий — закритий
        plt.plot([x1], [y], marker="o", markersize=6,
                markerfacecolor="black", markeredgecolor="black")

        plt.xlim(x_left, x_right)

    # підписи Ox тільки для x_i з вибірки
    ticks = []
    for (x0, x1, y) in segments:
        if x0 != x_left:
            ticks.append(float(x0))
    ticks = sorted(set(ticks))
    plt.xticks(ticks)

    plt.savefig(save_path)
    if not show_plots:
        plt.close()


def plot_histogram_density(intervals, wi, title, save_path, show_plots: bool):
    plt.figure()

    lefts = []
    widths = []
    heights = []

    for i in range(len(intervals)):
        a0, a1 = intervals[i]
        width = a1 - a0

        lefts.append(a0)
        widths.append(width)
        heights.append(wi[i] / width)   # h_i

    plt.bar(lefts, heights, width=widths, align="edge")

    plt.title(title)
    plt.xlabel(r"$a_i$")
    plt.ylabel(r"$h_i=\dfrac{w_i}{a_i-a_{i-1}}$")
    plt.grid(True)
    plt.savefig(save_path)

    if not show_plots:
        plt.close()


def plot_empirical_cdf_grouped(xs, Fs, title, save_path, a, b, show_plots: bool):
    plt.figure()

    plt.plot(xs, Fs, marker="o")

    plt.title(title)
    plt.xlabel(r"$a_i$")
    plt.ylabel(r"$\tilde{F}(x)$")
    plt.ylim(0.0, 1.05)
    plt.grid(True)

    a_f = float(a)
    b_f = float(b)
    pad = 0.10 * (b_f - a_f) if b_f > a_f else 1.0
    x_left = a_f - pad
    x_right = b_f + pad
    plt.xlim(x_left, x_right)
    plt.hlines(0.0, x_left, a_f, linewidth=2)
    plt.hlines(1.0, b_f, x_right, linewidth=2)

    ticks = sorted(set(float(x) for x in xs if a_f <= float(x) <= b_f))
    if a_f not in ticks:
        ticks = [a_f] + ticks
    if b_f not in ticks:
        ticks = ticks + [b_f]
    plt.xticks(ticks)

    plt.savefig(save_path)
    if not show_plots:
        plt.close()