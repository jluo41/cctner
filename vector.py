from text import ChineseClinicalText 
import pandas as pd 

p = '/Users/floyd/Desktop/Research/NER-CRF/cctner' + '/vector/vect-50.txt'    

#p = '/vector/char2vec.txt'
def char2vec(Char, vecFilepath, dim):
    # to fix it, in the future
    l = []
    with open(vecFilepath, 'r') as f:
        for i in f.readlines():
            if i[0] == Char:            
                l = i.split(' ')[1:-1]
                break
    return l if len(l) == dim else [0]*dim


def cct2VecDF(cct, dim, path = p):
    L = []
    if not path:
        path = p
    for i in cct.atoms:
        L.append([i._atom] + char2vec(i._atom, path, dim))     
    return pd.DataFrame(L)

