import numpy as np


D = 2
#[100]
M = np.array(
    [
        [1,4],
        [4,1]

        ]
        
        )


gens = ["a","b"]
rels = [['a','a'], ['b','b'], ['a','b','a','b','a','b','a','b']]



def find_representation(mirrors, matrix):
    """
    mirrors: a list of elements. These should be ordered according as the coxeter matrix is set up
    matrix: a coxeter matrix

    This algorithm defines an orthogonal representation 
    for the generators coxeter group with respect to the dot product.
    
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
            print(1-n_i[i-1]**2)
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
    letters = list(elt)
    trans = np.identity(dims)
    for e in letters:
        trans = np.matmul(trans, reps[e])
    return trans



def compute_graph(gens, rels, coset):

    

    def scan_index(index):


        coincidences = []

        for rel in rels:

            print("---------------")
            print(" ", index)

            i = index
            j = 1

            for letter in rel:
                
                if i in graphs[letter]:
                    if j == len(rel):
                        if graphs[letter][i] != index:
                            coincidences.append((graphs[letter][i], index))
                            print("coincidence", index, graphs[letter][i])
                        graphs[letter][i] = index
                        print(letter, index)
                        print("relator established!")
                    else:
                        i = graphs[letter][i]
                        print(letter, i)
                else:
                    if j == len(rel):
                        graphs[letter][i] = index
                        print(letter, index)
                        print("relator established!")
                    else:

                        next = len(indices) + 1
                        graphs[letter][i] = next
                        i = next
                        indices.append(i) 
                        print(letter, i)
                
                j += 1

        
        
        print(graphs)
            
        for coincidence in coincidences:
            process_coincidence(coincidence)

        a = search_for_left_coincidence()
        while a != None:
            process_coincidence(a)
            a= search_for_left_coincidence()
        
        if index < len(indices):
            scan_index(index +1)
        else:
            print('done!')

    
    def substitute_index(b,a):
        """this function replaces all instances of b with a in the index set, as well as the graphs"""
        print("replacing",b,a)
        
                

    def process_coincidence(coincidence):
        print(indices, "before")
        i,j = coincidence
        x = min(i,j)
        y = max(i,j)

        #need to find a way to get rid of the coincidence/collapse the graph

        #substitute_index(y,x)
        for gen in gens:


            #first, we replace all instances of {i:y} with {i:x}
            for key in graphs[gen]:
                if graphs[gen][key] == y:
                    graphs[gen][key] = x
        
            #next, we simply remove all instances of {y:i}, because we already have these with {x:i} as these are left coincidences
            if y in graphs[gen]: #it may already have been removed
                graphs[gen].pop(y)

            # Let y be the larger coincident index. After removing y, for all indices larger than y we must make the substitution i |-> i-1
            #this substitution must also replace eery instance in the graphs.

        
        indices.remove(y)

        copy = indices[:]

        for a in copy:
            if a > y:
                
                for gen in gens:
                    for key in graphs[gen]:
                        if graphs[gen][key] == a:
                            graphs[gen][key] = a-1
            
                    if a in graphs[gen]: #it may already have been removed
                        graphs[gen].pop(a)
                print(a)
                indices.remove(a)
        
        indices[0] = 1

        for i in range(len(indices)):
            
            if i >= y:
                print(i)

        
        
        print(indices)
        print(graphs)

    def search_for_left_coincidence():

        #this algorithm could be made more efficient, could be optimized with a co_graph
        for gen in gens:
            for key1 in graphs[gen]:
                for key2 in graphs[gen]:
                    if key1 != key2 and graphs[gen][key1] == graphs[gen][key2]:
                        print("coincidence found: ", (key1, key2))
                        return (key1, key2)

        return None #if we return false, it means we have not found any coincidences



    indices = [1]

    graphs = {}
    co_graphs = {}

    for gen in gens:
        graphs[gen] = {}
        co_graphs[gen] = {}
    
    for gen in coset:
        graphs[gen][1] = 1
        co_graphs[gen][1] = 1

    scan_index(1)


    print(indices)

    return graphs,indices

def compute_words(graphs,indices,generators):
    """this function takes the graphs and creates a dictionary of indices to letters"""
    indices_to_letters = {}
    indices_to_letters[1] = "1"

    def trace_graph(i, word):
        
        que = {}
        for g in generators:
            
            que[graphs[g][i]] = g
        print(que, i)
        for q in que:
            if q not in indices_to_letters:
                indices_to_letters[q] =  que[q] + word 
                trace_graph(q,  que[q] + word)
    trace_graph(indices[0], "")
    return indices_to_letters
            

graphs, indices = compute_graph(gens, rels, ['b'])
words = compute_words(graphs, indices, gens)
coxeter_elts = []
for i in words:
    print(i,words[i])
    coxeter_elts.append( words[i])

reps = find_representation(gens, M)




# print(transform_by_elt(coxeter_elts[8], reps, 2))
X = []
Y = []
pts = []



p1 = np.array([0,1])
p2 = np.matmul(transform_by_elt('b', reps, D), p1)
#let {p1...pn} be the regular polytope
#to obtain the k dimensional face, remove the last k ps. Then orbit the initial point (which is on the mirror of p1),
#by the subgorup generated by the last ps which we removed. By removing, I mean quotienting. So in order to find the faces,
#we are to find the cosets of this group.

edges = []

for elt in coxeter_elts:

    pt1 = np.matmul(transform_by_elt(elt, reps, D), p1)
    pt2 = np.matmul(transform_by_elt(elt, reps, D), p2)

    print( pt1 )
    X.append(pt1[0])
    Y.append(pt1[1])
    pts.append(pt1)
    edges.append([pt1, pt2])

import matplotlib.pyplot as plt
# Creating a numpy array
X = np.array(X)
Y = np.array(Y)
# Plotting point using sactter method


#Plot a piecewice linear curve.  Input vertices in cyclic order
def plotline(p):
    for i in range(len(p)-1):
        plt.plot([p[i][0],p[i+1][0]],[p[i][1],p[i+1][1]], marker='o')
        

for edge in edges:
    print(edge)
    plotline(edge)

print(len(edges))



plt.show()