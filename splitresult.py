import pandas as pd
from io import StringIO


def splitResult(outputPath):
    lineIdx = []
    scores1 = []
    with open(outputPath, 'r') as f:
        n = 0
        for l in f.readlines():
            if l[:3] =='# 1' or l[:3] == '# 0':
                scores1.append(l.replace('# ', '').replace('\n',''))
                lineIdx.append(n)
            n+=1
        lineIdx.append(n-1)
    results = []
    with open(outputPath, 'r') as f:
        lines = f.readlines()
        for ii in range(len(lineIdx)-1):
            sentence = lines[lineIdx[ii]:lineIdx[ii+1]]
            f = StringIO(''.join(sentence[1:]))
            result = pd.read_csv(f, sep = '\t', 
                                 comment = '#', 
                                 header= None, 
                                 skip_blank_lines= False)
            score = sentence[0]
            score = score.replace('# ', '').replace('\n','')#
            results.append([score, result])
    
    assert scores1 == [r[0] for r in results] # Test the right result
    
    return results

    