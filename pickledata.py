import os
import time
import pickle
from datetime import datetime
import pandas as pd
import numpy as np

from text import ChineseClinicalText as CCT

filename = ['01-一般项目/一般项目-',
            '02-病史特点/病史特点-',
            '04-诊疗经过/诊疗经过-',
            '05-出院情况/出院情况-']

types = [item.split('/')[-1].replace('-', '') for item in filename]


# btime = time.clock()

fpath = 'dataset/annoted/'

now = datetime.now()
date = now.date()

def getFilePath(name, ind):
    orig = fpath + name + str(ind) + '.txtoriginal.txt'
    anno = fpath + name + str(ind) + '.txt'
    return {'originalFilePath': orig, 'annotedFilePath' : anno}


def origPickle(length):
    timeConsmpt = []
    CCTList = []
    Missing = []
    for name in filename:
        for ind in range(length):
            bbtime = time.clock()
            d = getFilePath(name, ind + 1)
            flg = True
            for i in d.values():
                if not os.path.isfile(i):
                    flg = False
                    Missing.append(i)
            if not flg:
                continue
            if (ind + 1) % 10 == 0:
                print(ind + 1)
            cct = CCT(**getFilePath(name, ind + 1))
            cct.execute()
            ##
            CCTList.append(cct)
            eetime = time.clock()
            timeConsmpt.append([name + str(ind + 1), eetime - bbtime])

    Time = pd.Series([i[-1] for i in timeConsmpt])

    cctDict = {}
    for t in types:
        cctDict[t] = []

    for cct in CCTList:
        for t in types:
            if t in cct.originalFilePath:
                cctDict[t].append(cct)
                break

    now = datetime.now()
    date = now.date()
    print(date)

    try:
        os.mkdir('pkldata/' + str(date))
    except:
        pass

    with open('pkldata/' + str(date) + '/CCT_List' + '.p', 'wb') as handle:
        pickle.dump(CCTList, handle)

    with open('pkldata/' + str(date) + '/CCT_Dict' + '.p', 'wb') as handle:
        pickle.dump(cctDict, handle)

    with open('pkldata/' + str(date) + '/CCT_Log'  + '.p', 'wb') as handle:
        pickle.dump([Time, timeConsmpt, Missing], handle)


def annoPickle(length):
    timeConsmpt = []
    CCTList = []
    Missing = []
    for name in filename:
        # name = filename[2]
        for ind in range(length):
            bbtime = time.clock()
            ## To check whether a file exists.
            d = getFilePath(name, ind + 1)
            flg = True
            for i in d.values():
                if not os.path.isfile(i):
                    flg = False
                    Missing.append(i)
            if not flg:
                continue

            if (ind + 1) % 10 == 0:
                print(ind + 1)

            cct = CCT(**getFilePath(name, ind + 1))
            cct.execute()
            cct.getAnnotedEntities('RTag')
            cct.coporAnnotation('RTag')
            cct.getAnnotedEntities('ETag')
            cct.coporAnnotation('ETag')
            CCTList.append(cct)
            eetime = time.clock()
            timeConsmpt.append([name + str(ind + 1), eetime - bbtime])

    Time = pd.Series([i[-1] for i in timeConsmpt])

    cctDict = {}
    for t in types:
        cctDict[t] = []

    for cct in CCTList:
        for t in types:
            if t in cct.originalFilePath:
                cctDict[t].append(cct)
                break
    now = datetime.now()
    date = now.date()
    print(date)

    try:
        os.mkdir('pkldata/' + str(date))
    except:
        pass

    with open('pkldata/' + str(date) + '/R_CCT_List' + '.p', 'wb') as handle:
        pickle.dump(CCTList, handle)

    with open('pkldata/' + str(date) + '/R_CCT_Dict' + '.p', 'wb') as handle:
        pickle.dump(cctDict, handle)

    with open('pkldata/' + str(date) + '/R_CCT_Log'  + '.p', 'wb') as handle:
        pickle.dump([Time, timeConsmpt, Missing], handle)


if __name__ == '__main__':
    length = 300
    print('Run origPickle')
    btime = time.clock()
    origPickle(length)
    etime = time.clock()
    print(etime - btime)
    print('Time Consumption: ', (etime - btime) / 60, 'mins')

    print('Run origPickle')
    btime = time.clock()
    annoPickle(length)
    etime = time.clock()
    print(etime - btime)
    print('Time Consumption: ', (etime - btime) / 60, 'mins')
