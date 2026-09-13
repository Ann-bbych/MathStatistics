def read_input_file(filename):
    bounds = []
    frequencies = []

    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()

        if line == "":
            continue

        parts = line.split()

        if len(parts) != 3:
            raise ValueError(
                f"Помилка у файлі {filename}, рядок {line_number}: "
                f"кожен рядок повинен містити 3 значення "
                f"(ліва межа, права межа, частота)."
            )

        left_text = parts[0]
        right_text = parts[1]
        frequency_text = parts[2]

        try:
            left = float(left_text)
        except ValueError:
            raise ValueError(
                f"Помилка у файлі {filename}, рядок {line_number}: "
                f"ліва межа '{left_text}' не є числом."
            )

        if right_text.lower() == "inf":
            right = float("inf")
        else:
            try:
                right = float(right_text)
            except ValueError:
                raise ValueError(
                    f"Помилка у файлі {filename}, рядок {line_number}: "
                    f"права межа '{right_text}' не є числом або 'inf'."
                )

        try:
            frequency = int(frequency_text)
        except ValueError:
            raise ValueError(
                f"Помилка у файлі {filename}, рядок {line_number}: "
                f"частота '{frequency_text}' не є цілим числом."
            )

        if frequency < 0:
            raise ValueError(
                f"Помилка у файлі {filename}, рядок {line_number}: "
                f"частота не може бути від’ємною."
            )

        if right != float("inf") and left >= right:
            raise ValueError(
                f"Помилка у файлі {filename}, рядок {line_number}: "
                f"ліва межа повинна бути меншою за праву."
            )

        if len(bounds) == 0:
            bounds.append(left)
            bounds.append(right)
        else:
            if bounds[-1] == float("inf"):
                raise ValueError(
                    f"Помилка у файлі {filename}, рядок {line_number}: "
                    f"після інтервалу з правою межею inf не може бути інших інтервалів."
                )

            if left != bounds[-1]:
                raise ValueError(
                    f"Помилка у файлі {filename}, рядок {line_number}: "
                    f"інтервали повинні йти без розривів. "
                    f"Очікувана ліва межа: {bounds[-1]}, отримано: {left}."
                )

            bounds.append(right)

        frequencies.append(frequency)

    if len(frequencies) == 0:
        raise ValueError(f"Файл {filename} порожній або не містить коректних даних.")

    return bounds, frequencies