import random
import time
import pickle
import pandas as pd
import numpy as np
from splitresult import splitResult

from vector import cct2VecDF

from dataset import batch_LUOHU




def getCrossValidationIdx(length, cross_num, pad = -1):
    
    length_pad = (int(length/cross_num) + 1 ) * cross_num
    #print(length_pad)
    new_list = list(range(length)) + [pad] * (length_pad - length)
    #print(new_list)

    cross_index = np.array(random.sample(new_list, length_pad))
    #cross_index.sort()
    return cross_index.reshape((cross_num, -1))




def loadData(pklDictPath, batch, cross_num,  
             seed = 10,
             cross_validation = False, 
             cross_idx = 0,
             pad = -1):

    random.seed(seed)

    with open(pklDictPath, 'rb') as handle:
        cctDict_R = pickle.load(handle)
    
    cctTrain = []
    cctTest  = []

    if not cross_validation:

        for t in batch['dataInput']['filenames']:
            typeCCT = CCTDict[t]
            random.seed(10)
            l = random.sample(range(len(typeCCT)), int(len(typeCCT)/cross_num))
            l.sort()
            cctTypeTrain = [typeCCT[idx] for idx in l]
            cctTrain.append(cctTypeTrain)
            cctTypeTest  = [typeCCT[idx] for idx in range(len(typeCCT)) if idx not in l]
            cctTest.append(cctTypeTest)
    else:
        
        for t in  batch['dataInput']['filenames']:
            typeCCT = cctDict_R[t]
            cross_index = getCrossValidationIdx(len(typeCCT), cross_num, pad = pad)
            test_index = cross_index[cross_idx, ]
            test_index = [idx for idx in test_index if idx is not pad] # get rid of pad
            #l = random.sample(range(len(typeCCT)), int(len(typeCCT)/section_num))
            #l.sort()
            cctTypeTest = [typeCCT[idx] for idx in test_index]
            cctTest.append(cctTypeTest)
            cctTypeTrain  = [typeCCT[idx] for idx in range(len(typeCCT)) if idx not in test_index]
            cctTrain.append(cctTypeTrain)
        
    return cctTrain, cctTest


def getTrainData(cctTrain, attr_cols = None, tag_cols = None,  
                 Path = None, 
                 Vector = False, 
                 vect_cols = None, 
                 Vdim = None, 
                 vect_path = None):

    DFtrain = pd.DataFrame()
    for t in cctTrain:
        for cct in t:
            df = cct.dfFormat.copy()
            df = df.dropna()
            df.loc[len(df)] = np.NaN     ## Trick Here
            df = df[attr_cols + tag_cols]
            
            if Vector == True and vect_cols:
                df_vec = cct2VecDF(cct, dim = Vdim, path = vect_path)
                df_vec = df_vec.dropna()
                df_vec.loc[len(df_vec)] = np.NaN
                assert len(df_vec) == len(df)
                df = pd.concat([df, df_vec], axis = 1)
                df = df[attr_cols + vect_cols + tag_cols]
                #print(df)
                
            DFtrain = DFtrain.append(df) ## Trick Here
    DFtrain = DFtrain.reset_index(drop=True)
    # DFtrain = DFtrain[cols]
    DFtrain.to_csv(Path, sep = '\t', encoding = 'utf=8', header = False, index = False )
    # return DFtrain

def getTestData(cctTest, attr_cols = None,  
                Path = None,
                Vector = False,
                Vdim = None,
                vect_cols = None,
                vect_path = None):

    DFtest = pd.DataFrame()
    for t in cctTest:
        for cct in t:
            cct.outputCols = attr_cols
            df = cct.dfFormat.copy()
            df = df.dropna()
            df.loc[len(df)] = np.NaN    ## Trick Here
            df = df[attr_cols]
            
            if Vector == True and vect_cols:
                df_vec = cct2VecDF(cct, dim = Vdim, path = vect_path)
                df_vec = df_vec.dropna()
                df_vec.loc[len(df_vec)] = np.NaN
                assert len(df_vec) == len(df)
                df = pd.concat([df, df_vec], axis = 1)
                df = df[attr_cols + vect_cols ]

            DFtest = DFtest.append(df)   ## Trick Here

    DFtest = DFtest.reset_index(drop=True)
    DFtest.to_csv(Path, sep = '\t', encoding = 'utf=8', 
                  header = False, index = False )
    #return DFtest

def getTestData2(TempPath,
                 Test2Path):
    
    Test2Data = pd.read_csv(TempPath, 
                            sep = '\t', 
                            header = None, 
                            skip_blank_lines=False)
    Test2Data.to_csv(Test2Path, 
                     sep = '\t', 
                     encoding = 'utf=8', 
                     header = False, 
                     index = False )

if __name__ == '__main__':
    batch =batch_LUOHU
    pklDictPath = 'pkldata/luohu/CCT_Dict.p'
    cross_num = 10

    btime = time.clock()
    cctTrain, cctTest = loadData(pklDictPath, batch, cross_num,  
                                 seed = 10,
                                 cross_validation = False, 
                                 cross_idx = 0)
    etime = time.clock()

    print(etime - btime)
    print([len(i) for i in cctTrain])
    print([len(i) for i in cctTest])

    DIM = 50
    
    trainDataPara = {'vect_cols': list(range(1,DIM + 1)),
                     'Vector': True,
                     'Vdim': 50,
                     'attr_cols': ['_atom'],
                     'tag_cols' : ['ETag'],
                     'Path':'demo/train.txt'}

    btime = time.clock()
    getTrainData(cctTrain, **trainDataPara)
    etime = time.clock()
    print(etime - btime)

    
    testDataPara = {'attr_cols': ['_atom'],
                    'vect_cols': list(range(1,DIM + 1)),
                    'Vector': True,
                    'Vdim': 50,
                    'Path':'demo/test.txt'}

    btime = time.clock()
    getTestData(cctTest, **testDataPara)
    etime = time.clock()
    print(etime - btime)


