import re


def starts_with_space_or_hash(string: str) -> bool:
    """Фильтр для хедэров"""
    if string.startswith("\n") or string.startswith("#"):
        return False
    return True


def parser_header(file_name: str = "c_code/matrix.h") -> str:
    """Функция для парсинга хедера C файла"""

    with open(file_name, "r") as file:
        lines = list(
            map(
                lambda x: re.sub(' +', ' ', x),
                map(
                    str.strip,
                    filter(starts_with_space_or_hash, file.readlines())
                )
            )
        )

        return " ".join(lines)
