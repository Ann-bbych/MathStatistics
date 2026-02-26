from __future__ import annotations
from typing import List
import random

def generate_sample(n: int, a: int, b: int) -> List[int]:
    """
    Генерує вибірку з цілих чисел у діапазоні [a; b].
    """
    if n < 100:
        raise ValueError("n має бути не менше 100.")
    if a > b:
        raise ValueError("Ліва межа a не може бути більшою за b.")

    sample: List[int] = []
    for _ in range(n):
        sample.append(random.randint(a, b))
    return sample