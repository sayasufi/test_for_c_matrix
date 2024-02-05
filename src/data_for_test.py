class MatrixVector:
    def __init__(self):
        self.matrices = {}
        self.vectors = {}

    def set_matrix(self, name, matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        self.matrices[name] = {"rows": rows, "cols": cols, "matrix": matrix}

    def set_vector(self, name, vector):
        cols = len(vector)
        self.vectors[name] = {"cols": cols, "vector": vector}

    def get_matrix(self, name):
        if name in self.matrices:
            return self.matrices[name]["matrix"]
        else:
            raise ValueError("Matrix not found")

    def get_vector(self, name):
        if name in self.vectors:
            return self.vectors[name]["vector"]
        else:
            raise ValueError("Vector not found")


def data_gen():
    # Пример использования
    m = MatrixVector()
    m.set_matrix(
        "matrix8",
        [
            [1, 2, 3, 4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21, 22, 23, 24],
            [25, 26, 27, 28, 29, 30, 31, 32],
            [33, 34, 35, 36, 37, 38, 39, 40],
            [41, 42, 43, 44, 45, 46, 47, 48],
            [49, 50, 51, 52, 53, 54, 55, 56],
            [57, 58, 59, 60, 61, 62, 63, 64],
        ],
    )
    m.set_matrix(
        "matrix_zero",
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
    )
    m.set_matrix(
        "matrix_one",
        [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ],
    )
    m.set_vector("vector8", [1, 2, 3, 4, 5, 6, 7, 8])
    m.set_vector("vector_zero", [0, 0, 0, 0, 0, 0, 0, 0])
    m.set_vector("vector_one", [1, 1, 1, 1, 1, 1, 1, 1])
    return m


