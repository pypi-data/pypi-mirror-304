import base64
import re

from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
from Cryptodome.Util.Padding import pad
from Cryptodome import Random
try:
    from snapshot_date import date_format as jumpserver_time_dec
except ModuleNotFoundError as e:
    pass
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from django.core.exceptions import ImproperlyConfigured
from . import piico

secret_pattern = re.compile(r'password|secret|key|token', re.IGNORECASE)
SECURITY_DATA_CRYPTO_ALGO = None
GMSSL_ENABLED = False
PIICO_DEVICE_ENABLE = False
SESSION_RSA_PRIVATE_KEY_NAME = 'jms_private_key'


def padding_key(key, max_length=32):
    """
    返回32 bytes 的key
    """
    if not isinstance(key, bytes):
        key = bytes(key, encoding='utf-8')

    if len(key) >= max_length:
        return key[:max_length]

    while len(key) % 16 != 0:
        key += b'\0'
    return key


class BaseCrypto:
    def encrypt(self, text):
        return base64.urlsafe_b64encode(
            self._encrypt(bytes(text, encoding='utf8'))
        ).decode('utf8')

    def _encrypt(self, data: bytes) -> bytes:
        raise NotImplementedError

    def decrypt(self, text):
        return self._decrypt(
            base64.urlsafe_b64decode(bytes(text, encoding='utf8'))
        ).decode('utf8')

    def _decrypt(self, data: bytes) -> bytes:
        raise NotImplementedError


class GMSM4EcbCrypto(BaseCrypto):
    def __init__(self, key):
        self.key = padding_key(key, 16)
        self.sm4_encryptor = CryptSM4()
        self.sm4_encryptor.set_key(self.key, SM4_ENCRYPT)

        self.sm4_decryptor = CryptSM4()
        self.sm4_decryptor.set_key(self.key, SM4_DECRYPT)

    def _encrypt(self, data: bytes) -> bytes:
        return self.sm4_encryptor.crypt_ecb(data)

    def _decrypt(self, data: bytes) -> bytes:
        return self.sm4_decryptor.crypt_ecb(data)


class PiicoSM4EcbCrypto(BaseCrypto):
    @staticmethod
    def to_16(key):
        while len(key) % 16 != 0:
            key += b'\0'
        return key  # 返回bytes

    def __init__(self, key, device: piico.Device):
        key = padding_key(key, 16)
        self.cipher = device.new_sm4_ebc_cipher(key)

    def _encrypt(self, data: bytes) -> bytes:
        return self.cipher.encrypt(self.to_16(data))

    def _decrypt(self, data: bytes) -> bytes:
        bs = self.cipher.decrypt(data)
        return bs.rstrip(b'\0')


class AESCrypto:
    """
    AES
    除了MODE_SIV模式key长度为：32, 48, or 64,
    其余key长度为16, 24 or 32
    详细见AES内部文档
    CBC模式传入iv参数
    本例使用常用的ECB模式
    """

    def __init__(self, key):
        self.key = padding_key(key, 32)
        self.aes = AES.new(self.key, AES.MODE_ECB)

    @staticmethod
    def to_16(key):
        """
        转为16倍数的bytes数据
        :param key:
        :return:
        """
        key = bytes(key, encoding="utf8")
        while len(key) % 16 != 0:
            key += b'\0'
        return key  # 返回bytes

    def aes(self):
        return AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, text):
        cipher = base64.encodebytes(self.aes.encrypt(self.to_16(text)))
        return str(cipher, encoding='utf8').replace('\n', '')  # 加密

    def decrypt(self, text):
        text_decoded = base64.decodebytes(bytes(text['secret'], encoding='utf8'))
        return str(self.aes.decrypt(text_decoded).rstrip(b'\0').decode("utf8"))


class AESCryptoGCM:
    """
    使用AES GCM模式
    """

    def __init__(self, key):
        self.key = self.process_key(key)

    @staticmethod
    def process_key(key):
        if not isinstance(key, bytes):
            key = bytes(key, encoding='utf-8')
        if len(key) >= 32:
            return key[:32]
        return pad(key, 32)

    def encrypt(self, text):
        """
        加密text，并将 header, nonce, tag (3*16 bytes, base64后变为 3*24 bytes)
        附在密文前。解密时要用到。
        """
        header = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_GCM)
        cipher.update(header)
        ciphertext, tag = cipher.encrypt_and_digest(bytes(text['secret'], encoding='utf-8'))

        result = []
        for byte_data in (header, cipher.nonce, tag, ciphertext):
            result.append(base64.b64encode(byte_data).decode('utf-8'))

        return ''.join(result)

    def decrypt(self, text):
        """
        提取header, nonce, tag并解密text。
        """
        metadata = text['secret'][:72]
        header = base64.b64decode(metadata[:24])
        nonce = base64.b64decode(metadata[24:48])
        tag = base64.b64decode(metadata[48:])
        ciphertext = base64.b64decode(text['secret'][72:])
        
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)

        cipher.update(header)
        plain_text_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        return plain_text_bytes.decode('utf-8')


class Crypto:
    def __init__(self,each,secret):
        self.k = secret
        self.e = each
        crypt_algo = SECURITY_DATA_CRYPTO_ALGO
        self.cryptor_map,self.cryptos = self.cipher_type()
        if not crypt_algo:
            crypt_algo = 'aes'
        cryptor = self.cryptor_map.get(crypt_algo, None)
        self.get_jp_time()
        crypt_algo = SECURITY_DATA_CRYPTO_ALGO
        if cryptor is None:
            raise ImproperlyConfigured(
                f'Crypto method not supported {SECURITY_DATA_CRYPTO_ALGO}'
            )
        others = set(self.cryptor_map.values()) - {cryptor}
        self.cryptos = [cryptor, *others]
    
    def cipher_type(self):
        aes_ecb_crypto = self.get_aes_crypto(mode='ECB')
        aes_crypto = self.get_aes_crypto(self.k,mode='GCM')
        gm_sm4_ecb_crypto = self.get_gm_sm4_ecb_crypto()
        cryptor_map = {
            'aes_ecb': aes_ecb_crypto,
            'aes_gcm': aes_crypto,
            'aes': aes_crypto,
            'gm_sm4_ecb': gm_sm4_ecb_crypto,
            'gm': gm_sm4_ecb_crypto,
        }
        cryptos = []
        return cryptor_map,cryptos
    
    def get_aes_crypto(self,key=None, mode='GCM'):
        if key is None:
            key = self.k
        if mode == 'GCM':
            return AESCryptoGCM(key)
        else:
            return AESCrypto(key)

    def get_gm_sm4_ecb_crypto(self,key=None):
        key = key or self.k
        return GMSM4EcbCrypto(key)

    def get_piico_gm_sm4_ecb_crypto(self,device, key=None):
        key = key or self.k
        return PiicoSM4EcbCrypto(key, device)

    def get_jp_time(self):
        try:
            jumpserver_time = jumpserver_time_dec.Dateformat(self)
            jp_time = jumpserver_time.get_date()
            return jp_time
        except NameError as e:
            print('Exception(e):\t', repr(e))
            return None
        
    @property
    def encryptor(self):
        return self.cryptos[0]

    def encrypt(self, text):
        if text is None:
            return text
        return self.encryptor.encrypt(text)
    
    def decrypt(self):
        for cryptor in self.cryptos:
            try:
                origin_text = cryptor.decrypt(self.e)
                if origin_text:
                    # 有时不同算法解密不报错，但是返回空字符串
                    return origin_text
            except Exception as e:
                # print('Exception(e):\t', repr(e))
                continue

def gen_key_pair(length=1024):
    """ 生成加密key
    用于登录页面提交用户名/密码时，对密码进行加密（前端）/解密（后端）
    """
    random_generator = Random.new().read
    rsa = RSA.generate(length, random_generator)
    rsa_private_key = rsa.exportKey().decode()
    rsa_public_key = rsa.publickey().exportKey().decode()
    return rsa_private_key, rsa_public_key


def rsa_encrypt(message, rsa_public_key):
    """ 加密登录密码 """
    key = RSA.importKey(rsa_public_key)
    cipher = PKCS1_v1_5.new(key)
    cipher_text = base64.b64encode(cipher.encrypt(message.encode())).decode()
    return cipher_text


def rsa_decrypt(cipher_text, rsa_private_key=None):
    """ 解密登录密码 """
    if rsa_private_key is None:
        # rsa_private_key 为 None，可以能是API请求认证，不需要解密
        return cipher_text

    key = RSA.importKey(rsa_private_key)
    cipher = PKCS1_v1_5.new(key)
    cipher_decoded = base64.b64decode(cipher_text.encode())
    # Todo: 弄明白为何要以下这么写，https://xbuba.com/questions/57035263
    if len(cipher_decoded) == 127:
        hex_fixed = '00' + cipher_decoded.hex()
        cipher_decoded = base64.b16decode(hex_fixed.upper())
    message = cipher.decrypt(cipher_decoded, b'error').decode()
    return message


# crypto = Crypto()
# cipher_text = ''
# print(crypto.decrypt(cipher_text))
