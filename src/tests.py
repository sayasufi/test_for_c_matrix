import math
import unittest
from ctypes import *
import subprocess
from data_for_test import data_gen


class MatrixTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def compile_to_shared_object(source_file, output_file):
            try:
                # Компилируем файл source_file в shared object
                subprocess.check_call(
                    ["gcc", "-shared", "-o", output_file, source_file]
                )
                print(
                    f"Файл {source_file} успешно скомпилирован в {output_file}"
                )
            except subprocess.CalledProcessError as e:
                print(f"Ошибка при компиляции файла {source_file}: {e}")

        # Указываем путь к исходному файлу и выходному файлу
        source_file = "./matrix.c"
        output_file = "./matrix.so"

        # Вызываем функцию для компиляции
        compile_to_shared_object(source_file, output_file)

        # Загрузка библиотеки C
        cls.matrix_lib = CDLL("./matrix.so")

        # Определение типов данных
        cls.TWideVector = c_double * 8
        cls.TWideMatrix = c_double * 8 * 8

        cls.data = data_gen()

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
