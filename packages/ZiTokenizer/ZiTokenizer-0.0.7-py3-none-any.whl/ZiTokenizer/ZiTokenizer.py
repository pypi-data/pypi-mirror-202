
import collections
import os
import random
import math

from logzero import logger

from .UnicodeTokenizer import UnicodeTokenizer
from .ZiCutter import ZiCutter 
from .glance import load_frequency, describe
from .ZiSegmenter import ZiSegmenter


class ZiTokenizer:
    def __init__(self, dir=None, do_lower_case=True, max_split=3, never_split=[]) -> None:
        self.do_lower_case = do_lower_case
        self.max_split = max_split
        self.dir = dir
        self.never_split = set(x for x in never_split)
        self.token2index = collections.OrderedDict()
        if dir:
            self.load(dir)

    def load(self,folder):
        vocab=[]
        root_words = []
        prefixs = []
        suffixs = []
        vocab_path = os.path.join(folder,"vocab.txt")
        assert os.path.exists(vocab_path)
        vocab = open(vocab_path).read().splitlines()
        for i, x in enumerate(vocab):
            # if i==3680:
            #     d=0
            # assert x.strip()                
            if len(x) > 1:
                if x[:2] == '--':
                    suffixs.append(x[2:])
                    continue
                if x[-2:] == '--':
                    prefixs.append(x[:-2])
                    continue
            root_words.append(x)
        logger.info(
            f" {vocab_path} load vocab:{len(vocab)} root:{len(root_words)} prefix:{len(prefixs)} suffix:{len(suffixs)} ")

        self.vocab = vocab
        for i, x in enumerate(vocab):
            self.token2index[x] = i

        root_words = set(root_words)
        never_split = self.never_split | root_words
        self.unicodeTokenizer = UnicodeTokenizer(do_lower_case=self.do_lower_case,never_split=never_split)
        self.ziCutter = ZiCutter(self.dir)
        self.ziSegmenter = ZiSegmenter(
            root_words=root_words, prefixs= prefixs, suffixs= suffixs, max_split=self.max_split)

    def token_word(self, word):
        [heads, root, tails] = self.ziSegmenter.token_word(word)
        if root:
            for i in range(len(heads)):
                heads[i] += '--'
            for i in range(len(tails)):
                tails[i] = '--' + tails[i]
            tokens = heads+[root]+tails
            return tokens
        token=self.ziCutter.cutWord(word)
        if token.startswith('##'):
            tokens = [token ]
        else:
            tokens=list(token)
        return tokens

    def build(self,word_freq_path,folder, min_ratio=1.5e-6, min_freq=3):
        assert os.path.exists(word_freq_path)
        logger.warning(f" building from {word_freq_path}")
        word_freq = load_frequency(
            word_freq_path, do_lower_case=self.do_lower_case)
        if not word_freq:
            logger.error(f"no word_freq")
            return
        total = describe(word_freq)
        bottom = max(min_freq, (total*min_ratio))
        bottom_char=max(min_freq, bottom/4)
        logger.info(
            f"min_ratio:{min_ratio} min_freq:{min_freq} bottom:{bottom:.2f} bottom_char:{bottom_char:.2f}")
        hot = [k for k, v in word_freq if v >= bottom]
        hot=set(hot)
        # hot=set()
        # for k,v in word_freq:
        #     if v/total/(len(hot)+1)>=min_ratio/2**15:
        #         hot.add(k)
        chars = [k for k, v in word_freq if v/len(k) >= bottom_char and k not in hot]
        # chars = [k for k, v in word_freq if len(k)==1 and v>= bottom_char and k not in hot]
        # chars=[]
        root_words = self.never_split | hot | set(chars)
        logger.info(
            f" words:{len(word_freq)} hot:{len(hot)} chars:{len(chars)} root_words:{len(root_words)}")
        ziCutter = ZiCutter(folder)
        ziCutter.build(folder,root_words)
        root_words |= set(ziCutter.vocab)
        # for x in root_words:
        #     assert x.strip()
        ziSegmenter = ZiSegmenter(root_words=root_words)

        logger.info("  === token_root ===  ")
        sample = random.choices(word_freq, k=5)
        for k, v in sample:
            [prefix, root, suffix] = ziSegmenter.token_root(k)
            row = [k, v, prefix, root, suffix]
            logger.info((row))

        prefix_counter = collections.Counter()
        suffix_counter = collections.Counter()
        # ignore rare words and decline bottom may save time
        for k, v in word_freq:
            if k in root_words:
                continue
            [prefix, root, suffix] = ziSegmenter.token_root(k)
            if not root:
                continue
            if prefix:
                prefix_counter[prefix] += v
            if suffix:
                suffix_counter[suffix] += v
        del word_freq
        prefixs = [k for k, v in prefix_counter.items() if v  >= bottom ]
        del prefix_counter
        # for x in prefixs:
        #     assert x.strip()
        suffixs = [k for k, v in suffix_counter.items() if v  >= bottom ]
        del suffix_counter
        # for x in suffixs:
        #     assert x.strip()
        logger.info(
            f"root_words:{len(root_words)} prefixs:{len(prefixs)} suffixs:{len(suffixs)}")

        prefixs = [x+'--' for x in prefixs]
        root_words = [x for x in root_words]
        suffixs = ['--'+x for x in suffixs]
        vocab = sorted(root_words)+sorted(prefixs)+sorted(suffixs)
        # for x in vocab:
        #     assert x.strip()        
        vocab_path = os.path.join(folder,"vocab.txt")
        with open(vocab_path, 'w') as f:
            for x in vocab:
                f.write(x+'\n')
        logger.info(f"save  vocab { len(vocab) }  -->{vocab_path} ")
        self.load(folder)

    def tokenize(self, line):
        words = self.unicodeTokenizer.tokenize(line)
        tokens = []
        for word in words:
            if not word:
                continue
            if word in self.token2index:
                tokens.append(word)
            else:
                cuts = self.token_word(word)
                tokens += cuts
        tokens = [x for x in tokens if x]
        return tokens

    def tokens2indexs(self, tokens):
        idxs = [self.token2index[x] for x in tokens]
        return idxs

    def indexs2tokens(self, indexs):
        indexs = [self.vocab[x] for x in indexs]
        return indexs

    def encode(self, line):
        tokens = self.tokenize(line)
        indexs = self.tokens2indexs(tokens)
        return indexs

    def tokens2words(self, tokens):
        ts = tokens[:1]
        for i in range(1, len(tokens)):
            x = tokens[i]
            if len(ts[-1]) > 1 and ts[-1][-2:] == '--':  # prefix
                ts[-1] = ts[-1][:-2]+x
                continue
            if len(x) > 1 and x[:2] == '--':  # suffix
                ts[-1] += x[1:]
                continue
            ts.append(x)
        return ts

    def decode(self, indexs):
        tokens = self.indexs2tokens(indexs)
        ts = self.tokens2words(tokens)
        words=self.ziCutter.combineWord(ts)
        return words
