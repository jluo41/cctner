import os

batch_CCKS = dict(name = 'ccks',
                  dataInput = dict(rootPath = '', 
                                   fpath = 'dataset/ccks/',
                                   filenames= ['一般项目', '病史特点', '诊疗经过', '出院情况'],
                                   orig_iden = '.txtoriginal.txt',
                                   anno_iden = '.txt'),
                                   dataAnno = dict(sep = '\t',
                                                   fLabel = {'症状和体征': 'Sy',
                                                             '身体部位': 'Bo',
                                                             '检查和检验': 'Ch',
                                                             '治疗': 'Tr', 
                                                             '疾病和诊断': 'Si'},
                                                   start = 0))


batch_LUOHU = dict(name = 'luohu',
                   dataInput = dict(rootPath = '',
                                    fpath = 'dataset/luohu/',
                                    filenames= ['text'],
                                    orig_iden = '.txt',
                                    anno_iden = '_StandardFormat.txt'),
                                    dataAnno = dict(sep = '\t',
                                                    fLabel = {'症状': 'Sy', 
                                                              '身体部位以及器官': 'Bo',
                                                              '检查项目': 'Ch',
                                                              '治疗手段': 'Tr', 
                                                              '疾病名称': 'Si',
                                                              '疾病类型': 'DT',
                                                              '不确定'  : 'unct' },
                                                     start = 1))
# TODO
batch_LH_M = dict(name = 'luohuM',
                  dataInput = dict(rootPath = '',
                                   fpath = 'dataset/luohuM/',
                                   filenames= ['Entity-lx', 'Entity-zmc', 'Entity-hsy', 'Entity-lyh', 'Entity-xdl'],
                                   orig_iden = '.txt',
                                   anno_iden = '_LabeledEntity.txt'),
                                   dataAnno = dict(sep = '\t',
                                                   fLabel =  {'症状': 'Sy', 
                                                              '检查': 'Ch',
                                                              '疾病': 'Di',
                                                              '治疗': 'Tr', 
                                                              '修饰': 'Dec',
                                                              '疾病诊断分类': 'DT',
                                                              '不确定'  : 'unct' },
                                                   start = 1))

# TODO
batch_LH_A = dict(name = 'luohuA',
                  dataInput = dict(rootPath = '',
                                   fpath = 'dataset/luohuA/',
                                   filenames= ['Anatomy-lx', 'Anatomy-zmc', 'Anatomy-hsy', 'Anatomy-lyh'],
                                   orig_iden = '.txt',
                                   anno_iden = '_LabeledAnatomy.txt'),
                                   dataAnno = dict(sep = '\t',
                                                   fLabel =  {'主体': 'A'},
                                                   start = 1))




def generateOriAn(fpath, filenames, orig_iden, anno_iden, rootPath):
    OriAn = dict()
    for filename in filenames:
        path = rootPath+fpath+filename
        L =  [i for i in os.listdir(path) if orig_iden in i or anno_iden in i]
        Orig = [i for i in L if orig_iden in i]
        Anno = [i for i in L if anno_iden in i]
        if len(Orig) == len(L)/2:
            Anno = [i for i in L if i not in Orig]
        elif len(Anno) == len(L)/2:
            Orig = [i for i in L if i not in Anno]
        else:
            print('Wrong !!!')

        assert len(Orig) == len(Anno)   
        
        d_orig = {}
        for i in Orig:
            d_orig[i.replace(orig_iden, '')] = i
            
        d_anno = {}
        for i in Anno:
            d_anno[i.replace(anno_iden, '')] = i
        assert d_anno.keys() == d_orig.keys()
        
        OriAn_L = []
        for k in d_anno:
            OriAn_L.append({'originalFilePath':path +'/'+ d_orig[k], 
                            'annotedFilePath' :path +'/'+ d_anno[k]})
        OriAn[filename] =  OriAn_L
    return OriAn