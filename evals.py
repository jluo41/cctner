import pandas as pd
from splitresult import splitResult

#resultPath = tmpOutput

def match(L, A, cct):
    t1, start1, end1, e1 = L
    t2, start2, end2, e2 = A
    d = {}
    if set(range(start1, end1+1)).intersection(range(start2, end2+1)):
        idx = set(range(start1, end1+1)).union(range(start2, end2+1))
        # print()
        d['Text'] = cct._text[min(idx): max(idx) + 1]
        d['T_start'] = min(idx)
        d['T_end' ]  = max(idx) 
        d['Learned'] = t1
        d['LearnET'] = e1
        d['Annoted'] = t2
        d['AnnotET'] = e2
        d['FilePath']= cct.annotedFilePath
        return d
    
    
def matchUpair(unpaired, cct, kind):
    d = {}
    d['Text'], d['T_start'], d['T_end' ], e = unpaired
    d['FilePath']= cct.annotedFilePath
    if kind == 'L':
        d['Learned'], d['LearnET'] = d['Text'], e
        d['Annoted'], d['AnnotET'] = None, None
    else:
        d['Learned'], d['LearnET'] = None, None
        d['Annoted'], d['AnnotET'] = d['Text'], e
    return d


def logError(cct):
    log = []
    inter = list(set(cct.learnedEntities).intersection(set(cct.annotedEntities)))
    OnlyLearned = [ i for i in cct.learnedEntities if i not in inter]   
    OnlyAnnoted = [ i for i in cct.annotedEntities if i not in inter]
    
    pairedL = []
    pairedA = []
    for L in OnlyLearned:
        for A in OnlyAnnoted:
            d = match(L, A, cct)
            if d:
                log.append(d)
                pairedL.append(L)
                pairedA.append(A)
                
    for L in [i for i in OnlyLearned if i not in pairedL]:
        log.append(matchUpair(L, cct, 'L'))
        
    for A in [i for i in OnlyAnnoted if i not in pairedA]:
        log.append(matchUpair(A, cct, 'A'))
           
    if len(log) == 0:
        return pd.DataFrame()
    cols = ['FilePath', 'Text', 'T_start', 'T_end', 'Annoted', 'AnnotET', 'Learned', 'LearnET']
    return pd.DataFrame(log)[cols].sort_values('T_start')


def evalPerform(cctTest, resultPath, eType, cols, logPath = False):
    results = splitResult(resultPath)
    cctTestList = sum(cctTest, [])
    if len(cctTestList) != len(results):
        return "Bad Performance, Not Match!!!"
    for idx in range(len(cctTestList)):
        cct    = cctTestList[idx]
        result = results[idx]
        cct.outputCols = cols 
        cct.corpResult(result=result[1], newTag= eType) ## TODO
        cct.score = result[0]
        cct.getLearnedEntities(eType)
        
    if logPath:
        log_list = []
        for cct in cctTestList:
            a = logError(cct)
            if len(a) is not 0 :
                log_list.append(a)
        LogError = pd.concat(log_list).reset_index(drop = True)
        LogError.to_csv(logPath, encoding='utf-8')

    df = pd.DataFrame([cct.data() for cct in cctTestList])
    Result = df.sum()
    Result = Result.to_dict()
    
    List = []
    batch = cct.batch
    entitiesLable = list(batch['dataAnno']['fLabel'].values()) + ['E']
    # entitiesLable = ['Sy','Bo', 'Ch', 'Tr', 'Si'] + ['R'] + ['E']
    for i in entitiesLable:
        d = dict()
        d['id'] = i
        for k in Result:
            if i in k:
                d[k.replace('_','').replace(i,'')] = Result[k]
        List.append(d)
    
    R = pd.DataFrame(List)
    R.set_index('id', inplace = True)
    R.index.name = None

    R['R'] = R['Matched']/R['Annoted']
    R['P'] = R['Matched']/R['Learned']
    R['F1'] = 2*R['R']*R['P']/(R['R'] + R['P'])
    return R[['Annoted', 'Learned', 'Matched', 'R', 'P','F1']]