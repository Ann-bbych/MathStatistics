from input_handler import read_input_file
from statistics import get_n, get_mean, get_variance, get_sigma, get_lambda


def main():
    try:
        bounds1, frequencies1 = read_input_file("input1.txt")
        bounds2, frequencies2 = read_input_file("input2.txt")

        print("=== Завдання 1 ===")
        print("Межі:", bounds1)
        print("Частоти:", frequencies1)

        n1 = get_n(frequencies1)
        mean1 = get_mean(bounds1, frequencies1)
        variance1 = get_variance(bounds1, frequencies1, mean1)
        sigma1 = get_sigma(variance1)

        print(f"n = {n1}")
        print(f"x̄ = {mean1}")
        print(f"S² = {variance1}")
        print(f"σ = {sigma1}")

        print("\n=== Завдання 2 ===")
        print("Межі:", bounds2)
        print("Частоти:", frequencies2)

        n2 = get_n(frequencies2)
        mean2 = get_mean(bounds2, frequencies2)
        variance2 = get_variance(bounds2, frequencies2, mean2)
        sigma2 = get_sigma(variance2)
        lambda_value = get_lambda(mean2)

        print(f"n = {n2}")
        print(f"x̄ = {mean2}")
        print(f"S² = {variance2}")
        print(f"σ = {sigma2}")
        print(f"λ = {lambda_value}")

    except Exception as error:
        print("Помилка:", error)


if __name__ == "__main__":
    main()