from scipy.stats import chi2


def get_chi_square_empirical(frequencies, expected):
    if len(frequencies) != len(expected):
        raise ValueError("Списки frequencies і expected повинні мати однакову довжину.")

    chi_square_empirical = 0.0

    for i in range(len(frequencies)):
        if expected[i] <= 0:
            raise ValueError("Очікувана частота npᵢ повинна бути більшою за 0.")

        difference = frequencies[i] - expected[i]
        chi_square_empirical += (difference * difference) / expected[i]

    return chi_square_empirical


def get_degrees_of_freedom(class_count, estimated_params_count):
    degrees_of_freedom = class_count - estimated_params_count - 1

    if degrees_of_freedom <= 0:
        raise ValueError(
            "Кількість ступенів вільності повинна бути більшою за 0. "
            "Перевірте кількість класів і число оцінених параметрів."
        )

    return degrees_of_freedom


def get_chi_square_critical(alpha, degrees_of_freedom):
    if not (0 < alpha < 1):
        raise ValueError("Рівень значущості α повинен належати інтервалу (0; 1).")

    if degrees_of_freedom <= 0:
        raise ValueError("Кількість ступенів вільності повинна бути більшою за 0.")

    chi_square_critical = chi2.ppf(1 - alpha, degrees_of_freedom)
    return chi_square_critical


def check_hypothesis(chi_square_empirical, chi_square_critical):
    if chi_square_empirical < chi_square_critical:
        return "H₀ приймається"
    return "H₀ відхиляється"