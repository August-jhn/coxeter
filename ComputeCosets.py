
import pyvis

debug = False

# gens = ["a","b", "c"]

# rels = [   ['b', 'b'], ['b', 'c', 'b', 'c', 'b', 'c'],['a', 'c', 'a', 'c'], ['c', 'c'],['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b','a','b'],['a', 'a']]

gens = ['a','b']
rels = [['a','a','a'], ['b','b'], ['a','b','a','b']]


#rels = [['a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a']]
def compute_graph(gens, rels, coset):

    

    def scan_index(index):
        
        print("computed cosets: ", index)


        coincidences = []

        for rel in rels:
            if debug:
                    
                print("---------------")
                print(" ", index)

            i = index
            j = 1

            for letter in rel:
                
                if i in graphs[letter]:
                    if j == len(rel):
                        if graphs[letter][i] != index:
                            coincidences.append((graphs[letter][i], index))
                            if debug:
                                print("coincidence", index, graphs[letter][i])
                        graphs[letter][i] = index
                        if debug:
                            print(letter, index)
                            print("relator established!")
                    else:
                        i = graphs[letter][i]
                        if debug:
                            print(letter, i)
                else:
                    if j == len(rel):
                        graphs[letter][i] = index
                        if debug:
                                
                            print(letter, index)
                            print("relator established!")
                    else:

                        next = len(indices) + 1
                        graphs[letter][i] = next
                        i = next
                        indices.append(i) 
                        if debug:
                                
                            print(letter, i)
                
                j += 1

        if debug:
        
            print(graphs)
            
        for coincidence in coincidences:
            process_coincidence(coincidence)

        a = search_for_left_coincidence()
        while a != None:
            process_coincidence(a)
            a= search_for_left_coincidence()
        
        done = True
        next = None
        reached = {}
        for gen in gens:
            reached[gen] = set()
        for i in indices:
            for g in gens:
                if i not in graphs[g]:
                    done = False
                    next = i
                    scan_index(next)
                    break
                else:
                    reached[g].add(graphs[g][i])
        for g in gens:
            for i in indices:
                if i not in reached[g]:
                    next = i
                    done = False
                    scan_index(next)
                    break
        
        if done:
            print('done!')
            return
            
            

    
    def substitute_index(b,a):
        """this function replaces all instances of b with a in the index set, as well as the graphs"""
        print("replacing",b,a)
                

    def process_coincidence(coincidence):
        if debug:
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

        #after removing y, we have n-1 elements. However, those elements after y are labeled as i +1
        #after relabeling, we should still have exactly n-1 elements

        copy = indices[:]

        index = 1
        for a in copy:
            if a > y:
                
                for gen in gens:
                    for key in graphs[gen]:
                        if graphs[gen][key] == a:
                            graphs[gen][key] = a-1
                    
            
                    if a in graphs[gen]: 
                        
                        graphs[gen][a-1] = graphs[gen][a]
                        graphs[gen].pop(a)
                
                indices[index - 1] = index
                if debug:
                    print("replaced",index , a-1)

            index += 1
        
        indices[0] = 1
        
        

    def search_for_left_coincidence():

        #this algorithm could be made more efficient, could be optimized with a co_graph
        for gen in gens:
            for key1 in graphs[gen]:
                for key2 in graphs[gen]:
                    if key1 != key2 and graphs[gen][key1] == graphs[gen][key2]:
                        if debug:
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

def compute_words(graphs,indices,generators, shorten = True):
    """this function takes the graphs and creates a dictionary of indices to letters"""
    indices_to_letters = {}
    indices_to_letters[1] = "1"

    def trace_graph(i, word):
        
        que = {}
        for g in generators:
        
            que[graphs[g][i]] = g
        
        for q in que:
            if q not in indices_to_letters:
                indices_to_letters[q] =  que[q] + word 
                trace_graph(q,  que[q] + word)
    trace_graph(indices[0], "")
    return indices_to_letters

def word_to_index(word, graphs, indices, generators):
    """word: should be a string of generators and 1
    graphs: this is the dictionary of graphs
    indices: this is the indices as an array
    generators: these are the generators of the group.
    
    All of these must be consistent in order for this to work
    """

    pass

            
def test_run():
    

    colors = { 'a': "red", 'b' : "green", 'c' : "blue"}
    graphs, indices = compute_graph(gens, rels, [])
    words = compute_words(graphs, indices, gens)
    for i in words:
        print(i,words[i])
    

    

    s_graph = pyvis.network.Network(directed = True, bgcolor = 'black', width = "800px", height = "800px")
    s_graph.add_nodes(indices, size = [5 for index in indices])

    for graph in graphs:
        for ind in graphs[graph]:
            s_graph.add_edge(
                ind,
                graphs[graph][ind],
                color = colors[graph])

    s_graph.toggle_physics(False)
    
    s_graph.show('s_graph.html')

    

    
    
if __name__ == "__main__":
    test_run()