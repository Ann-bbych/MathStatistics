from input_handler import read_input_file
from statistics import get_mean, get_variance, get_sigma, get_lambda
from distributions import prepare_distribution_table
from chi_square import (
    get_chi_square_empirical,
    get_degrees_of_freedom,
    get_chi_square_critical,
    check_hypothesis
)


def main():
    try:
        alpha = 0.05

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

        chi_emp_1 = get_chi_square_empirical(
            table1["frequencies_after"],
            table1["expected_after"]
        )
        df1 = get_degrees_of_freedom(len(table1["frequencies_after"]), 2)
        print(df1)
        chi_crit_1 = get_chi_square_critical(alpha, df1)
        conclusion1 = check_hypothesis(chi_emp_1, chi_crit_1)

        print("=== Завдання 1 ===")
        print("χ²емп =", chi_emp_1)
        print("d.f. =", df1)
        print("χ²кр =", chi_crit_1)
        print(conclusion1)

        mean2 = get_mean(bounds2, frequencies2)
        lambda_value = get_lambda(mean2)

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
        df2 = get_degrees_of_freedom(len(table2["frequencies_after"]), 1)
        chi_crit_2 = get_chi_square_critical(alpha, df2)
        conclusion2 = check_hypothesis(chi_emp_2, chi_crit_2)

        print("\n=== Завдання 2 ===")
        print("χ²емп =", chi_emp_2)
        print("d.f. =", df2)
        print("χ²кр =", chi_crit_2)
        print(conclusion2)

    except Exception as error:
        print("Помилка:", error)


if __name__ == "__main__":
    main()