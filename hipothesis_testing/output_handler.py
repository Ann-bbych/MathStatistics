import math


def write_line(text, file):
    print(text)
    file.write(text + "\n")


def format_number(value, digits=6):
    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        if math.isinf(value):
            if value > 0:
                return "+∞"
            return "-∞"

        rounded = round(value, digits)

        if abs(rounded - int(rounded)) < 10 ** (-digits):
            return str(int(rounded))

        return f"{rounded:.{digits}f}"

    return str(value)


def format_alpha(alpha):
    return f"{alpha:.2f}"


def format_interval(left, right):
    if math.isinf(left) and left < 0:
        left_text = "-∞"
        left_bracket = "("
    else:
        left_text = format_number(left)
        left_bracket = "["

    if math.isinf(right) and right > 0:
        right_text = "+∞"
        right_bracket = ")"
    else:
        right_text = format_number(right)
        right_bracket = ")"

    return f"{left_bracket}{left_text}; {right_text}{right_bracket}"


def print_distribution_table(file, bounds, frequencies, probabilities, expected):
    write_line(
        f"{'Інтервал':<20} {'nᵢ':>10} {'pᵢ':>15} {'npᵢ':>15}",
        file
    )
    write_line("-" * 62, file)

    for i in range(len(frequencies)):
        interval_text = format_interval(bounds[i], bounds[i + 1])
        n_text = format_number(frequencies[i])
        p_text = format_number(probabilities[i])
        np_text = format_number(expected[i])

        write_line(
            f"{interval_text:<20} {n_text:>10} {p_text:>15} {np_text:>15}",
            file
        )

    write_line("", file)


def print_parameters_info(file, user_parameters_text, estimated_parameters_text):
    if user_parameters_text != "":
        write_line(user_parameters_text, file)

    if estimated_parameters_text != "":
        write_line(estimated_parameters_text, file)

    if user_parameters_text != "" or estimated_parameters_text != "":
        write_line("", file)


def print_merge_info(file, was_merged):
    if was_merged:
        write_line(
            "Умови nᵢ ≥ 5 і npᵢ ≥ 5 не виконуються => потрібно об'єднати класи.",
            file
        )
    else:
        write_line(
            "Умови nᵢ ≥ 5 і npᵢ ≥ 5 виконуються => об'єднання класів не потрібне.",
            file
        )

    write_line("", file)


def print_task_results(
    file,
    task_number,
    hypothesis_text,
    alpha,
    user_parameters_text,
    estimated_parameters_text,
    bounds_before,
    frequencies_before,
    probabilities_before,
    expected_before,
    bounds_after,
    frequencies_after,
    probabilities_after,
    expected_after,
    was_merged,
    chi_square_empirical,
    class_count,
    estimated_params_count,
    degrees_of_freedom,
    chi_square_critical,
    conclusion_text
):
    write_line("=" * 80, file)
    write_line(f"Завдання {task_number}", file)
    write_line("=" * 80, file)
    write_line("", file)

    write_line(f"Гіпотеза H₀: {hypothesis_text}", file)
    write_line(f"Рівень значущості α = {format_alpha(alpha)}", file)
    write_line("", file)

    print_parameters_info(file, user_parameters_text, estimated_parameters_text)

    write_line("Таблиця розподілу до перевірки умов", file)
    print_distribution_table(
        file,
        bounds_before,
        frequencies_before,
        probabilities_before,
        expected_before
    )

    print_merge_info(file, was_merged)

    if was_merged:
        write_line("Таблиця розподілу після об'єднання класів", file)
        print_distribution_table(
            file,
            bounds_after,
            frequencies_after,
            probabilities_after,
            expected_after
        )

    write_line(f"χ²емп = {format_number(chi_square_empirical)}", file)
    write_line(
        f"d.f. = m - s - 1 = {class_count} - {estimated_params_count} - 1 = {degrees_of_freedom}",
        file
    )
    write_line(
        f"χ²кр({format_alpha(alpha)}; {degrees_of_freedom}) = {format_number(chi_square_critical)}",
        file
    )

    if chi_square_empirical < chi_square_critical:
        comparison = "<"
    else:
        comparison = ">"

    write_line(f"Порівняння: χ²емп {comparison} χ²кр", file)
    write_line(f"Висновок: {conclusion_text}", file)
    write_line("", file)