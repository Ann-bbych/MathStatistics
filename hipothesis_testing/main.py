import os

from input_handler import read_input_file
from statistics import get_mean, get_variance, get_sigma, get_lambda
from distributions import prepare_distribution_table
from chi_square import (
    get_chi_square_empirical,
    get_degrees_of_freedom,
    get_chi_square_critical,
    check_hypothesis
)
from output_handler import print_task_results
from histograms import plot_histogram, show_all_histograms


def read_alpha():
    alpha_text = input("Введіть рівень значущості α (Enter -> 0.05): ").strip()

    if alpha_text == "":
        return 0.05

    try:
        alpha = float(alpha_text)
    except ValueError:
        raise ValueError("α повинна бути числом.")

    if not (0 < alpha < 1):
        raise ValueError("α повинна належати інтервалу (0; 1).")

    return alpha


def read_normal_parameters():
    a_text = input(
        "Завдання 1. Введіть a (Enter -> оцінити a і σ² за вибіркою): "
    ).strip()

    if a_text == "":
        return None

    try:
        a = float(a_text)
    except ValueError:
        raise ValueError("Параметр a повинен бути числом.")

    sigma_square_text = input("Завдання 1. Введіть σ²: ").strip()

    if sigma_square_text == "":
        raise ValueError(
            "Для нормального розподілу потрібно або ввести і a, і σ², "
            "або залишити обидва поля порожніми."
        )

    try:
        sigma_square = float(sigma_square_text)
    except ValueError:
        raise ValueError("Параметр σ² повинен бути числом.")

    if sigma_square <= 0:
        raise ValueError("Параметр σ² повинен бути більшим за 0.")

    sigma = get_sigma(sigma_square)

    return {
        "mean": a,
        "variance": sigma_square,
        "sigma": sigma,
        "estimated_params_count": 0,
        "user_parameters_text": f"a = {a:.6f}\nσ² = {sigma_square:.6f}",
        "estimated_parameters_text": ""
    }


def read_exponential_parameter():
    lambda_text = input(
        "Завдання 2. Введіть λ (Enter -> оцінити λ за вибіркою): "
    ).strip()

    if lambda_text == "":
        return None

    try:
        lambda_value = float(lambda_text)
    except ValueError:
        raise ValueError("Параметр λ повинен бути числом.")

    if lambda_value <= 0:
        raise ValueError("Параметр λ повинен бути більшим за 0.")

    return {
        "lambda_value": lambda_value,
        "estimated_params_count": 0,
        "user_parameters_text": f"λ = {lambda_value:.6f}",
        "estimated_parameters_text": ""
    }


def main():
    try:
        alpha = read_alpha()

        os.makedirs("output", exist_ok=True)

        bounds1, frequencies1 = read_input_file("input1.txt")
        bounds2, frequencies2 = read_input_file("input2.txt")

        normal_input = read_normal_parameters()
        exponential_input = read_exponential_parameter()

        with open("output/results.txt", "w", encoding="utf-8") as file:
            bounds1_for_distribution = bounds1[:]
            bounds1_for_distribution[0] = float("-inf")
            bounds1_for_distribution[-1] = float("inf")

            if normal_input is None:
                mean1 = get_mean(bounds1, frequencies1)
                variance1 = get_variance(bounds1, frequencies1, mean1)
                sigma1 = get_sigma(variance1)

                estimated_params_count_1 = 2
                user_parameters_text_1 = ""
                estimated_parameters_text_1 = (
                    f"a = x̄ = {mean1:.6f}\n"
                    f"σ² = S² = {variance1:.6f}\n"
                    f"σ = √S² = {sigma1:.6f}"
                )
            else:
                mean1 = normal_input["mean"]
                variance1 = normal_input["variance"]
                sigma1 = normal_input["sigma"]

                estimated_params_count_1 = normal_input["estimated_params_count"]
                user_parameters_text_1 = normal_input["user_parameters_text"]
                estimated_parameters_text_1 = normal_input["estimated_parameters_text"]

            table1 = prepare_distribution_table(
                bounds1_for_distribution,
                frequencies1,
                "normal",
                {"mean": mean1, "sigma": sigma1}
            )

            chi_emp_1 = get_chi_square_empirical(
                table1["frequencies_after"],
                table1["expected_after"]
            )

            class_count_1 = len(table1["frequencies_after"])
            df1 = get_degrees_of_freedom(class_count_1, estimated_params_count_1)
            chi_crit_1 = get_chi_square_critical(alpha, df1)
            conclusion1 = check_hypothesis(chi_emp_1, chi_crit_1)

            hypothesis_text_1 = "вибірка має нормальний закон розподілу"

            print_task_results(
                file=file,
                task_number=1,
                hypothesis_text=hypothesis_text_1,
                alpha=alpha,
                user_parameters_text=user_parameters_text_1,
                estimated_parameters_text=estimated_parameters_text_1,
                bounds_before=table1["bounds_before"],
                frequencies_before=table1["frequencies_before"],
                probabilities_before=table1["probabilities_before"],
                expected_before=table1["expected_before"],
                bounds_after=table1["bounds_after"],
                frequencies_after=table1["frequencies_after"],
                probabilities_after=table1["probabilities_after"],
                expected_after=table1["expected_after"],
                was_merged=table1["was_merged"],
                chi_square_empirical=chi_emp_1,
                class_count=class_count_1,
                estimated_params_count=estimated_params_count_1,
                degrees_of_freedom=df1,
                chi_square_critical=chi_crit_1,
                conclusion_text=conclusion1
            )

            if exponential_input is None:
                mean2 = get_mean(bounds2, frequencies2)
                lambda_value = get_lambda(mean2)

                estimated_params_count_2 = 1
                user_parameters_text_2 = ""
                estimated_parameters_text_2 = (
                    f"λ = 1 / x̄ = 1 / {mean2:.6f} = {lambda_value:.6f}"
                )
            else:
                mean2 = None
                lambda_value = exponential_input["lambda_value"]

                estimated_params_count_2 = exponential_input["estimated_params_count"]
                user_parameters_text_2 = exponential_input["user_parameters_text"]
                estimated_parameters_text_2 = exponential_input["estimated_parameters_text"]

            table2 = prepare_distribution_table(
                bounds2,
                frequencies2,
                "exponential",
                {"lambda_value": lambda_value}
            )

            chi_emp_2 = get_chi_square_empirical(
                table2["frequencies_after"],
                table2["expected_after"]
            )

            class_count_2 = len(table2["frequencies_after"])
            df2 = get_degrees_of_freedom(class_count_2, estimated_params_count_2)
            chi_crit_2 = get_chi_square_critical(alpha, df2)
            conclusion2 = check_hypothesis(chi_emp_2, chi_crit_2)

            hypothesis_text_2 = "вибірка має показниковий закон розподілу"

            print_task_results(
                file=file,
                task_number=2,
                hypothesis_text=hypothesis_text_2,
                alpha=alpha,
                user_parameters_text=user_parameters_text_2,
                estimated_parameters_text=estimated_parameters_text_2,
                bounds_before=table2["bounds_before"],
                frequencies_before=table2["frequencies_before"],
                probabilities_before=table2["probabilities_before"],
                expected_before=table2["expected_before"],
                bounds_after=table2["bounds_after"],
                frequencies_after=table2["frequencies_after"],
                probabilities_after=table2["probabilities_after"],
                expected_after=table2["expected_after"],
                was_merged=table2["was_merged"],
                chi_square_empirical=chi_emp_2,
                class_count=class_count_2,
                estimated_params_count=estimated_params_count_2,
                degrees_of_freedom=df2,
                chi_square_critical=chi_crit_2,
                conclusion_text=conclusion2
            )

        plot_histogram(
            bounds1_for_distribution,
            frequencies1,
            "output/histogram1.png",
            "Гістограма 1",
            1
        )

        plot_histogram(
            bounds2,
            frequencies2,
            "output/histogram2.png",
            "Гістограма 2",
            2
        )

        show_all_histograms()

    except Exception as error:
        print("Помилка:", error)


if __name__ == "__main__":
    main()