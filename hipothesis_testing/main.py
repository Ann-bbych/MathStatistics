from input_handler import read_input_file
from statistics import get_mean, get_variance, get_sigma, get_lambda
from distributions import prepare_distribution_table
import math


def main():
    try:
        bounds1, frequencies1 = read_input_file("input1.txt")
        bounds2, frequencies2 = read_input_file("input2.txt")

        bounds1_for_distribution = bounds1[:]
        bounds1_for_distribution[0] = float("-inf")
        bounds1_for_distribution[-1] = float("inf")

        mean1 = get_mean(bounds1, frequencies1)
        variance1 = get_variance(bounds1, frequencies1, mean1)
        sigma1 = get_sigma(variance1)

        table1 = prepare_distribution_table(
            bounds1_for_distribution,
            frequencies1,
            "normal",
            {"mean": mean1, "sigma": sigma1}
        )

        print("=== Завдання 1 ===")
        print("До об'єднання:")
        print(table1["bounds_before"])
        print(table1["frequencies_before"])
        print(table1["probabilities_before"])
        print(table1["expected_before"])

        print("\nПісля об'єднання:")
        print(table1["bounds_after"])
        print(table1["frequencies_after"])
        print(table1["probabilities_after"])
        print(table1["expected_after"])
        print("Було об'єднання:", table1["was_merged"])

        mean2 = get_mean(bounds2, frequencies2)
        lambda_value = get_lambda(mean2)

        table2 = prepare_distribution_table(
            bounds2,
            frequencies2,
            "exponential",
            {"lambda_value": lambda_value}
        )

        print("\n=== Завдання 2 ===")
        print("До об'єднання:")
        print(table2["bounds_before"])
        print(table2["frequencies_before"])
        print(table2["probabilities_before"])
        print(table2["expected_before"])

        print("\nПісля об'єднання:")
        print(table2["bounds_after"])
        print(table2["frequencies_after"])
        print(table2["probabilities_after"])
        print(table2["expected_after"])
        print("Було об'єднання:", table2["was_merged"])

    except Exception as error:
        print("Помилка:", error)


if __name__ == "__main__":
    main()