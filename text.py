from pandas import read_csv
from pandas import DataFrame as df
from jieba import posseg as ppseg
import string

from atom import Atom

# this dictionary is used to deal with the annotated entities in texts.
fLabel = {'症状和体征': 'Sy',
          '身体部位':   'Bo',
          '检查和检验': 'Ch',
          '治疗':      'Tr',
          '疾病和诊断': 'Si'}


def strQ2B(ustring):
    rstring = ''
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):
            inside_code -= 65248
        # 2: unichr; 3: chr
        rstring += chr(inside_code)
    return rstring


def cleanSpace(text):
    #return text.replace("\t"," ").replace(" ","&nbsp;").replace('\n', '')
    '''
    return text.strip()
    '''
    for i in ' \t\r\x0b\x0c':
        text = text.replace(i, '@')
    text = text.strip()
    text =  text.replace('\n', '@')
    return text 
    

def segmentStr(text):
    strLen = len(text)
    atoms = []
    for i in range(strLen):
        atoms.append(text[i])
    return atoms


def getPOSTagsList(text):
    segs = list(ppseg.cut(text))
    
    for i in range(len(segs)):
        pair = segs[i]
        start = sum(len(p.word) for p in segs[:i])
        end = sum(len(p.word) for p in segs[:i+1]) -1
        pair.indeces = [start, end]
        
    POSTagsList = []
    for p in segs:
        word = p.word
        for i in range(len(p.word)):
            if i == 0:
                POSTagsList.append([p.indeces[0] + i, word[i], p.flag+'-B'])
            else:
                POSTagsList.append([p.indeces[0] + i, word[i], p.flag+'-I'])
                
    return POSTagsList

def getRTag(data):
    if type(data) == str:
        return data.split('/')[0]
    else:
        return None


class ChineseClinicalText(object):
    atoms = []
    POSTags = None
    outputCols =['_atom', 'basicTag']
    newTags = []
    entities = []
    learnedEntities = []
    annotedEntities = []
    learnedREntities = []
    annotedREntities = []
    annotedFilePath = None
    score = None
    
    def __init__(self, text = None, originalFilePath = None, annotedFilePath = None):
        # to do: parse the text for this Chinise Clincal Text
        if text != None:
            self._text = cleanSpace(strQ2B(text))
            
            self.atomsBaseList = segmentStr(self._text)
            self.newTags = []
            self.dfFormat = []
            self.score = None
            learnedREntities = []
            annotedREntities = []
        else:
            if originalFilePath != None:
                with open(originalFilePath, 'r') as f:
                    text = f.read() 
                self._text = cleanSpace(strQ2B(text))

                self.atomsBaseList = segmentStr(self._text)
                self.originalFilePath = originalFilePath
                self.newTags = []
                self.dfFormat = []
                self.score = None
                learnedREntities = []
                annotedREntities = []
                if annotedFilePath != None:
                    self.annotedFilePath = annotedFilePath
            else:
                print('Need a Text!!!')

    def setAtomTags(self):
        self.atoms = []
        for i in range(len(self.atomsBaseList)):
            a = Atom(self.atomsBaseList[i])
            a.index = i
            self.atoms.append(a)
            
    def getPOSTags(self):
        # for Element is POSTags
        # [index, char, POS-Tag]
        # [8, '民', 'n-I']
        self.POSTags = getPOSTagsList(self._text)
          
    def setPOSTags(self):
        for a in self.atoms:
            a.POSTag = 'o'
            for pos in self.POSTags:
                if a.index == pos[0] and a._atom == pos[1]:
                    a.POSTag = pos[-1]
                    #print(a, '\t', a.POSTag)
        
    def updateDF(self):
        'update the attribute for pandas PF form sentence'
        DF = df([i.to_dict() for i in self.atoms])
        # TODO, may not contain POS Tag
        # OK, actually, it can. hh
        self.dfFormat = DF[['_atom', 'basicTag', 'dictTag', 'radical', 'POSTag'] + self.newTags]
        
    def toTextFile(self, filePath, cols = None):
        if cols != None:
            self.outputCols = cols
        self.dfFormat.to_csv(filePath, columns = self.outputCols,
                             sep = '\t', encoding = 'utf=8', 
                             header = False, index = False )
        
    # For Test Data, need Copor Result Data
    def coporResult(self, result, newTag):
        # The requirements on result
        # it is a dataframe
        # exactly the same as the CCT
        # include the right and same index of CCT's atoms
        result.columns = self.outputCols + ['Result'] + list(range((len(result.columns)-len(self.outputCols) -1)))
        result[newTag] = result['Result'].apply(getRTag)
        result = result[self.outputCols + [newTag]]
        for idx, row in result.iterrows():
            for a in self.atoms:
                if a.index == idx and a._atom == row['_atom']:
                    a.set_attr(newTag, row[newTag])
        self.newTags.append(newTag)
        self.updateDF()
        
    # For Train Data, need Copor Annotated Data
    def coporAnnotation(self, newTag):
        entityTagsList = []
        if newTag == 'RTag':
            for ae in self.annotedREntities:
                word = ae[0]
                for i in range(len(word)):
                    if i == 0:
                        entityTagsList.append([ae[1]+i, word[i], ae[-1] +'-B'])
                    else:
                        entityTagsList.append([ae[1]+i, word[i], ae[-1] +'-I'])
                        
        elif newTag == 'ETag':
            for ae in self.annotedEntities:
                word = ae[0]
                for i in range(len(word)):
                    if i == 0:
                        entityTagsList.append([ae[1]+i, word[i], ae[-1] +'-B'])
                    else:
                        entityTagsList.append([ae[1]+i, word[i], ae[-1] +'-I'])
                        
        for a in self.atoms:
            a.set_attr(newTag, 'O')
            for eTag in entityTagsList:
                if a.index == eTag[0] and a._atom == eTag[1]:
                    a.set_attr(newTag, eTag[-1])
    
        self.newTags.append(newTag)
        self.updateDF()
         
    #### NEW
    #### HERE
    def getLearnedEntities(self, eType):
        '''
        eType = 'RTag' or 'ETag
        Atoms have 'RTag' or 'ETag'
        '''
        taggedAtoms = [a for a in self.atoms if a.get_attr(eType) != 'O']
        startIdx = [idx for idx in range(len(taggedAtoms)) if taggedAtoms[idx].get_attr(eType)[-2:] == '-B']
        startIdx.append(len(taggedAtoms))
        entitiesList = []
        for i in range(len(startIdx)-1):
            entityAtom = taggedAtoms[startIdx[i]: startIdx[i+1]]
            startA, endA = entityAtom[0], entityAtom[-1]
            entitiesList.append([''.join(ea._atom for ea in entityAtom), startA.index, endA.index, startA.get_attr(eType).split('-')[0]])
        entitiesList = [tuple(i) for i in entitiesList]
        if eType == 'RTag':
            self.learnedREntities = entitiesList
        if eType == 'ETag':
            self.learnedEntities  = entitiesList
        return entitiesList

    def getAnnotedEntities(self, eType, annotedFilePath = None):
        '''
        eType = 'RTag' or 'ETag'
        '''
        if annotedFilePath == None:
            annotedFilePath = self.annotedFilePath
        annotedEntities = []
        with open(annotedFilePath, 'r') as f:
            for l in f.readlines():
                entity = strQ2B(l).replace('\n','').split('\t')
                entity[0] = cleanSpace(entity[0])
                entity[-1] = fLabel[entity[-1]]
                entity[1], entity[2] = int(entity[1]), int(entity[2])
                annotedEntities.append(entity)

        #New here, Add This to check the text is consistent or not
        
        for ae in annotedEntities:
            if self._text[ae[1]:ae[2]+1] != ae[0]:
                print('Not Macthed:', self.originalFilePath)
                break
        
        #New here--END

        if eType == 'RTag':
            for ae in annotedEntities:
                ae[-1] = 'R'
            self.annotedREntities = [tuple(i) for i in annotedEntities]
        elif eType == 'ETag':
            self.annotedEntities  = [tuple(i) for i in annotedEntities]

        return annotedEntities
    
    def data(self):
        s = {}
        # Num of Atoms
        s['Atoms'] = len(self.atoms)
        s['learned_E'] = len(self.learnedEntities)
        s['annoted_E'] = len(self.annotedEntities)
        s['matched_E'] = len(set(self.learnedEntities).intersection(set(self.annotedEntities)))## Union vs Join
        s['learned_R'] = len(self.learnedREntities)
        s['annoted_R'] = len(self.annotedREntities)
        s['matched_R'] = len(set(self.learnedREntities).intersection(set(self.annotedREntities)))## Union vs Join
        entitiesLable = ['Sy','Bo', 'Ch', 'Tr', 'Si']
        for eL in entitiesLable:
            elL = [e for e in self.learnedEntities if eL == e[-1]]
            elA = [e for e in self.annotedEntities if eL == e[-1]]
            elM = set(elA).intersection(set(elL)) ## Union vs Join
            s[eL+'_learned'] = len(elL)
            s[eL+'_annoted'] = len(elA)
            s[eL+'_matched'] = len(elM)
        
        return s
    
    def execute(self):
        self.setAtomTags()   # set atoms' tags
        self.getPOSTags()    # generate atoms' POS tags. (only valid in text)
        self.setPOSTags()    # set atoms' POS tags
        self.updateDF()      # update atoms' attributes to DF format



