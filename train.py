import os
import optparse 
from loaddata import loadData, getTrainData, getTestData, getTestData2
from crftools import crf_learn, crf_test
import time 
from evals import evalPerform
import pickle
# from splitresult import splitResult

attrLable = {}
attrLable['a'] = '_atom'
attrLable['b'] = 'basicTag'
attrLable['d'] = 'dictTag'
attrLable['r'] = 'radical'
attrLable['p'] = 'POSTag'
attrLable['R'] = 'RTag'
attrLable['E'] = 'ETag'

def genPara(modelLabel, vect = None, lstm = None):
    para = {}
    para['arch']  = int(modelLabel[0])
    para['attrs'] = list(modelLabel)[1:]
    para['cols']  = [attrLable[i] for i in para['attrs']]
    para['path']  = 'models/'+ modelLabel
    para['crf_learnPath'] = 'crftools/crf_learn'
    para['crf_testPath']  = 'crftools/crf_test'
    ## CRF Para
    learn_params2 = {'-f': '2',
                     '-c': '5.0',
                     '-t': None,
                     '-p': '4'}
    para['crfPara'] = learn_params2

    ## CRF Template
    p = 'template/'
    templatePath = {}
    templatePath[1] = [p + 'template0']
    templatePath[2] = [p + 'template01', p + 'template1' ]
    templatePath[3] = [p + 'template11']
    templatePath[4] = [p + 'templateFor5Tag']
    templatePath['v']=[p + 'template-v51']
    
    para['vect'] = {}
    if vect:
        para['vect']['Vector']   = True
        para['vect']['Vdim']     = int(vect.replace('vect-',''))
        para['vect']['vect_cols']= list(range(1,para['vect']['Vdim'] + 1))
        para['vect']['vect_path']= 'vector/'+ vect + '.txt'
        
        para['path'] += '-v'+str(para['vect']['Vdim'])
        
    para['lstm'] ={}
    if lstm:
        pass
    
    para['performPath']   = para['path'] + '/peformance.txt'
    para['logPath']  = para['path'] + '/logError.csv'
    para['paraPath']  = para['path'] + '/para.p'
    para['eval_cols'] = para['cols'].copy()

    if para['arch'] == 1:
        para['tag_cols'] = ['ETag']
        para['trainDataPath'] = para['path'] + '/output/trainData.txt'
        para['testDataPath']  = para['path'] + '/output/testData.txt'
        para['testDataResultPath'] = para['path'] + '/output/testDataResult.txt'
        para['modelPath'] = para['path'] + '/model'
        para['evalTag']   = 'LearnedETag'
        para['template'] = templatePath[len(para['attrs'])][0]
        if vect:
            para['template'] = templatePath['v'][0]
            para['eval_cols']+= para['vect']['vect_cols']
            
   
    if para['arch'] == 2:
        para['tag_cols1'] = ['RTag']
        para['tag_cols2'] = ['RTag', 'ETag']
        para['eval_cols'] = para['cols'].copy() + ['RTag']

        para['trainDataPath1'] = para['path'] + '/output/trainData1.txt'
        para['trainDataPath2'] = para['path'] + '/output/trainData2.txt'
        para['testDataPath1']  = para['path'] + '/output/testData1.txt'
        para['testDataPath2']  = para['path'] + '/output/testData2.txt'
        para['testDataResultPath1'] = para['path'] + '/output/testDataResult1.txt'
        para['testDataResultPath2'] = para['path'] + '/output/testDataResult2.txt'

        para['modelPath1'] = para['path'] + '/model1'
        para['modelPath2'] = para['path'] + '/model2'
        para['evalTag']   = 'LearnedETag'
        para['template1'] = templatePath[len(para['cols'])][0]
        para['template2'] = templatePath[len(para['cols']) + 1][0]
        if vect:
            para['template'] = templatePath['v'][0]
            para['eval_cols']= para['cols'].copy()  + para['vect']['vect_cols'] + ['RTag']
        
    return para


def trainModel(para, pklDictPath):
    try:
        os.mkdir(para['path'])
        os.mkdir(para['path']+ '/output')
    except:
        pass

    print('\nLoading Data\n')
    cctTrain, cctTest = loadData(pklDictPath, 10)
    if para['arch'] == 1:
        print('Loading Train Data\n')
        getTrainData(cctTrain, attr_cols = para['cols'], tag_cols = para['tag_cols'], Path = para['trainDataPath'],
                     **para['vect'])
        
        
        print('Loading Test Data\n')
        getTestData(cctTest,  attr_cols = para['cols'], Path = para['testDataPath'], **para['vect'])
        
        print('Start Learning ... \n')
        btime = time.clock()
        crf_learn(crf_learn_path = para['crf_learnPath'],
                  params         = para['crfPara'],
                  templatepath   = para['template'],
                  trainpath      = para['trainDataPath'],
                  modelname      = para['modelPath'])
        etime = time.clock()
        print('Time Consumption:', etime - btime,'s\n')
        

        print('Start Predicting ... ')
        btime = time.clock()
        crf_test(crf_test_path = para['crf_testPath'],
                 modelpath     = para['modelPath'],
                 testfilepath  = para['testDataPath'],
                 resultpath    = para['testDataResultPath'])
        etime = time.clock()
        print('Time Consumption:', etime - btime,'s\n')
        #'''
        print('Evaluating ... ')
        btime = time.clock()
        R = evalPerform(cctTest, para['testDataResultPath'], para['evalTag'], para['eval_cols'], logPath = para['logPath'])
        '''
        with open('test/problem.p', 'wb') as handle:
            pickle.dump([cctTrain, cctTest , para], handle)
        '''
        R = R.dropna()
        print(R)
        R.to_csv(para['performPath'], sep = '\t')
        para['perform'] = R
        etime = time.clock()
        print('Time Consumption:', etime - btime,'s\n')

        with open(para['paraPath'], 'wb') as handle:
            pickle.dump(para, handle)



    if para['arch'] == 2:
        
        print('Loading  Train Data 1')
        getTrainData(cctTrain, attr_cols = para['cols'], tag_cols = para['tag_cols1'], Path = para['trainDataPath1'])
        print('Finished Train Data 1\n')

        print('Loading  Train Data 2')
        getTrainData(cctTrain, attr_cols = para['cols'], tag_cols = para['tag_cols2'], Path = para['trainDataPath2'])
        print('Finished Train Data 2\n')

        
        print('Loading  Test Data 1')
        getTestData(cctTest,  attr_cols = para['cols'],  Path = para['testDataPath1'])
        print('Finished Test Data 1\n')

        
        print('Start  Learning -1- ... \n')
        btime = time.clock()
        crf_learn(crf_learn_path = para['crf_learnPath'],
                  params         = para['crfPara'],
                  templatepath   = para['template1'],
                  trainpath      = para['trainDataPath1'],
                  modelname      = para['modelPath1'])
        etime = time.clock()
        print('Time Consumption:', etime - btime,'s\n')
        
        
        print('Start Predicting -1- ... ')
        btime = time.clock()
        crf_test(crf_test_path = para['crf_testPath'],
                 modelpath     = para['modelPath1'],
                 testfilepath  = para['testDataPath1'],
                 resultpath    = para['testDataResultPath1'],
                 concise       = True)
        etime = time.clock()
        print('Time Consumption:', etime - btime,'s\n')
        
        # results = splitResult(para['testDataResultPath1'])
        getTestData2(para['testDataResultPath1'], para['testDataPath2'])
        
        print('Start  Learning -2- ... \n')
        btime = time.clock()
        crf_learn(crf_learn_path = para['crf_learnPath'],
                  params         = para['crfPara'],
                  templatepath   = para['template2'],
                  trainpath      = para['trainDataPath2'],
                  modelname      = para['modelPath2'])
        etime = time.clock()
        print('Time Consumption:', etime - btime,'s\n')
        
        
        print('Start Predicting -2- ... ')
        btime = time.clock()
        crf_test(crf_test_path = para['crf_testPath'],
                 modelpath     = para['modelPath2'],
                 testfilepath  = para['testDataPath2'],
                 resultpath    = para['testDataResultPath2'] )
        etime = time.clock()
        print('Time Consumption:', etime - btime,'s\n')
        
        print('Evaluating ... ')
        btime = time.clock()
        R = evalPerform(cctTest, para['testDataResultPath2'], para['evalTag'],  para['eval_cols'], logPath = para['logPath'])
        R = R.dropna()
        print(R)
        R.to_csv(para['performPath'], sep = '\t')
        para['perform'] = R
        etime = time.clock()
        print('Time Consumption:', etime - btime,'s\n')

        with open(para['paraPath'], 'wb') as handle:
            pickle.dump(para, handle)



if __name__ == '__main__':
    pklDictPath = 'pkldata/CCKS-2018-04-04/CCT_Dict.p'

    parser = optparse.OptionParser()
    parser.add_option("-m", "--model", default='',
                      help="Model Name")
    parser.add_option("-v", "--vector", default = '',
                      help='Word2Vector Dim')

    opts = parser.parse_args()[0]

    modelLabel = opts.model
    vect       = opts.vector
    #lstm       = opts.lstm
    # modelLabel = '1abdp'

    assert int(modelLabel[0]) == 2 or int(modelLabel[0]) == 1
    assert modelLabel[1] == 'a'

    if vect:
        assert vect[:5] == 'vect-'

    para = genPara(modelLabel, vect = vect)

    trainModel(para, pklDictPath)



