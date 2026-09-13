import math
import matplotlib.pyplot as plt


def get_histogram_bounds(bounds):
    histogram_bounds = bounds[:]

    if math.isinf(histogram_bounds[-1]):
        if len(histogram_bounds) < 3:
            raise ValueError("Недостатньо меж для побудови гістограми.")

        previous_width = histogram_bounds[-2] - histogram_bounds[-3]
        histogram_bounds[-1] = histogram_bounds[-2] + previous_width

    if math.isinf(histogram_bounds[0]):
        if len(histogram_bounds) < 3:
            raise ValueError("Недостатньо меж для побудови гістограми.")

        first_width = histogram_bounds[2] - histogram_bounds[1]
        histogram_bounds[0] = histogram_bounds[1] - first_width

    return histogram_bounds


def get_interval_labels(bounds):
    labels = []

    for i in range(len(bounds) - 1):
        left = bounds[i]
        right = bounds[i + 1]

        if math.isinf(left) and left < 0:
            left_text = "-∞"
            left_bracket = "("
        else:
            left_text = str(int(left)) if float(left).is_integer() else str(left)
            left_bracket = "["

        if math.isinf(right) and right > 0:
            right_text = "+∞"
            right_bracket = ")"
        else:
            right_text = str(int(right)) if float(right).is_integer() else str(right)
            right_bracket = ")"

        labels.append(f"{left_bracket}{left_text}; {right_text}{right_bracket}")

    return labels


def plot_histogram(bounds, frequencies, filename, title, figure_number):
    histogram_bounds = get_histogram_bounds(bounds)

    left_edges = []
    widths = []

    for i in range(len(frequencies)):
        left_edges.append(histogram_bounds[i])
        widths.append(histogram_bounds[i + 1] - histogram_bounds[i])

    plt.figure(figure_number, figsize=(12, 6))
    plt.bar(left_edges, frequencies, width=widths, align="edge", edgecolor="black")

    centers = []
    for i in range(len(frequencies)):
        centers.append((histogram_bounds[i] + histogram_bounds[i + 1]) / 2)

    labels = get_interval_labels(bounds)

    plt.xticks(centers, labels, rotation=45, ha="right")
    plt.xlabel(r"$[x_{i-1}; x_i)$")
    plt.ylabel(r"$n_i$")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)


def show_all_histograms():
    plt.show()