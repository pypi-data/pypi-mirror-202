 # -*- coding: utf-8 -*-
import os

from logzero import logger

from .UnicodeTokenizer import UnicodeTokenizer
from ZiTokenizer import He2Zi


# 2365
GouJian = "⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻⿼⿽⿾⿿〇〾㇀㇁㇂㇃㇄㇅㇆㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇑㇒㇓㇔㇕㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣㇤㇥㇦㇧㇨㇩㇪㇫㇬㇭㇮㇯㐄㐅㐫㐱㒳㒼㓁㔾㕯㠯㡀㢴㣇㦰㫃㲋㸦䇂䒑䶹一丁丂七丄丅丆万丈三上下丌与丏丑丘丙业丣严丨丩丬中丮丯丰丱丵丶丷丿乀乁乂乇乑乙乚乛九习乡亅二亍亏五井亜亞亠亥产亯人亻亼亾仌从來侖儿兀兂兆先克入八公六冂冃冄冈冉冋册冎冏冖冘冫几凵刀刂刃刄刅力勹匕北匚匸十卂千卄卅午卌南卜卝卤卩卯厂厃厄厶厷叀又叕叚口史吅咅咼啇喿嘼囗四囟囧囪囱土圥坴堇士壬壴夂夅夆夊夋夌夕夗大夨天夫夬女娄婁子宀寅寸尃小尚尞尢尣尸尺屮屰山屵巛巜川州巠巤工巨己巳巴巾巿帀干幵并幷幺广庚廌廴廾廿开弋弓彐彑彖彡彳心忄戈戉戊戌戍我戶户戼手扌支攴攵文斗斤方无旡日昜昷曰曷月木朩未本朮朱朿東枼桼欠止步歹歺殳毋毌母比毚毛氏氐民气水氵氶氺火灬爪爫爭父爻爾爿片牙牛牜犬犭犮玄玉王瓜瓦甘生用田甲申甶甾畀畐疋疌疒癶癸白皀皋皮皿盍目睘矛矢石示礻禸禺禾穴立竹米粦糸糹絲纟缶网罒罓羊羽翏老耂而耒耳聿肀肉肙臣自至臼臽與舌舛舟艮色艸艹菐萬虍虎虫血行衣衤襾西覀覃見见角言訁讠谷豆豕豸貝贝赤走足身車车辛辰辵辶邑酉釆采里金釒钅長镸长門门阜阝隶隹隺雚雨霝靑青非面靣革韋韦韭音頁页風风飛飞食飠饣首香馬马骨高髟鬥鬯鬲鬼魚鱼鳥鸟鹵鹿麥麦麻黃黄黍黑黹黽黾鼎鼓鼠鼻齊齐齒齿龍龙龜龠龰龴龵龶龷龸龹龻爫艹𠀁𠂊𠂤𠂭𠃑𠃬𠆢𠕁𠘨𠤎𠫓𡭔𡿨𣎳𣶒𤴓𤴔𦈢𦍌𦘒𦣝𦣞𦥑𧾷𨸏𩙿"

JieGou = '〾⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻'

def slim(v):
    if len(v) <= 3:
        return v
    for i in range(1,len(v)-1):
        if v[i] not in JieGou:
            w = v[0]+v[i]+v[-1]
            return w
    assert len(v) == 3
    return v


def valid(seq, Ji):
    for x in seq:
        if x not in Ji:
            return 0
    return 1


def loadHeZi(path, JiZi,shrink=False):
    doc = open(path).read().splitlines()
    doc = [x.split('\t') for x in doc]
    doc = [(k, slim(v)) if shrink else (k, v) for k, v in doc if valid(v, JiZi)]
    HeZi = {k: v for k, v in doc}
    slim2Zi={ v:k for k,v in HeZi.items() }
    values = ''.join(HeZi.values())
    values = list(set(values))
    values.sort()
    # for x in values:
    #     assert x.strip()
    logger.info(
        f"  {path} {len(doc)}  JiZi:{len(JiZi)} --> loadHeZi {len(HeZi)}  values:{len(values)} slim2Zi:{len(slim2Zi)}")
    return HeZi, values,slim2Zi


# Nums = ''.join(chr(i) for i in range(ord('0'), ord('9')+1))
# Az = ''.join(chr(i) for i in range(ord('a'), ord('z')+1))
# Alphabet = Nums+Az  # 36

class ZiCutter:
    def __init__(self, dir=None,do_lower_case=True, shrink=False,k=10):
        """
        """
        self.do_lower_case = do_lower_case
        self.shrink = shrink
        self.k = k
        self.vocab = set()
        self.HeZi = {}
        self.slim2Zi={}
        self.here = os.path.dirname(__file__)
        self.HanZiDir = os.path.join(self.here, "HanZi")
        self.UNKs = [f"##{x}" for x in range(k)]  # 100
        self.dir = dir
        if  dir:
            self.load(dir)
        # self.unicodeTokenizer = UnicodeTokenizer(do_lower_case=self.do_lower_case,never_split=self.vocab)

    def load(self, dir):
        HeZiPath = os.path.join(dir, "HeZi.txt")
        JiZiPath = os.path.join(dir, "JiZi.txt")
        if not os.path.exists(HeZiPath):
            HeZiPath = os.path.join( self.HanZiDir, "He2ZiGen.txt")
            JiZiPath = os.path.join( self.HanZiDir, "ZiGen.txt")

        JiZi = open(JiZiPath).read().splitlines()
        JiZi = set(JiZi)
        logger.info(f"{JiZiPath} load  JiZi:{len(JiZi)}")

        HeZi, values,slim2Zi = loadHeZi(HeZiPath, JiZi,self.shrink)
        self.slim2Zi = slim2Zi
        self.HeZi = HeZi
        self.vocab = self.UNKs+values
        logger.info(f"{dir} loaded vocab:{len(self.vocab)}")

    def build(self,folder, roots):
        logger.warning(f" {folder} building")
        vocab = set(self.UNKs) | set(GouJian) | set(x for x in roots)
        # vocab = set(self.UNKs) |  set(x for x in roots)
        JiZi = [x for x in vocab if len(x) == 1]
        logger.info(f"receive roots:{len(roots)} JiZi:{len(JiZi)}")

        ChaiZiPath=os.path.join(self.HanZiDir, "ChaiZi.txt")
        YiTiZiPath=os.path.join(self.HanZiDir, "YiTiZi.txt")
        HeZiPath = os.path.join(folder, "HeZi.txt")
        JiZiPath = os.path.join(folder, "JiZi.txt")
        He2Zi.build(JiZi, ChaiZiPath, YiTiZiPath,HeZiPath, JiZiPath)
        self.load(folder)

    def cutHanzi(self, zi)-> str:
        ids = self.HeZi.get(zi, zi)
        return ids

    def cutWord(self, word)-> str:
        if len(word)==1:
            token=self.cutHanzi(word)
            if word!=token:
                return token
        token=self.cutToken(word)
        return token

    def cutToken(self, token)-> str:
        point = sum(ord(x) for x in token)% 10
        return f"##{point}"

    def tokenize(self, line):
        words = self.unicodeTokenizer.tokenize(line)
        tokens = []
        for x in words:
            z=self.cutWord(x)
            tokens.append(z)
        return tokens

    def combineWord(self, tokens):
        if not self.shrink:
            return tokens
        words=[]
        j=0
        for i,x in enumerate(tokens):
            if i<j:
                continue
            if x[0] in JieGou:
                slim=''.join(tokens[i:i+3])
                if slim in self.slim2Zi:
                    x=self.slim2Zi[slim]
                j=min(i+3,len(tokens))
            words.append(x)
        return words

