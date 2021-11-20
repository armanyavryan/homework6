class Matrix:
    def __init__(self, *args, **kwargs):
        """
        Takes 2 keyword arguments: filename or list. If filename is given
        read the matrix from file. Else, read it directly from list.
        """
        if 'filename' in kwargs:
            self.read_from_file(kwargs['filename'])
        elif 'list' in kwargs:
            self.read_as_list(kwargs['list'])

    def __str__(self):
        s = '---------MATRIX---------\n'
        s += '\n'.join(str(row) for row in self._matrix)
        s += '\n'
        s += f'colums = {self.shape[0]}\nrows = {self.shape[1]}'
        s += '\n------------------------\n'
        return s

    def __sub__(self, other):
        if (type(other) == type(self)):
            if other._rows != self._rows or other._columns != self._columns:
                raise ArithmeticError("shapes mismatch.")
            arr = []
            for r in range(self._rows):
                arr.append([])
                for c in range(self._columns):
                    arr[r].append(self._matrix[r][c] - other._matrix[r][c])

            m = Matrix()
            m.read_as_list(arr)
            return m
        else:
            raise ArithmeticError(f"wrong operand type {type(other)}")

    def __add__(self, other):
        """
        The `+` operator. Sum two matrices.
        TODO: implement
        """
        if (type(other) == type(self)):
            if other._rows != self._rows or other._columns != self._columns:
                raise ArithmeticError("shapes mismatch.")
            arr = []
            for r in range(self._rows):
                arr.append([])
                for c in range(self._columns):
                    arr[r].append(self._matrix[r][c] + other._matrix[r][c])

            m = Matrix()
            m.read_as_list(arr)
            return m
        else:
            raise ArithmeticError(f"wrong operand type {type(other)}")

    def __mul__(self, other):
        """
        The `*` operator. Element-wise matrix multiplication.
        Columns and rows sizes of two matrices should be the same.

        If other is not a matrix (int, float) multiply all elements of the matrix to other.
        TODO: implement
        """
        if (type(other) == type(self)):
            if other._rows != self._columns:
                raise ValueError("shapes mismatch.")
            arr = []
            for k in range(self._rows):
                arr.append([])
                for j in range(other._columns):
                    c = 0
                    for i in range(other._rows):
                        c = c + self._matrix[k][i] * other._matrix[i][j]
                    arr[k].append(c)

            m = Matrix()
            m.read_as_list(arr)
            return m
        elif type(other) == type(1) or type(other) == type(1.0):
            arr = []
            for i in range(self._rows):
                arr.append([])
                for j in range(self._columns):
                    arr[i].append(other * self._matrix[i][j])

            m = Matrix()
            m.read_as_list(arr)
            return m
        else:
            raise ArithmeticError(f"can't multiply a matrix with an object of type {type(other)}")

    def __matmul__(self, other):
        """
        The `@` operator. Mathematical matrix multiplication.
        The number of columns in the first matrix must be equal to the number of rows in the second matrix.
        TODO: implement
        """
        if (type(other) == type(self)):
            if other._rows != self._rows or other._columns != self._columns:
                raise ArithmeticError("shapes mismatch.")
            arr = []
            for r in range(self._rows):
                arr.append([])
                for c in range(self._columns):
                    arr[r].append( self._matrix[r][c] * other._matrix[r][c])

            m = Matrix()
            m.read_as_list(arr)
            return m
        elif type(other) == type(1) or type(other) == type(1.0):
            arr = []
            for i in range(self._rows):
                arr.append([])
                for j in range(self._columns):
                    arr[i].append(other * self._matrix[i][j])

            m = Matrix()
            m.read_as_list(arr)
            return m
        else:
            raise ArithmeticError(f"can't multiply a matrix with an object of type {type(other)}")

    def read_as_list(self, matrix_list):
        if len(matrix_list) == 0:
            self._matrix = []
            self._columns = 0
            self._rows = 0
            return

        columns_count_0 = len(matrix_list[0])
        if not all(len(row) == columns_count_0 for row in matrix_list):
            raise ValueError('Got incorrect matrix')

        self._matrix = matrix_list
        self._rows = len(self._matrix)
        self._columns = columns_count_0

    def read_from_file(self, filename):
        with open(filename, 'r') as f:
            matrix_list = f.readlines()
        matrix_list = list(map(lambda s: list(map(float, s[:-1].split(' '))), matrix_list))
        self.read_as_list(matrix_list)

    def write_to_file(self, filename):
        """
        Write the matrix to the given filename.
        TODO: implement
        """
        with open(filename, 'w') as f:
            f.writelines(str(self._matrix))

    def transpose(self):
        tr = []
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[i])):
                if i == 0:
                    tr.append([])
                tr[j].append(self._matrix[i][j])

        m = Matrix()
        m.read_as_list(tr)
        return  m

    def adj(self):
        d = []
        for i in range(self._rows):
            d.append([])
            for j in range(self._columns):
                aij = self.minor(i, j).determinant * (-1) ** (i + j)
                d[i].append(aij)
        m = Matrix()
        m.read_as_list(d)
        return m

    def invert(self):
        d = self.determinant
        if (d == 0):
            raise ArithmeticError("Inverse of matrix with determinant = 0 is not defined!")

        k = self.adj()
        p = k.transpose()
        t = p * (1 / d)
        return t

    def minor(self, dr, dc):
        min = []
        if dr > self._rows or dc > self._columns or dr < 0 or dc < 0:
            raise ValueError("Wrong row or column!")
        for r in range(self._rows):
            if r == dr:
                continue
            min.append([])
            for c in range(self._columns):
                if c == dc:
                    continue
                min[-1].append(self._matrix[r][c])

        m = Matrix()
        m.read_as_list(min)
        return m

    @property
    def trace(self):
        if(self._columns != self._rows):
            raise ArithmeticError("Trace not defined for the non square matrices!")
        tr = 0
        for i in range(self._columns):
            tr += self._matrix[i][i]
        return tr

    @property
    def determinant(self):
        if self._columns != self._rows:
            raise ValueError("Not square matrix!")
        if self._columns == 1:
            return self._matrix[0][0]
        det = 0
        for c in range(self._columns):
            minor = self.minor(0, c)
            det = det + (-1)**(c) * self._matrix[0][c] * minor.determinant

        return det

    @property
    def shape(self):
        return self._columns, self._rows






# -----------------------TESTING-----------------------

# m1 = Matrix()
# m1.read_as_list([[1,2,3],
#               [4,5,6]])
#
# m2 = Matrix()
# m2.read_as_list([[10,11],
#               [20,21],
#               [30,31]])
#
# m3 = m1 * m2
# print(str(m3))
#
# m0 = Matrix()
# m0.read_as_list([[4, 3, 2, 2],
#               [0, 1, -3, 3],
#               [0, -1, 3, 3],
#               [0, 3, 1, 1]])
# m0.write_to_file("m0mat.txt")
# print(str(m0 * m0.invert()))
# print(m0.trace)
# print(m0.minor(2, 2))
#
# b = Matrix()
# b.read_as_list([[2,1,1],
#                 [1,0,3],
#                 [5,2,4]])
#
# a = Matrix()
# a.read_as_list([[5,0,1],
#                 [1,2,3],
#                 [3,3,2]])
#
# print("a", a)
# print("a(-1)", a.invert())
# print("a@a(-1)", a@2)
#
# print("a + a", a + a)
# print("a - a", a - a)
#
# x = a.invert()*b
# print(x*(a.determinant))
# print(a*x)
# print(m0.determinant)
#
