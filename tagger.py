import os
import time
import codecs
import optparse 
import pickle

import numpy as np
import pandas as pd


from dataset import batch_CCKS, batch_LUOHU, batch_LH_M, batch_LH_A, generateOriAn

from text import ChineseClinicalText as CCT
from crftools import crf_test

from tabulate import tabulate

from vector import cct2VecDF

def tagger(model, inputPathFile, outputPathFile, batch):

    cct = CCT(originalFilePath=inputPathFile, batch = batch)
    cct.execute()
    tmp = inputPathFile.split('/')[-1]
    fileName = tmp.split('.')[0]

    parapath = 'models/' + batch['name'] + '/'+ model + '/para.p' #  , 'rb'
    if not os.path.isfile(parapath):
    	parapath = 'models/' + batch['name'] + '/'+ model + '_0/para.p' # , 'rb'
    
    with open(parapath, 'rb') as handle:
        para = pickle.load(handle)

    if para['arch'] == 1:

        print("Loading Model...")
        btime = time.clock()

        tmpInput  = 'demo/tmp/' + model + '-'+ fileName + '-Test' + '.txt'
        tmpOutput = 'demo/tmp/' + model + '-'+ fileName + '-Rslt' + '.txt'

        if not para['vect']['Vector']:
            cct.toTextFile(tmpInput, cols = para['cols'])
        else:
            cct.outputCols = para['cols']
            df = cct.dfFormat.copy()
            df = df.dropna()
            df.loc[len(df)] = np.NaN    ## Trick Here
            df = df[para['cols']]

            df_vec = cct2VecDF(cct, dim = para['vect']['Vdim'], path = para['vect']['vect_path'])
            df_vec = df_vec.dropna()
            df_vec.loc[len(df_vec)] = np.NaN

            df = pd.concat([df, df_vec], axis = 1)
            df = df[  para['cols'] + para['vect']['vect_cols'] ]
            df.to_csv(tmpInput, sep = '\t', encoding = 'utf=8', header = False, index = False )

        crf_test(crf_test_path = para['crf_testPath'],
                 modelpath     = para['modelPath'],
                 testfilepath  = tmpInput,
                 resultpath    = tmpOutput)

        result = pd.read_csv(tmpOutput, sep = '\t', comment = '#', header= None, skip_blank_lines= False)
        
        cct.outputCols = para['eval_cols']
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

parser.add_option(
    "-b", "--batch", default="ccks",
    help="batch name"
)


if __name__ == '__main__':
    opts = parser.parse_args()[0]

    assert os.path.isfile(opts.input)

    model = opts.model 
    inputPathFile = opts.input
    outputPathFile = opts.output

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
    
    tagger(model, inputPathFile, outputPathFile, batch)
