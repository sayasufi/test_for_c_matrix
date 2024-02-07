def multiply_matrices(a, b):
    temp = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i1 in range(len(a)):
        for j1 in range(len(b[0])):
            for k1 in range(len(b)):
                temp[i1][j1] += a[i1][k1] * b[k1][j1]

    return temp


def transpose(matrix):
    temp = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for i1 in range(len(temp)):
        for j1 in range(len(temp[0])):
            temp[i1][j1] = matrix[j1][i1]
    return temp


def multiply_matrices_digit(matrix, digit):
    # Создаем пустую матрицу для результата
    expected_result = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    # Выполняем умножение матрицы на число
    for i1 in range(len(matrix)):
        for j1 in range(len(matrix[0])):
            expected_result[i1][j1] = matrix[i1][j1] * digit
    return expected_result

def multiply_matrices_vector(matrix, vector):
    # Создаем пустой вектор для результата
    expected_result = [0 for _ in range(len(matrix))]

    # Выполняем умножение матрицы на вектор
    for i1 in range(len(matrix)):
        for j1 in range(len(vector)):
            expected_result[i1] += matrix[i1][j1] * vector[j1]

    return expected_result

def inverse_matrix(matrix):
    # Размерность матрицы
    n = len(matrix)

    # Создаем единичную матрицу
    I = [[float(i == j) for j in range(n)] for i in range(n)]

    # Создаем копию матрицы A
    A_copy = [row[:] for row in matrix]

    # Приводим матрицу A к ступенчатому виду методом Гаусса
    for i in range(n):
        # Если элемент на главной диагонали равен 0, меняем строки местами
        if A_copy[i][i] == 0:
            for j in range(i + 1, n):
                if A_copy[j][i] != 0:
                    A_copy[i], A_copy[j] = A_copy[j], A_copy[i]
                    I[i], I[j] = I[j], I[i]
                    break

        # Делим строку i на A_copy[i][i], чтобы получить 1 на главной диагонали
        divisor = A_copy[i][i]
        for j in range(n):
            A_copy[i][j] /= divisor
            I[i][j] /= divisor

        # Обнуляем остальные элементы в столбце i
        for j in range(i + 1, n):
            multiplier = A_copy[j][i]
            for k in range(n):
                A_copy[j][k] -= multiplier * A_copy[i][k]
                I[j][k] -= multiplier * I[i][k]

    # Приводим матрицу A к диагональному виду
    for i in range(n - 1, 0, -1):
        for j in range(i - 1, -1, -1):
            multiplier = A_copy[j][i]
            for k in range(n):
                A_copy[j][k] -= multiplier * A_copy[i][k]
                I[j][k] -= multiplier * I[i][k]

    return I

