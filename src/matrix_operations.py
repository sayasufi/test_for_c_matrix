import numpy as np


def abs_vector(vector: list) -> float | int:
    """Модуль вектора"""
    vector_np = np.array(vector)
    return np.linalg.norm(vector_np)


def add_matrices(matrix1: list, matrix2: list) -> list:
    """Сложение матриц или векторов"""
    matrix_np1, matrix_np2 = np.array(matrix1), np.array(matrix2)
    return (matrix_np1 + matrix_np2).tolist()


def sub_matrices(matrix1: list, matrix2: list) -> list:
    """Вычитание матриц или векторов"""
    matrix_np1, matrix_np2 = np.array(matrix1), np.array(matrix2)
    return (matrix_np1 - matrix_np2).tolist()


def multiply_matrices(matrix1: list, matrix2: list) -> list:
    """Перемножение матриц"""
    matrix_np1, matrix_np2 = np.array(matrix1), np.array(matrix2)
    return np.dot(matrix_np1, matrix_np2).tolist()


def transpose_matrices(matrix: list) -> list:
    """Транспонирование матрицы"""
    matrix_np = np.array(matrix)
    return matrix_np.transpose().tolist()


def multiply_matrices_digit(matrix: list, digit: int | float) -> list:
    """Умножение матрицы или вектора на число"""
    matrix_np = np.array(matrix)
    return (matrix_np * digit).tolist()


def multiply_matrices_vector(matrix: list, vector: list) -> list:
    """Умножение матрицы на вектор"""
    matrix_np, vector_np = np.array(matrix), np.array(vector)
    return np.dot(matrix_np, vector_np).tolist()


def inverse_matrices(matrix: list) -> list:
    """Обратная матрица"""
    matrix_np = np.array(matrix)
    return np.linalg.inv(matrix_np).tolist()
