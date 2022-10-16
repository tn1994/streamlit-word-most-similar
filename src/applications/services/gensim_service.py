import random
import logging
from functools import lru_cache

import gensim
import gensim.downloader as api
from gensim.models import FastText
from gensim.models import word2vec

from gensim.test.utils import common_texts

logger = logging.getLogger(__name__)


@lru_cache(maxsize=10)
class GensimService:
    """
    ref:
    https://qiita.com/MuAuan/items/d46985223cad76764b9d
    https://huggingface.co/Gensim/glove-twitter-25
    """
    random_positive_list: list = [
        '東京', 'フランス', '北京'
        # 'Tokyo', 'France', 'America'
    ]

    random_negative_list: list = [
        'すごい', '悲しい', '面白い'
        # 'cool', 'Amazing', 'OMG'
    ]

    most_similar_list: list = []

    def __init__(self):
        # self.model = FastText.load_fasttext_format('model300.bin')
        self._setup_model()
        self.random_positive_idx: int = self._get_positive_idx()
        self.random_negative_idx: int = self._get_negative_idx()
        # self._check_word_list()

    def _check_word_list(self):
        try:
            # diff_list = set(self.random_positive_list) ^ set(self.model.wv.vocab)
            print(f'{self.model.wv.key_to_index=}')
            diff_set = set(self.random_positive_list) - \
                set(self.model.wv.key_to_index.keys())
            print(f'{diff_set=}')
            self.random_positive_list = list(
                set(self.random_positive_list) - diff_set)
            # diff_list = set(self.random_negative_list) ^ set(self.model.wv.vocab)
            # diff_set = set(self.random_negative_list) ^ set(self.model.wv.key_to_index)
            diff_set = set(self.random_negative_list) - \
                set(self.model.wv.key_to_index.keys())
            print(f'{diff_set=}')
            self.random_negative_list = list(
                set(self.random_negative_list) - diff_set)
        except Exception:
            diff_set = set(self.random_positive_list) - \
                set(self.model.key_to_index.keys())
            print(f'{diff_set=}')
            self.random_positive_list = list(
                set(self.random_positive_list) - diff_set)

            diff_set = set(self.random_negative_list) - \
                set(self.model.key_to_index.keys())
            print(f'{diff_set=}')
            self.random_negative_list = list(
                set(self.random_negative_list) - diff_set)

    def _setup_model(self):
        filename = ''
        # sentences = gensim.models.word2vec.Text8Corpus(filename)
        # self.model = word2vec.Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)

        # coupus = word2vec.Text8Corpus(filename)
        # self.model = word2vec.Word2Vec(coupus, size=200, window=5, min_count=5)
        # self.model = word2vec.Word2Vec(sentences=common_texts, vector_size=100, window=5, min_count=1, workers=4)

        try:
            file_name: str = '/root/gensim-data/glove-twitter-25/glove-twitter-25.gz'
            # self.model = gensim.models.KeyedVectors.load_word2vec_format(
            #     '/root/gensim-data/glove-twitter-25/glove-twitter-25.gz', binary=True)
            # self.model = gensim.models.Word2Vec.load(file_name)
            self.model = word2vec.KeyedVectors.load_word2vec_format(file_name)
            self.model_keyword_list = self.model.wv.key_to_index.keys()
        except Exception as e:
            logger.error(msg=e)
            self.model = gensim.downloader.load('glove-twitter-25')  # ok
            self.model_keyword_list = self.model.key_to_index.keys()

        # no
        # self.model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)

        # self.model = api.load("glove-twitter-25", from_hf=True)
        # self.model = api.load("glove-twitter-25")  # todo: use this
        # model.most_similar(positive=['fruit', 'flower'], topn=1)

    def main(self):
        try:
            self.most_similar_list: list = self.model.wv.most_similar(
                positive=[
                    self.random_positive_list[self.random_positive_idx]
                ],
                negative=[
                    self.random_negative_list[self.random_negative_idx]
                ])
        except Exception:
            self.most_similar_list: list = self.model.most_similar(
                positive=[
                    self.random_positive_list[self.random_positive_idx]
                ],
                negative=[
                    self.random_negative_list[self.random_negative_idx]
                ])

    def _get_positive_idx(self):
        return random.randint(0, len(self.random_negative_list))

    def _get_negative_idx(self):
        return random.randint(0, len(self.random_negative_list))

    def is_correct_answer(self, word: str) -> bool:
        if word not in self.random_negative_list:
            return False
        elif word == self.random_negative_list[self.random_negative_idx]:
            return True
        elif word != self.random_negative_list[self.random_negative_idx]:
            return False
        else:
            raise
