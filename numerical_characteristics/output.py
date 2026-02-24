# =========================
# file: output.py
# =========================
from __future__ import annotations
from typing import Optional, TextIO


class DualOutput:
    """
    Вивід одночасно в консоль і (за бажанням) у файл.
    Використання:
        out = DualOutput("result.txt")
        out.line("Hello")
        out.close()
    """

    def __init__(self, file_path: Optional[str] = None, encoding: str = "utf-8") -> None:
        self._file: Optional[TextIO] = None
        if file_path:
            self._file = open(file_path, "w", encoding=encoding)

    def line(self, text: str = "") -> None:
        print(text)
        if self._file is not None:
            self._file.write(text + "\n")

    def close(self) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None


def format_num(x: float, digits: int = 2) -> str:
    """Округлення ТІЛЬКИ для виводу."""
    return f"{x:.{digits}f}"