import logging
import random
from typing import Optional


class MatrixVector:
    BASE_VECTOR_NAMES = (
        "vector_8_zero",
        "vector_8_one",
        "vector_8_-one",
        "vector_8_range",
        "vector_8_rand",
        "vector_1_zero",
        "vector_4_range",
    )
    BASE_MATRIX_NAMES = (
        "matrix_8_8_zero",
        "matrix_8_8_one",
        "matrix_8_8_-one",
        "matrix_8_8_range",
        "matrix_8_8_rand",
        "matrix_1_1_zero",
        "matrix_1_8_range",
        "matrix_8_1_range",
        "matrix_4_4_range",
    )

    def __init__(self):
        self.name: Optional[str] = None
        self.__valid_names = (
            "rand",
            "range",
            "one",
            "zero",
            "-one"
        )

    def gen(self, name: str) -> list[int | float] | list[list[int | float]]:
        """
        Функция генерации матрицы или вектора по имени
        :param name: matrix_8_8_one
                     vector_4_rand
        """
        self.name = name
        lst = self.name.split("_")
        if lst[0] not in ("vector", "matrix"):
            logging.warning("Неверное имя, оно должно начинаться с (vector, matrix)")
            raise ValueError("Неверное имя")
        elif lst[0] == "vector":
            return self.__get_vector()
        else:
            return self.__get_matrix()

    def __get_matrix(self) -> list[list[int | float]]:
        """Генерация матрицы по имени"""
        if not self.__valid_name_matrix():
            raise ValueError("Неверное имя вектора")
        lst = self.name.split("_")

        if lst[3] == "one":
            return [[1] * int(lst[1]) for _ in range(int(lst[2]))]

        elif lst[3] == "zero":
            return [[0] * int(lst[1]) for _ in range(int(lst[2]))]

        elif lst[3] == "-one":
            return [[-1] * int(lst[1]) for _ in range(int(lst[2]))]

        elif lst[3] == "range":
            val = [[0] * int(lst[1]) for _ in range(int(lst[2]))]
            for i in range(int(lst[2])):
                for j in range(int(lst[1])):
                    val[i][j] = i * int(lst[1]) + j + 1
            return val

        else:
            val = [[0] * int(lst[1]) for _ in range(int(lst[2]))]
            for i in range(int(lst[2])):
                for j in range(int(lst[1])):
                    val[i][j] = random.uniform(-1, 1) * 1000
            return val

    def __get_vector(self) -> list[int | float]:
        """Генерация вектора по имени"""
        if not self.__valid_name_vector():
            raise ValueError("Неверное имя вектора")
        lst = self.name.split("_")

        if lst[2] == "one":
            return [1] * int(lst[1])

        elif lst[2] == "zero":
            return [0] * int(lst[1])

        elif lst[2] == "-one":
            return [-1] * int(lst[1])

        elif lst[2] == "range":
            return list(range(1, int(lst[1]) + 1))

        else:
            val = [0] * int(lst[1])
            for i in range(int(lst[1])):
                val[i] = random.uniform(-1, 1) * 1000
            return val

    def __valid_name_vector(self) -> bool:
        """Проверка валидности имени вектора"""
        lst = self.name.split("_")
        if len(lst) != 3:
            logging.warning("Неверное имя вектора, необходимо указать 2 атрибута через _")
            return False
        if not (lst[1].isdigit() and 1 <= int(lst[1]) <= 8):
            logging.warning("Неверное имя вектора, первый аргумент должен лежать в пределах от 1 до 8")
            return False
        if lst[2] not in self.__valid_names:
            logging.warning(
                f"Неверное имя вектора, второй аргумент должен быть выбран из данного списка {self.__valid_names}")
            return False
        return True

    def __valid_name_matrix(self) -> bool:
        """Проверка валидности имени матрицы"""
        lst = self.name.split("_")
        if len(lst) != 4:
            logging.warning("Неверное имя вектора, необходимо указать 3 атрибута через _")
            return False
        if not (lst[1].isdigit() and 1 <= int(lst[1]) <= 8):
            logging.warning("Неверное имя вектора, первый аргумент должен лежать в пределах от 1 до 8")
            return False
        if not (lst[2].isdigit() and 1 <= int(lst[2]) <= 8):
            logging.warning("Неверное имя вектора, второй аргумент должен лежать в пределах от 1 до 8")
            return False
        if lst[3] not in self.__valid_names:
            logging.warning(
                f"Неверное имя вектора, второй аргумент должен быть выбран из данного списка {self.__valid_names}")
            return False
        return True
