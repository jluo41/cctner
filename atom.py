import string
import re

from radical import Radical



# Tags for the basic information


def basicTags(word):
    punStr = string.punctuation + '＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'
    engReg = r'[A-Za-z]{1}'
    if '%' in word or '%' in word:
        return 'PERC'
    elif re.match(r'[0-9]{1}', word):
        return "NUM"
    elif word in punStr:
        return "PUNC"
    elif word >= '\u4e00' and word <= '\u9fff':
        return "CHN"
    elif re.match(engReg, word):
        return 'ENG'
    #elif word in string.whitespace:
        #return 'SPA'
    elif word == '@':
        return 'SPA'
    else:
        return 'OTHER'


def matrixPreparing(matrix):
    matrix.sort(key = lambda x:len(x))
    return matrix[::-1]

# Medical Dictionary Tag
def dictTags(word):
    units = 'kBq kbq mg Mg UG Ug ug MG ml ML Ml GM iu IU u U g G l L cm CM mm s S T % % mol mml mmol MMOL HP hp mmHg umol ng'.split(
        ' ')
    chn_units = '毫升 毫克 单位 升 克 第 粒 颗粒 支 件 散 丸 瓶 袋 板 盒 合 包 贴 张 泡 国际单位 万 特充 个 分 次'.split(' ')
    med_units = 'qd bid tid qid qh q2h q4h q6h qn qod biw hs am pm St DC prn sos ac pc gtt IM IV po iH'.split(' ')
    all_units = units + chn_units + med_units

    site_units = '上 下 左 右 间 片 部 内 外 前 侧 后'.split(' ')
    sym_units = '大 小 增 减 多 少 升 降 高 低 宽 厚 粗 两 双 延 长 短 疼 痛 终 炎 咳'.split(' ')
    part_units = '脑 心 肝 脾 肺 肾 胸 脏 口 腹 胆 眼 耳 鼻 颈 手 足 脚 指 壁 膜 管 窦 室 管 髋 头 骨 膝 肘 肢 腰 背 脊 腿 茎 囊 精 唇 咽'.split(' ')
    break_units = '呈 示 见 伴 的 因'.split(' ')
    more_units = '较 稍 约 频 偶 偏'.split(' ')
    non_units = '无 不 非 未 否'.split(' ')
    tr_units = '服 予 行'.split(' ')

    all_units = matrixPreparing(all_units)
    units = matrixPreparing(units)
    chn_units = matrixPreparing(chn_units)
    med_units = matrixPreparing(med_units)

    if word in units:
        return 'UNIT'
    elif word in chn_units:
        return 'CHN_UNIT'
    elif word in med_units:
        return 'MED_UNIT'
    elif word in site_units:
        return 'SITE_UNIT'
    elif word in sym_units:
        return 'SYM_UNIT'
    elif word in part_units:
        return 'PART_UNIT'
    elif word in break_units:
        return 'BREAK_UNIT'
    elif word in more_units:
        return 'more_UNIT'
    elif word in non_units:
        return 'NON_UNIT'
    elif word in tr_units:
        return 'TR_UNIT'
    else:
        return 'OTHER'


def radicalTags(atom):
    if atom  >= '\u4e00' and atom <= '\u9fff':
        radical = Radical()
        rad = radical.get_radical(atom)
        return rad
    else:
        return '-'

# radicalTags('譝')

class Atom(object):
    
    # the index in the sentence
    index = None
    
    def __init__(self, atom):
        self._atom = atom
        self.basicTag = basicTags(self._atom)
        self.dictTag = dictTags(self._atom)
        self.radical = radicalTags(self._atom)
    
    def to_dict(self):
        return self.__dict__
    
    def get_attr(self, name):
        return self.__getattribute__(name)
    
    def set_attr(self, name, value):
        self.__setattr__(name, value)
    
    def __repr__(self):
        return "\t".join([self._atom, self.basicTag, self.dictTag, self.radical])




