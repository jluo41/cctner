
import pandas as pd

console_encoding = 'gb2312'
file_encoding = 'utf-8'



def dict2list(paramdict):
    resultlist = []
    for k, v in paramdict.items():
        resultlist.append(k)
        if v:
            resultlist.append(v)
    return resultlist


def shell_invoke(args, sinput = None, soutput = None):
    import subprocess
    if sinput and soutput:
        p = subprocess.Popen(args, stdin = sinput, stdout= soutput)
    elif sinput:
        p = subprocess.Popen(args, stdin=sinput, stdout=subprocess.PIPE)
    elif soutput:
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=soutput)
    else:
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    result = p.communicate()
    for robj in result:
        if robj:
            print(robj.decode(console_encoding))
    return None


def crf_learn(crf_learn_path = 'crftools/crf_learn',
              params         = None,
              templatepath   = './template/template01',
              trainpath      = 'demotraingold',
              modelname      = 'tmptest'):

    args = [crf_learn_path]
    if params:
        args += dict2list(params)
    args += [templatepath, trainpath, modelname]
    shell_invoke(args)


def crf_test(crf_test_path = 'crftools/crf_learn',
             modelpath     = None,
             testfilepath  = None,
             resultpath    = None):

    if (not modelpath) or (not testfilepath) or (not resultpath):
        return

    args = [crf_test_path, '-v', '2', '-m', modelpath, testfilepath]
    with open(resultpath, 'w') as fh_write:
        shell_invoke(args, soutput = fh_write)


