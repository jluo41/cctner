import os
import time
import pickle
from datetime import datetime
import pandas as pd
import numpy as np

from text import ChineseClinicalText as CCT
from dataset import batch1, batch2, generateOriAn

def annoPickle(batch):
    
    pathDict = generateOriAn(**batch['dataInput'])
    CCTDict = {}

    for filename in pathDict:
        CCTDict[filename] = []
        for cctPathDict in pathDict[filename]:
            #print(cctPathDict['originalFilePath'])
            bbtime = time.clock()
            cct = CCT(batch, **cctPathDict)
            cct.execute()
            cct.getAnnotedEntities('RTag')
            cct.corpAnnotation('RTag')
            cct.getAnnotedEntities('ETag')
            cct.corpAnnotation('ETag')
            CCTDict[filename].append(cct)
            eetime = time.clock()     
            timeConsmpt.append(eetime - bbtime)

    etime = time.clock()
    
    Time = pd.Series(timeConsmpt)
    now = datetime.now()
    date = now.date()
    print(date)
    rootPath = batch['dataInput']['rootPath']
    pkPath = rootPath + 'pkldata/'+ batch['name'] + '-' + str(date)
    
    try:
        os.mkdir(pkPath)
    except:
        pass

    with open(pkPath + '/CCT_Dict'+'.p', 'wb') as handle:
        pickle.dump(CCTDict, handle)

    with open(pkPath + '/CCT_Log' +'.p', 'wb') as handle:
        pickle.dump([Time, etime, btime ], handle)


if __name__ == '__main__':
    batch = batch1
    print('Run origPickle')
    btime = time.clock()
    annoPickle(batch)
    etime = time.clock()
    print(etime - btime)
    print('Time Consumption: ', (etime - btime) / 60, 'mins')
