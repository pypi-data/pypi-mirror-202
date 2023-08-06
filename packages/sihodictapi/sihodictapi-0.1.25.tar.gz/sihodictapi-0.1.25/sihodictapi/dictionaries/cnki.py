import base64

from Crypto.Cipher import AES

from sihodictapi import utils


class EncryptDate:
    def __init__(self, key):
        self.key = key  # 初始化密钥
        self.length = AES.block_size  # 初始化数据块大小
        self.aes = AES.new(self.key, AES.MODE_ECB)  # 初始化AES,ECB模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def pad(self, text):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数
        res = self.aes.encrypt(self.pad(encrData).encode("utf8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        msg = self.aes.decrypt(res).decode("utf8")
        return self.unpad(msg)


class Cnki:
    key = '4e87183cfd3a45fe'.encode('utf8')
    encrypt_date = EncryptDate(key)

    @classmethod
    def translate(cls, text: str, translateType: int = None) -> dict:
        words = cls.encrypt_date.encrypt(text).replace('/', '_').replace('+', '-')
        print(words)
        return utils.request_post('https://dict.cnki.net/fyzs-front-api/translate/literaltranslation',
                                  json={
                                      'translateType': translateType,
                                      'words': words
                                  },
                                  headers={
                                      'Content-Type': 'application/json;charset=UTF-8',
                                      'Token': 'undefined',
                                  }).json()
