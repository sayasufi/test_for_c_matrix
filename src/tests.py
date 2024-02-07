import logging
import math
import os
import subprocess
import unittest

import cffi

from data_for_test import MatrixVector
from logs.logging_setup import setup_logging
from matrix_operations import *
from parser_header import parser_header

count_valid_test = 0


def compile_to_shared_object(source_file_in, output_file_in):
    """Функция компиляции C файла в расширение .so"""
    try:
        # Компилируем файл source_file в shared object
        subprocess.check_call(
            ["gcc", "-shared", "-o", output_file_in, source_file_in]
        )
        logging.info(f"Файл {source_file_in} успешно скомпилирован в {output_file_in}")
    except subprocess.CalledProcessError as e:
        logging.warning(f"Ошибка при компиляции файла {source_file_in}: {e}")


class MatrixTestCase(unittest.TestCase):
    """Класс тестов"""

    ffi = None

    @classmethod
    def setUpClass(cls):
        """Класс настройки перед запуском тестов"""

        # Настраиваем логгер в консоль и в файл
        setup_logging(log_file="logs/cache.log", stdout_logging=True)

        # Указываем путь к исходному файлу и выходному файлу
        source_file = "c_code/matrix.c"
        output_file = "c_code/matrix.so"
        header_file = "c_code/matrix.h"

        # Вызываем функцию для компиляции
        compile_to_shared_object(source_file, output_file)

        # Загрузка библиотеки C
        cls.ffi = cffi.FFI()
        cls.lib = cls.ffi.dlopen(output_file)
        logging.info(f"Файл {output_file} успешно загружен")
        cls.ffi.cdef(parser_header(header_file))

        cls.m = MatrixVector()

        cls.delta = 1e-10
        cls.count_all_test = 15

    @classmethod
    def tearDownClass(cls):
        """Функция удаления временного файла .so"""

        os.remove("c_code/matrix.so")
        logging.info("Временные файлы удалены")

    def test_CopyWideMatr(self):
        """Копирование матрицы"""

        global count_valid_test
        for i in self.m.BASE_MATRIX_NAMES:
            matrix = self.m.gen(i)
            arr_var = self.ffi.new('TWideMatrix', matrix)
            res = self.ffi.new('TWideMatrix', self.m.gen(f"matrix_{len(matrix)}_{len(matrix[0])}_zero"))
            self.lib.CopyWideMatr(len(matrix), len(matrix[0]), arr_var, res)

            # Проверка, что матрицы равны
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    self.assertAlmostEqual(res[i][j], arr_var[i][j], delta=self.delta)
                    self.assertAlmostEqual(res[i][j], matrix[i][j], delta=self.delta)

        logging.info("Тесты для CopyWideMatr (копирование матрицы) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_AbsWideVect(self):
        """Модуль вектора"""

        global count_valid_test
        for i in self.m.BASE_VECTOR_NAMES:
            vector = self.m.gen(i)
            arr_var = self.ffi.new('TWideVector', vector)
            res = self.lib.AbsWideVect(len(vector), arr_var)
            expected_result = math.sqrt(sum(map(lambda x: x ** 2, vector)))

            # Проверка, что результат соответствует ожидаемому значению
            self.assertAlmostEqual(res, expected_result, delta=self.delta)

        logging.info("Тесты для AbsWideVect (модуль вектора) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_AddWideVect(self):
        """Сложение двух векторов"""

        global count_valid_test
        for i in self.m.BASE_VECTOR_NAMES:
            vector1 = self.m.gen(i)
            arr_var1 = self.ffi.new('TWideVector', vector1)

            for j in self.m.BASE_VECTOR_NAMES:
                vector2 = self.m.gen(j)
                arr_var2 = self.ffi.new('TWideVector', vector2)
                res = self.ffi.new('TWideVector', self.m.gen(f"vector_{len(vector2)}_zero"))
                self.lib.AddWideVect(len(vector2), arr_var1, arr_var2, res)

                expected_result = [x + y for x, y in zip(vector1, vector2)]

                for k in range(len(expected_result)):
                    self.assertAlmostEqual(res[k], expected_result[k], delta=self.delta)

        logging.info("Тесты для AddWideVect (сложение векторов) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_SubWideVect(self):
        """Вычитание двух векторов"""

        global count_valid_test
        for i in self.m.BASE_VECTOR_NAMES:
            vector1 = self.m.gen(i)
            arr_var1 = self.ffi.new('TWideVector', vector1)

            for j in self.m.BASE_VECTOR_NAMES:
                vector2 = self.m.gen(j)
                arr_var2 = self.ffi.new('TWideVector', vector2)
                res = self.ffi.new('TWideVector', self.m.gen(f"vector_{len(vector2)}_zero"))
                self.lib.SubWideVect(len(vector2), arr_var1, arr_var2, res)

                expected_result = [x - y for x, y in zip(vector1, vector2)]

                for k in range(len(expected_result)):
                    self.assertAlmostEqual(res[k], expected_result[k], delta=self.delta)

        logging.info("Тесты для SubWideVect (вычитание векторов) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_MultWideVectScal(self):
        """Умножение вектора на число"""

        global count_valid_test
        for i in self.m.BASE_VECTOR_NAMES:
            vector = self.m.gen(i)
            arr_var = self.ffi.new('TWideVector', vector)
            res = self.ffi.new('TWideVector', self.m.gen(f"vector_{len(vector)}_zero"))

            for j in [0, 1, -1, 13, 1.25]:
                self.lib.MultWideVectScal(len(vector), arr_var, j, res)
                expected_result = list(map(lambda x: x * j, vector))

                for k in range(len(expected_result)):
                    # Проверка, что результат соответствует ожидаемому значению
                    self.assertAlmostEqual(res[k], expected_result[k], delta=self.delta)

        logging.info("Тесты для MultWideVectScal (умножение вектора на число) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_AddWideMatr(self):
        """Сложение двух матриц"""

        global count_valid_test
        for i in self.m.BASE_MATRIX_NAMES:
            matrix1 = self.m.gen(i)
            arr_var1 = self.ffi.new('TWideMatrix', matrix1)

            for j in self.m.BASE_MATRIX_NAMES:
                matrix2 = self.m.gen(j)
                arr_var2 = self.ffi.new('TWideMatrix', matrix2)
                res = self.ffi.new('TWideMatrix', self.m.gen(f"matrix_{len(matrix2)}_{len(matrix2[0])}_zero"))

                self.lib.AddWideMatr(len(matrix2), len(matrix2[0]), arr_var1, arr_var2, res)

                expected_result = [[0] * len(matrix2[0]) for _ in range(len(matrix2))]
                for k1 in range(len(matrix1)):
                    for k2 in range(len(matrix1[k1])):
                        expected_result[k1][k2] = matrix1[k1][k2] + matrix2[k1][k2]

                for k1 in range(len(matrix1)):
                    for k2 in range(len(matrix1[k1])):
                        self.assertAlmostEqual(res[k1][k2], expected_result[k1][k2], delta=self.delta)

        logging.info("Тесты для AddWideMatr (сложение матриц) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_SubWideMatr(self):
        """Вычитание двух матриц"""

        global count_valid_test
        for i in self.m.BASE_MATRIX_NAMES:
            matrix1 = self.m.gen(i)
            arr_var1 = self.ffi.new('TWideMatrix', matrix1)

            for j in self.m.BASE_MATRIX_NAMES:
                matrix2 = self.m.gen(j)
                arr_var2 = self.ffi.new('TWideMatrix', matrix2)
                res = self.ffi.new('TWideMatrix', self.m.gen(f"matrix_{len(matrix2)}_{len(matrix2[0])}_zero"))

                self.lib.SubWideMatr(len(matrix2), len(matrix2[0]), arr_var1, arr_var2, res)

                expected_result = [[0] * len(matrix2[0]) for _ in range(len(matrix2))]
                for k1 in range(len(matrix1)):
                    for k2 in range(len(matrix1[k1])):
                        expected_result[k1][k2] = matrix1[k1][k2] - matrix2[k1][k2]

                for k1 in range(len(matrix1)):
                    for k2 in range(len(matrix1[k1])):
                        self.assertAlmostEqual(res[k1][k2], expected_result[k1][k2], delta=self.delta)

        logging.info("Тесты для SubWideMatr (вычитание матриц) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_MultWideMatrMatr(self):
        """Перемножение двух матриц"""

        global count_valid_test
        for i in self.m.BASE_MATRIX_NAMES:
            matrix1 = self.m.gen(i)
            arr_var1 = self.ffi.new('TWideMatrix', matrix1)

            for j in self.m.BASE_MATRIX_NAMES:
                matrix2 = self.m.gen(j)
                arr_var2 = self.ffi.new('TWideMatrix', matrix2)
                res = self.ffi.new('TWideMatrix', self.m.gen(f"matrix_{len(matrix2)}_{len(matrix2[0])}_zero"))

                self.lib.MultWideMatrMatr(len(matrix1), len(matrix2[0]), len(matrix2), arr_var1, arr_var2, res)

                # Создаем пустую матрицу для результата
                expected_result = multiply_matrices(matrix1, matrix2)

                for k1 in range(len(matrix1)):
                    for k2 in range(len(matrix1[0])):
                        self.assertAlmostEqual(res[k1][k2], expected_result[k1][k2], delta=self.delta)

        logging.info("Тесты для MultWideMatrMatr (перемножение матриц) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_MultWideMatrVect(self):
        """Умножение матрицы на вектор"""

        global count_valid_test
        for i in self.m.BASE_MATRIX_NAMES:
            matrix = self.m.gen(i)
            arr_matr = self.ffi.new('TWideMatrix', matrix)

            for j in self.m.BASE_VECTOR_NAMES:
                vector = self.m.gen(j)
                arr_vec = self.ffi.new('TWideVector', vector)
                res = self.ffi.new('TWideVector', self.m.gen(f"vector_{len(vector)}_zero"))

                self.lib.MultWideMatrVect(len(matrix), len(matrix[0]), arr_matr, arr_vec, res)

                # Создаем пустой вектор для результата
                expected_result = multiply_matrices_vector(matrix, vector)

                for k1 in range(len(vector)):
                    self.assertAlmostEqual(res[k1], expected_result[k1], delta=self.delta)

        logging.info("Тесты для MultWideMatrVect (умножение матрицы на вектор) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_MultWideMatrScal(self):
        """Умножение матрицы на число"""

        global count_valid_test
        for i in self.m.BASE_MATRIX_NAMES:
            matrix = self.m.gen(i)
            arr_matr = self.ffi.new('TWideMatrix', matrix)
            res = self.ffi.new('TWideMatrix', self.m.gen(f"matrix_{len(matrix)}_{len(matrix[0])}_zero"))

            for j in [0, 1, -1, 13, 1.25]:
                self.lib.MultWideMatrScal(len(matrix), len(matrix[0]), arr_matr, j, res)

                # Создаем пустую матрицу для результата
                expected_result = multiply_matrices_digit(matrix, j)

                for k1 in range(len(matrix)):
                    for k2 in range(len(matrix[0])):
                        self.assertAlmostEqual(res[k1][k2], expected_result[k1][k2], delta=self.delta)

        logging.info("Тесты для MultWideMatrScal (умножение матрицы на число) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_IdentityWide(self):
        """Создание единичной матрицы"""
        global count_valid_test
        for i in self.m.BASE_MATRIX_NAMES:
            matrix = self.m.gen(i)
            arr_matr = self.ffi.new('TWideMatrix', matrix)
            self.lib.IdentityWide(len(matrix), arr_matr)

            expected_result = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

            for i1 in range(len(expected_result)):
                for j1 in range(len(expected_result[0])):
                    if i1 == j1:
                        expected_result[i1][j1] = 1

            for k1 in range(len(matrix)):
                for k2 in range(len(matrix[0])):
                    self.assertAlmostEqual(arr_matr[k1][k2], expected_result[k1][k2], delta=self.delta)

        logging.info("Тесты для IdentityWide (создание единичной матрицы) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_TransposeWide(self):
        """Транспонирование матрицы"""

        global count_valid_test
        for i in self.m.BASE_MATRIX_NAMES:
            matrix = self.m.gen(i)
            arr_matr = self.ffi.new('TWideMatrix', matrix)
            res = self.ffi.new('TWideMatrix', self.m.gen(f"matrix_{len(matrix)}_{len(matrix[0])}_zero"))

            self.lib.TransposeWide(len(matrix), len(matrix[0]), arr_matr, res)

            expected_result = transpose(matrix)

            for k1 in range(len(matrix)):
                for k2 in range(len(matrix[0])):
                    self.assertAlmostEqual(res[k1][k2], expected_result[k1][k2], delta=self.delta)

        logging.info("Тесты для TransposeWide (транспонирование матрицы) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_SimilarityWide(self):
        """Тест для Similarity Wide"""

        global count_valid_test
        for i in self.m.BASE_MATRIX_NAMES:
            matrix1 = self.m.gen(i)
            arr_matr1 = self.ffi.new('TWideMatrix', matrix1)

            for j in self.m.BASE_MATRIX_NAMES:
                matrix2 = self.m.gen(j)
                arr_matr2 = self.ffi.new('TWideMatrix', matrix2)
                res = self.ffi.new('TWideMatrix', self.m.gen(f"matrix_{len(matrix1)}_{len(matrix1[0])}_zero"))

                self.lib.SimilarityWide(len(matrix1), len(matrix1[0]), arr_matr1, arr_matr2, res)

                # Перемножение матриц
                temp1 = multiply_matrices(matrix1, matrix2)
                # Транспонирование матрицы
                temp2 = transpose(matrix1)
                # Перемножение матриц
                expected_result = multiply_matrices(temp1, temp2)

                for k1 in range(len(expected_result)):
                    for k2 in range(len(expected_result[0])):
                        self.assertAlmostEqual(res[k1][k2], expected_result[k1][k2], delta=self.delta)

        logging.info("Тесты для SimilarityWide успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")

    def test_InverseWide(self):
        """Тест для обратной матрицы"""

        global count_valid_test
        for _ in range(5):
            matrix = self.m.gen("matrix_8_8_rand")
            arr_matr = self.ffi.new('TWideMatrix', matrix)
            res = self.ffi.new('TWideMatrix', self.m.gen(f"matrix_{len(matrix)}_{len(matrix[0])}_zero"))

            self.lib.InverseWide(len(matrix), arr_matr, res)

            expected_result = inverse_matrix(matrix)

            for k1 in range(len(matrix)):
                for k2 in range(len(matrix[0])):
                    self.assertAlmostEqual(res[k1][k2], expected_result[k1][k2], delta=self.delta)

        logging.info("Тесты для InverseWide (обратная матрица) успешно пройдены")
        count_valid_test += 1
        logging.info(f"Тестов успешно пройдено: {count_valid_test} / {self.count_all_test}")



if __name__ == "__main__":
    unittest.main()
