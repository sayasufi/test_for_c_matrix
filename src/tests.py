import logging
import math
import subprocess
import unittest

import cffi

from data_for_test import MatrixVector
from logs.logging_setup import setup_logging
from parser_header import parser_header


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

    @classmethod
    def tearDownClass(cls):
        """Функция удаления временного файла .so"""

        # os.remove("c_code/matrix.so")
        logging.info("Временные файлы удалены")

    # def test_CopyWideMatr(self):
    #     """Копирование матрицы"""
    #     CopyWideMatr = self.matrix_lib.CopyWideMatr
    #     CopyWideMatr.argtypes = [
    #         c_short,
    #         c_short,
    #         self.TWideMatrix,
    #         self.TWideMatrix,
    #     ]
    #     for name in self.data.matrices:
    #         matrix_python = self.data.get_matrix(name)
    #         # Создание исходной и целевой матрицы
    #         C_from = self.TWideMatrix()
    #         C_to = self.TWideMatrix()
    #
    #         n = self.data.matrices[name]["rows"]
    #         m = self.data.matrices[name]["cols"]
    #
    #         for i in range(n):
    #             for j in range(m):
    #                 C_from[i][j] = matrix_python[i][j]
    #
    #         # Копирование матрицы
    #         CopyWideMatr(n, m, C_from, C_to)
    #
    #         # Проверка, что матрицы равны
    #         for i in range(n):
    #             for j in range(m):
    #                 self.assertEqual(C_to[i][j], C_from[i][j])
    #                 self.assertEqual(C_to[i][j], matrix_python[i][j])

    def test_AbsWideVect(self):
        """Модуль вектора"""

        lst = list(range(8))
        len_lst = len(lst)
        arr_var = self.ffi.new('double[]', lst)
        print(arr_var, type(arr_var))
        res = self.lib.AbsWideVect(len_lst, arr_var)
        print(f"Sum of {lst} is {res}")
        expected_result = math.sqrt(sum(map(lambda x: x ** 2, lst)))

        # Проверка, что результат соответствует ожидаемому значению
        self.assertAlmostEqual(res, expected_result, delta=0.0001)

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
