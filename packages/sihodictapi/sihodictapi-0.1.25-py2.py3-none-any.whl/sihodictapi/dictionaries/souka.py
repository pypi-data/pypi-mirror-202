from sihodictapi import utils


class Souka:
    """souka日语学习社区"""

    @classmethod
    def vocab_search(cls, word: str) -> list:
        """
        搜索单词
        :param word: 输入
        :return: 结果列表
        """
        return utils.request_get('https://soukaapp.com/vocab/entry/', params={
            'word': word
        }, headers={
            "accept": "application/json",
        }).json()
