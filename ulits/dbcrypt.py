# coding=utf-8
from cryptography.fernet import Fernet


# 对数据库密码进行加密，和加密
#  key = base64.urlsafe_b64encode(os.urandom(32))  生成key

class prpcrypt():
    def __init__(self):
        self.key = 'P30cMRRBa9kF3YNYpeKNmlUquLsX6ssOuBdy4yZe8wU='

    def encrypt(self, password):
        f = Fernet(self.key)
        passwd_encode = password.encode()
        token = f.encrypt(passwd_encode)
        return token.decode()

    def decrypt(self, password):
        f = Fernet(self.key)
        passwd_encode = password.encode()
        token = f.decrypt(passwd_encode)
        return token.decode()
