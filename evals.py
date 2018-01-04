from splitresult import splitResult
import pandas as pd
#resultPath = tmpOutput


#TODO: split this function to newly annoted cctTestList

def evalPerform(cctTest, resultPath, eType, cols):
    results = splitResult(resultPath)
    cctTestList = sum(cctTest, [])
    if len(cctTestList) != len(results):
        return "Bad Performance, Not Match!!!"
    for idx in range(len(cctTestList)):
        cct    = cctTestList[idx]
        result = results[idx]
        cct.outputCols = cols 
        cct.coporResult(result=result[1], newTag= eType) ## TODO
        cct.score = result[0]
        cct.getLearnedEntities(eType)
    for cct in cctTestList:
        cct.getAnnotedEntities('ETag')
        cct.getLearnedEntities('ETag')
    df = pd.DataFrame([cct.data() for cct in cctTestList])
    Result = df.sum()
    Result = Result.to_dict()
    
    List = []
    entitiesLable = ['Sy','Bo', 'Ch', 'Tr', 'Si'] + ['R'] + ['E']
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

    R['P'] = R['matched']/R['learned']
    R['R'] = R['matched']/R['annoted']
    R['F1'] = 2*R['R']*R['P']/(R['R'] + R['P'])
    return R