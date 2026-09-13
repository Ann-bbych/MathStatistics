import math


def laplace_function(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def normal_probability(left, right, mean, sigma):
    if sigma <= 0:
        raise ValueError("σ повинна бути більшою за 0.")

    if math.isinf(left) and left < 0:
        left_value = 0.0
    else:
        left_value = laplace_function((left - mean) / sigma)

    if math.isinf(right) and right > 0:
        right_value = 1.0
    else:
        right_value = laplace_function((right - mean) / sigma)

    probability = right_value - left_value

    if probability < 0 and abs(probability) < 1e-12:
        probability = 0.0

    return probability


def exponential_probability(left, right, lambda_value):
    if lambda_value <= 0:
        raise ValueError("λ повинна бути більшою за 0.")

    if left < 0:
        raise ValueError("Для показникового розподілу ліва межа не може бути від’ємною.")

    if math.isinf(right) and right > 0:
        probability = math.exp(-lambda_value * left)
    else:
        probability = math.exp(-lambda_value * left) - math.exp(-lambda_value * right)

    if probability < 0 and abs(probability) < 1e-12:
        probability = 0.0

    return probability


def fix_last_probability(probabilities):
    if len(probabilities) == 0:
        return probabilities

    fixed = probabilities[:]

    total = 0.0
    for i in range(len(fixed) - 1):
        if fixed[i] < 0 and abs(fixed[i]) < 1e-12:
            fixed[i] = 0.0
        total += fixed[i]

    fixed[-1] = 1.0 - total

    if fixed[-1] < 0 and abs(fixed[-1]) < 1e-12:
        fixed[-1] = 0.0

    return fixed


def get_probabilities(bounds, distribution_type, params):
    probabilities = []

    for i in range(len(bounds) - 1):
        left = bounds[i]
        right = bounds[i + 1]

        if distribution_type == "normal":
            mean = params["mean"]
            sigma = params["sigma"]
            probability = normal_probability(left, right, mean, sigma)

        elif distribution_type == "exponential":
            lambda_value = params["lambda_value"]
            probability = exponential_probability(left, right, lambda_value)

        else:
            raise ValueError("Невідомий тип розподілу.")

        probabilities.append(probability)

    return fix_last_probability(probabilities)


def get_expected(probabilities, frequencies):
    n = 0
    for frequency in frequencies:
        n += frequency

    expected = []
    for probability in probabilities:
        expected.append(n * probability)

    return expected


def conditions_are_met(frequencies, expected):
    for i in range(len(frequencies)):
        if frequencies[i] < 5 or expected[i] < 5:
            return False
    return True


def get_problem_index(frequencies, expected):
    for i in range(len(frequencies)):
        if frequencies[i] < 5 or expected[i] < 5:
            return i
    return -1


def choose_neighbor_index(frequencies, expected, problem_index):
    last_index = len(frequencies) - 1

    if problem_index == 0:
        return 1

    if problem_index == last_index:
        return last_index - 1

    left_value = min(frequencies[problem_index - 1], expected[problem_index - 1])
    right_value = min(frequencies[problem_index + 1], expected[problem_index + 1])

    if left_value <= right_value:
        return problem_index - 1

    return problem_index + 1


def build_classes(bounds, frequencies):
    classes = []

    for i in range(len(frequencies)):
        one_class = {
            "left": bounds[i],
            "right": bounds[i + 1],
            "frequency": frequencies[i]
        }
        classes.append(one_class)

    return classes


def unpack_classes(classes):
    if len(classes) == 0:
        return [], []

    bounds = [classes[0]["left"]]
    frequencies = []

    for one_class in classes:
        frequencies.append(one_class["frequency"])
        bounds.append(one_class["right"])

    return bounds, frequencies


def merge_neighbor_classes(classes, index1, index2):
    left_index = min(index1, index2)
    right_index = max(index1, index2)

    if right_index - left_index != 1:
        raise ValueError("Об’єднувати можна тільки сусідні класи.")

    merged_class = {
        "left": classes[left_index]["left"],
        "right": classes[right_index]["right"],
        "frequency": classes[left_index]["frequency"] + classes[right_index]["frequency"]
    }

    new_classes = []

    for i in range(len(classes)):
        if i == left_index:
            new_classes.append(merged_class)
        elif i == right_index:
            continue
        else:
            new_classes.append(classes[i])

    return new_classes


def merge_classes(bounds, frequencies, distribution_type, params):
    classes = build_classes(bounds, frequencies)

    while True:
        current_bounds, current_frequencies = unpack_classes(classes)
        current_probabilities = get_probabilities(current_bounds, distribution_type, params)
        current_expected = get_expected(current_probabilities, current_frequencies)

        if conditions_are_met(current_frequencies, current_expected):
            return current_bounds, current_frequencies, current_probabilities, current_expected

        problem_index = get_problem_index(current_frequencies, current_expected)

        if problem_index == -1:
            return current_bounds, current_frequencies, current_probabilities, current_expected

        neighbor_index = choose_neighbor_index(current_frequencies, current_expected, problem_index)

        classes = merge_neighbor_classes(classes, problem_index, neighbor_index)


def prepare_distribution_table(bounds, frequencies, distribution_type, params):
    probabilities_before = get_probabilities(bounds, distribution_type, params)
    expected_before = get_expected(probabilities_before, frequencies)

    bounds_before = bounds[:]
    frequencies_before = frequencies[:]

    was_merged = not conditions_are_met(frequencies_before, expected_before)

    if was_merged:
        bounds_after, frequencies_after, probabilities_after, expected_after = merge_classes(
            bounds,
            frequencies,
            distribution_type,
            params
        )
    else:
        bounds_after = bounds[:]
        frequencies_after = frequencies[:]
        probabilities_after = probabilities_before[:]
        expected_after = expected_before[:]

    return {
        "bounds_before": bounds_before,
        "frequencies_before": frequencies_before,
        "probabilities_before": probabilities_before,
        "expected_before": expected_before,
        "bounds_after": bounds_after,
        "frequencies_after": frequencies_after,
        "probabilities_after": probabilities_after,
        "expected_after": expected_after,
        "was_merged": was_merged
    }