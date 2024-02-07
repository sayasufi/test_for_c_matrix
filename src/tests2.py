import logging
import math
import os
import subprocess
import unittest
from ctypes import *

from data_for_test import data_gen
from logs.logging_setup import setup_logging


class MatrixTestCase(unittest.TestCase):
    """Класс тестов"""

    @classmethod
    def setUpClass(cls):
        """Класс настройки перед запуском тестов"""

        def compile_to_shared_object(source_file, output_file):
            """Функция компиляции C файла в расширение .so"""
            try:
                # Компилируем файл source_file в shared object
                subprocess.check_call(
                    ["gcc", "-shared", "-o", output_file, source_file]
                )
                logging.info(f"Файл {source_file} успешно скомпилирован в {output_file}")
            except subprocess.CalledProcessError as e:
                logging.warning(f"Ошибка при компиляции файла {source_file}: {e}")

        # Настраиваем логгер в консоль и в файл
        setup_logging(log_file="logs/cache.log", stdout_logging=True)

        # Указываем путь к исходному файлу и выходному файлу
        source_file = "c_code/matrix.c"
        output_file = "c_code/matrix.so"
        header_file = "c_code/matrix.h"

        # Вызываем функцию для компиляции
        compile_to_shared_object(source_file, output_file)

        # Загрузка библиотеки C
        cls.matrix_lib = CDLL(output_file)
        logging.info(f"Файл {output_file} успешно загружен")

        # Определение типов данных
        cls.TWideVector = c_double * 8
        cls.TWideMatrix = c_double * 8 * 8

        cls.data = data_gen()

    @classmethod
    def tearDownClass(cls):
        """Функция удаления временного файла .so"""

        # os.remove("c_code/matrix.so")
        logging.info("Временные файлы удалены")

    def test_CopyWideMatr(self):
        """Копирование матрицы"""
        CopyWideMatr = self.matrix_lib.CopyWideMatr
        CopyWideMatr.argtypes = [
            c_short,
            c_short,
            self.TWideMatrix,
            self.TWideMatrix,
        ]
        for name in self.data.matrices:
            matrix_python = self.data.get_matrix(name)
            # Создание исходной и целевой матрицы
            C_from = self.TWideMatrix()
            C_to = self.TWideMatrix()

            n = self.data.matrices[name]["rows"]
            m = self.data.matrices[name]["cols"]

            for i in range(n):
                for j in range(m):
                    C_from[i][j] = matrix_python[i][j]

            # Копирование матрицы
            CopyWideMatr(n, m, C_from, C_to)

            # Проверка, что матрицы равны
            for i in range(n):
                for j in range(m):
                    self.assertEqual(C_to[i][j], C_from[i][j])
                    self.assertEqual(C_to[i][j], matrix_python[i][j])

    def test_AbsWideVect(self):
        """Модуль вектора"""
        # Обертки для функций C
        AbsWideVect = self.matrix_lib.AbsWideVect
        AbsWideVect.argtypes = [c_short, self.TWideVector]
        AbsWideVect.restype = c_double
        for name in self.data.vectors:
            vector_python = self.data.get_vector(name)
            # n - размер вектора
            n = self.data.vectors[name]["cols"]
            # Создание вектора
            a = self.TWideVector()
            expected_result = 0
            # Заполнение вектора
            for i in range(n):
                a[i] = vector_python[i]
                expected_result += vector_python[i] * vector_python[i]
            expected_result = math.sqrt(expected_result)
            # Вычисление модуля вектора
            result = AbsWideVect(n, a)

            # Проверка, что результат соответствует ожидаемому значению
            self.assertAlmostEqual(result, expected_result, delta=0.0001)

    # def test_AddWideVect(self):
    #     """Сложение двух векторов"""
    #     AddWideVect = self.matrix_lib.AddWideVect
    #     AddWideVect.argtypes = [
    #         c_short,
    #         self.TWideVector,
    #         self.TWideVector,
    #         self.TWideVector,
    #     ]
    #
    #
    #     a1 = self.TWideVector(*slot1)
    #     a2 = self.TWideVector(*slot2)
    #     a = self.TWideVector()
    #
    #     expected_result = [0] * 8
    #     for i in range(8):
    #         expected_result[i] = a1[i] + a2[i]
    #
    #     AddWideVect(8, a1, a2, a)
    #
    #     for i in range(8):
    #         self.assertEqual(a[i], expected_result[i])


if __name__ == "__main__":
    unittest.main()
