from sympy.matrices import Matrix
import numpy as np

def matrix_to_array(m):
    
    return np.array([list(m.row(i)) for i in range(m.shape[0])])

def array_to_matrix(m):
    return Matrix([list(m[i]) for i in range(m.shape[0])])

def rref(m):
    """takes a numpy array and row reduces it"""
    return matrix_to_array(array_to_matrix(m).rref()[0])

def find_pivot_columns(m):
    """given a numpy array in reduced row echelon form, m, returns the pivot columns in a list of integers"""

    def pivot_column(i,c):
        """i is the index of the column"""
        ones = 0
        index = 0
        for elt in c:
            if elt == 1:
                ones += 1
                if index < i:
                    
                    return False
                    
            elif elt != 0:
                return False
            index += 1
        if ones == 1:
            
            return True
        return False
            
    t = m.transpose() #transposing makes it easier to loop through the columns
    pivot_columns = []

    i = 0
    index = 0
    for c in t:
        if pivot_column(index, c):
            pivot_columns.append(i)
            index += 1
        i += 1

    return pivot_columns

def non_trivial_nulspace_vector(m):
    """if there is a non-trivial vector in the nulspace of the matrix, it will return one of them.
    Otherwise we will get the zero vector"""
    transposed_matrix_in_rref = rref(m).transpose()

    vector = np.zeros(m.shape[1])

    rm = rref(m)

    pivot_columns = find_pivot_columns(rm)

    free_columns = []
    for i in range(vector.shape[0]):
        if i not in pivot_columns:
            free_columns.append(i)
    

    for i in range(vector.shape[0]):
        for j in free_columns:
            if i < rm.shape[0]:
                
                vector[i] += -rm.transpose()[j][i]
        if i not in pivot_columns:
            vector[i] = 1

    return vector

def orthogonal_to_vecs(vecs):
    """takes a set of vectors and returns a normalized vector orthogonal to all of them if possible,
     or else returns the zero vector.
     Each of the vectors should be in list of np arrays [x1,...,xn]. 
     (In reality, these would be the transposes of each vector)
     """
    N = np.array(vecs)
    
    
    n = non_trivial_nulspace_vector(N)
    norm = np.linalg.norm(n)
    if norm != 0:
        return n/norm
    print("No normal orthogonal vector can be found. The list of n vectors must have been linearly independent in n dimensional space")
    return n

def normal_from_reflection_matrices(matrix):
    """takes a reflection matrix, computes the eigenvectors of 1 (implying that these vectors are fixed).
    These eigenvectors span the hyperplane of reflection, which is determined by it's normal vectors.
    returns one such normal vector"""
    
    spanning_vectors = []

    evals,evecs = np.linalg.eig(matrix)
    for i in range(len(evals)):
        if evals[i] == 1:
            spanning_vectors.append(evecs[i])
    
    return orthogonal_to_vecs(spanning_vectors)

if __name__ == "__main__":
    vecs = [
        np.array([1,0,0,0,0]),
        np.array([0,1,1,0,0]),
        np.array([2,0,1,0,0]),
        np.array([1,0,0,0,1]),
        ]

    print(rref(np.array(vecs)))
    n = orthogonal_to_vecs(vecs)
    print(n)
    for vec in vecs:
        print(np.dot(vec, n))
    