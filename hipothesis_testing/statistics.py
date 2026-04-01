import math


def get_midpoints(bounds):
    midpoints = []

    for i in range(len(bounds) - 1):
        left = bounds[i]
        right = bounds[i + 1]

        if math.isinf(left) and math.isinf(right):
            raise ValueError("Не можна обчислити середину інтервалу (-∞; +∞).")

        if math.isinf(left):
            raise ValueError(
                "Ліва межа -∞ не дозволяє обчислити середину інтервалу."
            )

        if math.isinf(right):
            if i == 0:
                raise ValueError(
                    "Неможливо обчислити середину першого інтервалу з правою межею +∞."
                )

            previous_left = bounds[i - 1]
            previous_right = bounds[i]

            if math.isinf(previous_left) or math.isinf(previous_right):
                raise ValueError(
                    "Неможливо визначити ширину попереднього інтервалу для відкритого класу."
                )

            interval_width = previous_right - previous_left
            right = left + interval_width

        midpoint = (left + right) / 2
        midpoints.append(midpoint)

    return midpoints


def get_n(frequencies):
    n = 0

    for frequency in frequencies:
        n += frequency

    return n


def get_mean(bounds, frequencies):
    midpoints = get_midpoints(bounds)
    n = get_n(frequencies)

    if n == 0:
        raise ValueError("Неможливо обчислити середнє: n = 0.")

    total = 0.0

    for i in range(len(midpoints)):
        total += midpoints[i] * frequencies[i]

    mean = total / n
    return mean


def get_variance(bounds, frequencies, mean):
    midpoints = get_midpoints(bounds)
    n = get_n(frequencies)

    if n == 0:
        raise ValueError("Неможливо обчислити дисперсію: n = 0.")

    total = 0.0

    for i in range(len(midpoints)):
        total += ((midpoints[i] - mean) ** 2) * frequencies[i]

    variance = total / n
    return variance


def get_sigma(variance):
    if variance < 0:
        raise ValueError("Дисперсія не може бути від’ємною.")

    sigma = math.sqrt(variance)
    return sigma


def get_lambda(mean):
    if mean <= 0:
        raise ValueError("Для показникового розподілу середнє повинно бути додатним.")

    lambda_value = 1 / mean
    return lambda_value