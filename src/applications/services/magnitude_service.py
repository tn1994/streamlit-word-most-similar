import os
import sys
import random
import logging
from functools import lru_cache

try:
    from pymagnitude import Magnitude, MagnitudeUtils
except BaseException:
    import collections

    collections.__setattr__('MutableMapping', collections.abc.MutableMapping)
    from pymagnitude import Magnitude, MagnitudeUtils

logger = logging.getLogger(__name__)


# @lru_cache(maxsize=2)
class MagnitudeService:
    """
    ref:
    https://zenn.dev/sorami/articles/fb2eb78e250568b767fd
    """
    random_positive_list: list = [
        '東京', 'フランス', '北京', '岡山', '愛媛',
        # 'Tokyo', 'France', 'America'
    ]

    random_negative_list: list = [
        'すごい', '悲しい', '面白い', '広い', '遠い',
        # 'cool', 'Amazing', 'OMG'
    ]

    most_similar_list: list = []

    model_name_list: list = [
        'chive-1.1-mc90-aunit.magnitude',
        'chive-1.2-mc90.magnitude',
    ]

    def __init__(self):
        # self.model = FastText.load_fasttext_format('model300.bin')
        self._setup_model()
        self.random_positive_idx: int = self._get_positive_idx()
        self.random_negative_idx: int = self._get_negative_idx()
        # self._check_word_list()

    def _setup_model(self):
        model_name: str = 'chive-1.2-mc90.magnitude'
        try:
            file_path: str = f'/root/.magnitude/{model_name}'
            if os.path.isfile(file_path):
                self.model = Magnitude(file_path)
                # self.model = Magnitude(filename, stream=True)
            else:
                self.model = Magnitude(
                    MagnitudeUtils.download_model(
                        model=model_name,
                        remote_path="https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/"))
            self.model_keyword_list = list(self.model)
        except Exception as e:
            logger.error(msg=e)

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
        return random.randint(0, len(self.random_negative_list) - 1)

    def _get_negative_idx(self):
        return random.randint(0, len(self.random_negative_list) - 1)

    def is_correct_answer(self, word: str) -> bool:
        if word not in self.random_negative_list:
            return False
        elif word == self.random_negative_list[self.random_negative_idx]:
            return True
        elif word != self.random_negative_list[self.random_negative_idx]:
            return False
        else:
            raise

    def query_most_similar(self, positive: str, negative: str):
        positive: list = positive.split()
        negative: list = negative.split()
        logger.info(f'{positive=}')
        logger.info(f'{negative=}')
        # return self.model.most_similar(positive=[positive],
        # negative=[negative])
        return self.model.most_similar(positive=positive, negative=negative)

    def get_word_using_vector(self, vectors: str):
        return [self.model[int(vector)] for vector in vectors.split()]
