import random
import time
import pickle
import pandas as pd
import numpy as np
from splitresult import splitResult

pklDictPath = 'pkldata/2017-11-03/CCT_Dict.p'


filename = ['01-一般项目/一般项目-',
            '02-病史特点/病史特点-',
            '04-诊疗经过/诊疗经过-',
            '05-出院情况/出院情况-']

types = [item.split('/')[-1].replace('-', '') for item in filename]

def loadData(pklDictPath, seed):
    with open(pklDictPath, 'rb') as handle:
        cctDict = pickle.load(handle)
    
    cctTrain = []
    cctTest  = []
    n = 0
    for t in types:
        n+=1
        typeCCT = cctDict[t]
        random.seed(n*seed)
        l = random.sample(range(len(typeCCT)), int(len(typeCCT)*0.75))
        l.sort()
        cctTypeTrain = [typeCCT[idx] for idx in l]
        cctTrain.append(cctTypeTrain)
        cctTypeTest  = [typeCCT[idx] for idx in range(len(typeCCT)) if idx not in l]
        cctTest.append(cctTypeTest)
    return cctTrain, cctTest

def getTrainData(cctTrain, cols= None, Path = None):
    ## TODO
    ## Too slow here.
    for t in cctTrain:
        for cct in t:
            cct.getAnnotedEntities('RTag')
            cct.coporAnnotation('RTag')
            cct.getAnnotedEntities('ETag')
            cct.coporAnnotation('ETag')
            cct.outputCols = cols
    DFtrain = pd.DataFrame()
    for t in cctTrain:
        for cct in t:
            df = cct.dfFormat.copy()
            df = df.dropna()
            df.loc[len(df)] = np.NaN     ## Trick Here
            DFtrain = DFtrain.append(df) ## Trick Here
    DFtrain = DFtrain.reset_index(drop=True)
    DFtrain.to_csv(Path, columns = cols, sep = '\t', encoding = 'utf=8', header = False, index = False )

    
def getTestData(cctTest, cols, Path):
    DFtest = pd.DataFrame()
    for t in cctTest:
        for cct in t:
            cct.outputCols = cols
            df = cct.dfFormat.copy()
            df = df.dropna()
            df.loc[len(df)] = np.NaN     ## Trick Here
            DFtest = DFtest.append(df)   ## Trick Here
    DFtest = DFtest.reset_index(drop=True)
    DFtest.to_csv(Path, columns = cols, sep = '\t', encoding = 'utf=8', 
                  header = False, index = False )

def getTestData2(cctTest, cols, Path, resultPath):
    results = splitResult(resultPath)
    cctTestList = sum(cctTest, [])
    if len(cctTestList) != len(results):
        return "Bad Performance, Not Match!!!"

    DFtest = pd.DataFrame()
    for idx in range(len(cctTestList)):
        cct    = cctTestList[idx]
        result = results[idx]
        #cct.outputCols = cols 
        cct.coporResult(result=result[1], newTag= 'RTag') ## TODO
        cct.score = result[0]
        #cct.getLearnedEntities('RTag')
        cct.outputCols = cols
        df = cct.dfFormat.copy()
        df = df.dropna()
        df.loc[len(df)] = np.NaN     ## Trick Here
        DFtest = DFtest.append(df)   ## Trick Here
    DFtest = DFtest.reset_index(drop=True)
    DFtest.to_csv(Path, columns = cols, sep = '\t', encoding = 'utf=8', 
                  header = False, index = False )

    


if __name__ == '__main__':
    pklDictPath = 'pkldata/2017-11-03/CCT_Dict.p'
    btime = time.clock()
    cctTrain, cctTest = loadData(pklDictPath, 1)
    etime = time.clock()
    print(etime - btime)
    print([len(i) for i in cctTrain])
    print([len(i) for i in cctTest])

    trainDataPara = {'cols': ['_atom', 'basicTag', 'dictTag', 'POSTag', 'ETag'],
                     'Path':'demo/train.txt'}

    btime = time.clock()
    df = getTrainData(cctTrain, **trainDataPara)
    etime = time.clock()
    print(etime - btime)

    testDataPara = {'cols': ['_atom', 'basicTag', 'dictTag', 'POSTag' ],
                    'Path':'demo/test.txt'}

    btime = time.clock()
    getTestData(cctTest, **testDataPara)
    etime = time.clock()
    print(etime - btime)







