

import os
import time
import codecs
import optparse 
import pickle

import numpy as np
from pandas import read_csv
# from loader import prepare_sentence
# from utils import create_input, iobes_iob, zero_digits
# from model import Model

from text import ChineseClinicalText as CCT
from crftools import crf_test


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

def tagger(model, inputPathFile, outputPathFile):

    

    cct = CCT(originalFilePath=inputPathFile)
    cct.execute()
    tmp = inputPathFile.split('/')[-1]
    fileName = tmp.split('.')[0]

    with open(rootMPath + model + '/para.p', 'rb') as handle:
        para = pickle.load(handle)

    if para['arch'] == 1:

        print("Loading Model...")
        btime = time.clock()

        tmpInput  = 'demo/tmp/' + model + fileName + '-Test' + '.txt'
        tmpOutput = 'demo/tmp/' + model + fileName + '-Rslt' + '.txt'

        cct.toTextFile(tmpInput, cols = para['testCols'])

        crf_test(crf_test_path = para['testPath'],
                 modelpath     = para['modelPath'],
                 testfilepath  = tmpInput,
                 resultpath    = tmpOutput)

        result = read_csv(tmpOutput, sep = '\t', comment = '#', header= None, skip_blank_lines= False)

        cct.coporResult(result, 'ETag')

        print('Text Input:')
        print('--------------------------')
        with open(inputPathFile, 'r') as f:
            print(f.read())
        print('--------------------------\n')
                
        etime = time.clock()
    
        with open(outputPathFile, 'w', encoding = 'utf-8') as f:
            for en in cct.getLearnedEntities('ETag'):
                f.write('\t'.join([str(i) for i in en])+'\n')
        
        print('Entity Result:\n')
        print(read_csv(outputPathFile, sep = '\t', header = None))
        print('\nTime Consumption %f s' % (etime - btime))


    if para['arch'] == 2:

        print("Loading 1 Layer Model...")
        btime = time.clock()

        tmpInput1  = 'demo/tmp/' + model + fileName + '-1Test' + '.txt'
        tmpOutput1 = 'demo/tmp/' + model + fileName + '-1Rslt' + '.txt'

        cct.toTextFile(tmpInput1, cols = para['testCols1'])

        crf_test(crf_test_path = para['testPath'],
                 modelpath     = para['modelPath1'],
                 testfilepath  = tmpInput1,
                 resultpath    = tmpOutput1)

        result = read_csv(tmpOutput1, sep = '\t', comment = '#', header= None, skip_blank_lines= False)
        cct.coporResult(result, 'RTag')

        tmpInput2  = 'demo/tmp/' + model + fileName + '-2Test' + '.txt'
        tmpOutput2 = 'demo/tmp/' + model + fileName + '-2Rslt' + '.txt'
        cct.toTextFile(tmpInput2, cols = para['testCols2'])

        crf_test(crf_test_path = para['testPath'],
                 modelpath     = para['modelPath2'],
                 testfilepath  = tmpInput2,
                 resultpath    = tmpOutput2)

        result = read_csv(tmpOutput2, sep = '\t', comment = '#', header= None, skip_blank_lines= False)
        cct.coporResult(result, 'ETag')

        print('Text Input:')
        print('--------------------------')
        with open(inputPathFile, 'r') as f:
            print(f.read())
        print('--------------------------\n')

        etime = time.clock()

        print('\nTime Consumption %f s' % (etime - btime))

        with open(outputPathFile, 'w', encoding = 'utf-8') as f:
            for en in cct.getLearnedEntities('ETag'):
                f.write('\t\t'.join([str(i) for i in en])+'\n')

        print('Entity Result:\n')
        print(read_csv(outputPathFile, sep = '\t', header = None))
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
    tagger(model, inputPathFile, outputPathFile)














