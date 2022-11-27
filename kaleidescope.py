import numpy as np
import itertools as it

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def schlafli_symbol_to_matrix(symbol):
    """Turns a schlafli symbol into a coxeter matrix"""
    dims = len(symbol) + 1
    matrix = np.zeros((dims,dims))
    for pair in np.ndindex(matrix.shape):
        i,j = pair
        if i == j:
            matrix[i][j] = 1
        elif j-i == 1:
            matrix[i][j] = symbol[i]
            matrix[j][i] = symbol[i]
        elif i - j == -1:
            matrix[i][j] = symbol[j]
            matrix[j][i] = symbol[j]
        elif abs(i-j) > 1:
            matrix[i][j] = 2
    return matrix

def shlafli_symbol_to_presentation(symbol):
    """this takes a schlafli symbol [p1...pn] and returns the generators and relations of the corresponding coxeter group"""
    generators = [ALPHABET[i] for i in range(len(symbol) + 1)]
    relations = []
    indices = [i for i in range(len(generators))]

    checked = []

    for i in indices:
        for j in indices:
            if {i,j} not in checked:
                checked.append({i,j})
                
                p,q = (min(i,j), max(i,j))

                if q-p == 1:
                    r = []
                    for k in range(symbol[p]):
                        r.append(ALPHABET[p])
                        r.append(ALPHABET[q])
                    relations.append(r)
                elif p == q:
                    relations.append([ALPHABET[p],ALPHABET[p]])
                else:
                    r = []
                    for k in range(2):
                        r.append(ALPHABET[p])
                        r.append(ALPHABET[q])
                    relations.append(r)

    
    return generators, relations


    


def find_representation(mirrors, matrix):
    """
    mirrors: a list of elements. These should be ordered according as the coxeter matrix is set up
    matrix: a coxeter matrix

    This algorithm defines an orthogonal representation 
    for the generators of a coxeter group with respect to the dot product.
    
    This in turn can be used to represent the entire group!"""

    #first, we find the normals

    dims = len(mirrors)

    id = np.identity(dims)


    normals = {}
    norms = []

    for i in range(dims):
        n_i = np.zeros(dims)
        if i == 0:
            n_i[0] = 1
        else:
            n_i[i-1] = np.cos(np.pi - np.pi/matrix[i-1][i])/norms[i-1][i-1]
            
            n_i[i] = np.sqrt(1-n_i[i-1]**2)
        norms.append(n_i)

    #to ensure the code is shitty enough, we completely re-define everything to make it a dictionary

    for i in range(dims):
        normals[mirrors[i]] = norms[i]


    reps = {}
    for i in range(dims):
        mat = np.identity(dims)
        for j in range(dims):
            mat[j] = id[j] - 2* np.dot(id[j], normals[mirrors[i]])*normals[mirrors[i]]
        reps[mirrors[i]] = np.transpose(mat)

    reps["1"] = id

    return reps


def transform_by_elt(elt, reps, dims):
    """
    elt : takes a coxeter element (a string of generators)
    reps: takes a dictionary of generating elements to their reprenting matrix
    dims: this specifies the dimensions we are working in, it is an integer
    """
    letters = list(elt)
    trans = np.identity(dims)
    for e in letters:
        trans = np.matmul(trans, reps[e])
    return trans

def initial_element(reps, dims):
    """
    returns the coordinates of a point which is on all but the last mirror of reflection.
    That is, which is orthogonal to all but the first mirror.
    """
    for rep in reps:
        
        
        
        evals,evecs = np.linalg.eig(reps[rep])
        for i in range(len(evals)):
            if evals[i] == 1:
                print(evecs[i], evals[i])
        

def compute_vertices(coxeter_elts, reps, initial_element, dims):
    """
    takes a list of coxeter elements, representatives, an initial element, and the dimension

    returns a dictionary of points to coset representatives.
    """
    

#here's how I'll generate facet lattices:
#first, we compute the vertices, and have a dictionary of integers to coordinates.
#


if __name__ == "__main__":
    
    M = schlafli_symbol_to_matrix([3,3,4])
    mirrors = ['a','b','c']

    reps = find_representation(mirrors, M)
    
    print(shlafli_symbol_to_presentation([4,3]))
    
    