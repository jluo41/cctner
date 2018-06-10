import os
import time
import pickle
from datetime import datetime
import pandas as pd
import numpy as np

from text import ChineseClinicalText as CCT
from dataset import batch_CCKS, batch_LUOHU, batch_LH_M, batch_LH_A, generateOriAn

import optparse 


def annoPickle(batch):
    
    pathDict = generateOriAn(**batch['dataInput'])
    CCTDict = {}
    timeConsmpt = []
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
    pkPath = rootPath + 'pkldata/'+ batch['name'] + '/' 
    
    try:
        os.mkdir(pkPath)
    except:
        pass

    with open(pkPath + 'CCT_Dict'+'.p', 'wb') as handle:
        pickle.dump(CCTDict, handle)

    with open(pkPath + 'CCT_Log' +'.p', 'wb') as handle:
        pickle.dump([batch, Time, etime, btime], handle)


parser = optparse.OptionParser()

parser.add_option(
    "-b", "--batch", default='ccks',
    help="batch name"
)


if __name__ == '__main__':
    opts = parser.parse_args()[0]
    assert opts.batch in ['ccks', 'luohu', 'luohuA', 'luohuM']


    batch = None
    if opts.batch == 'ccks':
        batch = batch_CCKS
        print('Batch CCKS \n')

    elif opts.batch == 'luohu':
        batch = batch_LUOHU
        print('Batch LUOHU\n' )

    elif opts.batch == 'luohuA':
        batch = batch_LH_A
        print('Batch LUOHU Antonomy\n')

    elif opts.batch == 'luohuM':
        batch = batch_LH_M
        print('Batch LUOHU Miscellany\n')

    else:
        pass


    print('Run annoPickle\n')
    btime = time.clock()
    annoPickle(batch)
    etime = time.clock()
    print(etime - btime)
    print('Time Consumption: ', (etime - btime) / 60, 'mins')
