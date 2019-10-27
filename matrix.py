import math
from math import sqrt
import numbers

def zeroes(height, width):
    """
    Creates a matrix of zeroes.
    """
    g = [[0.0 for _ in range(width)] for __ in range(height)]
    return Matrix(g)


def identity(n):
    """
    Creates a n x n identity matrix.
    """
    I = zeroes(n, n)
    for i in range(n):
        I.g[i][i] = 1.0
    return I


class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])
        
    
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if self.h == 2:
            det_of_matrix = self[0][0] * self[1][1] - self[0][1] * self[1][0]
            
        return det_of_matrix
            

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
            
        
        tr_of_matrix = 0
        for i in range(len(self.g)):
            for j in range(len(self.g)):
                if i == j:
                    tr_of_matrix = tr_of_matrix + self[i][j]
                else:
                    continue
        
        return tr_of_matrix
        

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

            
        ### TRACE MULTIPLIED BY INENTITY
        
        tr = self.trace()
        iden = identity(self.h)
        trace_identity = []
        
        for row in range(self.h):
            rows = []
            for col in range(self.h):
                rows.append(tr * iden[row][col])
            trace_identity.append(rows)
            
            
        ### TRACE_IDENTITY MINUS MATRIX
        
        trace_identity_minus_matrix = []
        for i in range(self.h):
            rows = []
            for j in range(self.h):
                rows.append(trace_identity[i][j] - self[i][j])
            trace_identity_minus_matrix.append(rows)
            
        
        ### INVERSE CALCULATION
        
        inv_of_matrix = []

        if self.h == 1:
            inv_of_matrix = [[1 / self[0][0]]]
        else:
            if self.determinant() == 0:
                raise ValueError('Matrix is non-invertible')
            else:
                for row in range(self.h):
                    rows = []
                    for col in range(self.h):
                        rows.append((1 / self.determinant()) * trace_identity_minus_matrix[row][col])
                    inv_of_matrix.append(rows)
        
        return Matrix(inv_of_matrix)
    

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        
        matrix_transpose = []
    
        for col in range(self.w):
            rows = []
            for row in range(self.h):
                rows.append(self[row][col])
            matrix_transpose.append(rows)

        return Matrix(matrix_transpose)
        

    def is_square(self):
        return self.h == self.w
    
    
    def dot_product(self, vector_one, vector_two):
        s = 0
        for i in range(len(vector_one)):
            s += vector_one[i] * vector_two[i]

        return s
    
    
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    
    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    
    def __add__(self, other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        
        added_matrices = []
        
        for i in range(self.h):
            rows = []
            for j in range(self.w):
                rows.append(self.g[i][j] + other.g[i][j])
            added_matrices.append(rows)
            
        return Matrix(added_matrices)
            

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        
        negated_matrix = []
        
        for i in range(self.h):
            rows = []
            for j in range(self.w):
                rows.append(-self[i][j])
            negated_matrix.append(rows)
            
        return Matrix(negated_matrix)
        

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be subtracted if the dimensions are the same") 

        
        subtracted_matrices = []
        
        for i in range(self.h):
            rows = []
            for j in range(self.w):
                rows.append(self[i][j] - other[i][j])
            subtracted_matrices.append(rows)
            
        return Matrix(subtracted_matrices)
    

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        
        product = []
        
        transpose_other = other.T()
    
        for rowA in self:
            row_result = []
            for rowB in transpose_other:
                row_result.append(self.dot_product(rowA, rowB))
            product.append(row_result)

        return Matrix(product)
        

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        
        product = []
        
        if isinstance(other, numbers.Number):
            for i in range(len(self.g)):
                rows = []
                for j in range(len(self.g[0])):
                    rows.append(other * self.g[i][j])
                product.append(rows)
                
        return Matrix(product)
    
    
    
