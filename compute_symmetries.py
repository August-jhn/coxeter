import itertools as it
import os
import coxeter_todd
import kaleidescope

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def compute_for_diagram(symbol):
    """
    This function takes a schlafli symbol {p1,...,pn-1} in array format
    creates a directory named {p1,...,pn-1}
    finds all possible combinations of generating sets. 
    for each of these generating sets {a_i}, it computes the corresponding cosets G/<a_i>
    Then it stores them in a file named <a_1,...,a_n>.txt where the information is stored as
    i, word (coset representative)
    """
    dir_name = "["
    for letter in symbol:
        dir_name = dir_name + str(letter) + ','
    dir_name = dir_name[:-1] + "]"

    try:
        os.mkdir("symmetries/" + dir_name)
    except:
        print("Symbol alredy computed")
        return

    mirrors = []

    subsets = []

    for i in range(len(symbol) + 1):
        mirrors.append(ALPHABET[i])

    for i in range(len(mirrors) + 1):
        combos = list(it.combinations(mirrors, i))
        print(combos)
        for combo in combos:
            subsets.append(list(combo))

    print(symbol)
    gens, rels = kaleidescope.shlafli_symbol_to_presentation(symbol)

    print(gens,rels)

    for subset in subsets:
        with open("symmetries/" + dir_name + "/cosets_" + str(subset) + ".txt", 'x') as f:
            graphs, indices = coxeter_todd.compute_graph(gens, rels, subset)
            indices_to_words = coxeter_todd.compute_words(graphs, indices, gens)
            for index in indices:
                f.write(str(index) + "," + indices_to_words[index] + "\n")


    return dir_name,mirrors,subsets

print(compute_for_diagram([4,3,3]))

# gens = ["a","b", "c",'d']
# rels =[['a', 'a'], ['a', 'b', 'a', 'b', 'a', 'b'], ['a', 'b', 'a', 'b'], ['a', 'c', 'a', 'c'], ['a', 'd', 'a', 'd'], ['b', 'b'], ['b', 'c', 'b', 'c', 'b', 'c'], ['b', 'c', 'b', 'c'], ['b', 'd', 'b', 'd'], ['c', 'c'], ['c', 'd', 'c', 'd', 'c', 'd'], ['c', 'd', 'c', 'd'], ['d', 'd']]



# coxeter_todd.compute_graph(gens, rels, [])
