import os
import time
import codecs
import optparse 
import pickle

import numpy as np
import pandas as pd


from dataset import batch1, batch2
from text import ChineseClinicalText as CCT
from crftools import crf_test

from tabulate import tabulate


parser = optparse.OptionParser()

parser.add_option(
    "-m", "--model", default='1abdp',
    help="Model name"
)

parser.add_option(
    "-i", "--input", default="",
    help="Input file location"
)

parser.add_option(
    "-o", "--output", default="",
    help="Output file location"
)

def tagger(model, inputPathFile, outputPathFile, batch):

    cct = CCT(originalFilePath=inputPathFile, batch = batch)
    cct.execute()
    tmp = inputPathFile.split('/')[-1]
    fileName = tmp.split('.')[0]

    with open(rootMPath + model + '/para.p', 'rb') as handle:
        para = pickle.load(handle)

    if para['arch'] == 1:

        print("Loading Model...")
        btime = time.clock()

        tmpInput  = 'demo/tmp/' + model + '-'+ fileName + '-Test' + '.txt'
        tmpOutput = 'demo/tmp/' + model + '-'+ fileName + '-Rslt' + '.txt'

        cct.toTextFile(tmpInput, cols = para['cols'])

        crf_test(crf_test_path = para['crf_testPath'],
                 modelpath     = para['modelPath'],
                 testfilepath  = tmpInput,
                 resultpath    = tmpOutput)

        result = pd.read_csv(tmpOutput, sep = '\t', comment = '#', header= None, skip_blank_lines= False)

        cct.corpResult(result, 'LearnedETag')

        print('Text Input:')
        print('--------------------------')
        with open(inputPathFile, 'r') as f:
            print(f.read())
        print('--------------------------\n')
                
        etime = time.clock()
    
        columns = ['E-Name', 'E-Start', 'E-End', 'E-Type']
        Data = pd.DataFrame(cct.getLearnedEntities('LearnedETag'), columns= columns )
        Data.to_csv(outputPathFile, sep = '\t')
        
        print('Entity Result:\n')
        print(tabulate(Data,headers=Data.columns,tablefmt="psql", numalign="left"))
        print('\nTime Consumption %f s' % (etime - btime))


    if para['arch'] == 2:

        print("Loading 1 Layer Model...")
        btime = time.clock()

        tmpInput1  = 'demo/tmp/' + model + '-' + fileName + '-1Test' + '.txt'
        tmpOutput1 = 'demo/tmp/' + model + '-' + fileName + '-1Rslt' + '.txt'

        cct.toTextFile(tmpInput1, cols = para['cols'])

        crf_test(crf_test_path = para['crf_testPath'],
                 modelpath     = para['modelPath1'],
                 testfilepath  = tmpInput1,
                 resultpath    = tmpOutput1,
                 concise       = True)

        result = pd.read_csv(tmpOutput1, sep = '\t', comment = '#', header= None, skip_blank_lines= False)
        # cct.corpResult(result, 'RTag')

        tmpInput2  = 'demo/tmp/' + model + '-' + fileName + '-2Test' + '.txt'
        tmpOutput2 = 'demo/tmp/' + model + '-' + fileName + '-2Rslt' + '.txt'

        pd.read_csv(tmpOutput1, sep = '\t', header = None).to_csv(tmpInput2, sep = '\t', header = None, index=None)
        # cct.toTextFile(tmpInput2, cols = para['testCols2'])

        crf_test(crf_test_path = para['crf_testPath'],
                 modelpath     = para['modelPath2'],
                 testfilepath  = tmpInput2,
                 resultpath    = tmpOutput2)

        result = pd.read_csv(tmpOutput2, sep = '\t', comment = '#', header= None, skip_blank_lines= False)
        cct.outputCols = para['eval_cols']
        cct.corpResult(result, 'LearnedETag')

        print('Text Input:')
        print('--------------------------')
        with open(inputPathFile, 'r') as f:
            print(f.read())
        print('--------------------------\n')

        etime = time.clock()

        print('\nTime Consumption %f s' % (etime - btime))

        columns = ['E-Name', 'E-Start', 'E-End', 'E-Type']
        Data = pd.DataFrame(cct.getLearnedEntities('LearnedETag'), columns= columns )
        Data.to_csv(outputPathFile, sep = '\t')
        
        print('Entity Result:\n')
        print(tabulate(Data,headers=Data.columns,tablefmt="psql", numalign="left"))
        print('\nTime Consumption %f s' % (etime - btime))



if __name__ == '__main__':
    opts = parser.parse_args()[0]

    # Check parameters validity
    # assert opts.delimiter
    # print(opts.model)
    # print(os.path.isdir(opts.model))
    # assert os.path.isdir(opts.model)
    assert os.path.isfile(opts.input)

    # Load existing model
    # model = Model(model_path=opts.model)
    # parameters = model.parameters
    rootMPath = 'models/'
    model = opts.model 
    inputPathFile = opts.input
    outputPathFile = opts.output
    tagger(model, inputPathFile, outputPathFile, batch1)














