from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5

import base64
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.PublicKey import RSA

default_encoding = "utf-8"

__all__ = ['rc']


class RsaConfirm(object):
    """
    rc.test_Crypt(text=''): 测试RSA加密解密
    rc.testVertify():测试RSA私钥加密、公钥解密。数据生成签名，使用公钥验证签名，判断权限
    """
    def __init__(self, text='小博：这是一段明文'):
        print('构建')
        self.text = text
        from Crypto.PublicKey import RSA

        key = RSA.generate(2048)

        pri_key = key.export_key()
        with open("./pri_key.pem", "wb") as f:
            f.write(pri_key)

        pub_key = key.public_key().export_key()
        with open("./pub_key.pem", "wb") as f:
            f.write(pub_key)

    def get_key(self, key_or_path):
            if "BEGIN PUBLIC KEY" in key_or_path or "BEGIN PRIVATE KEY" in key_or_path:
                pem_data = key_or_path
            else:
                with open(key_or_path) as f:
                    pem_data = f.read()
            return RSA.importKey(pem_data)

    def rsa_encrypt(self, msg, pub_path, max_length=245):
            """
            RSA加密
            :param msg: 加密字符串
            :param pub_path: 公钥路径
            :param max_length: 1024bit的秘钥不能超过117， 2048bit的秘钥不能超过245
            :return:
            """
            key = self.get_key(pub_path)
            cipher = PKCS1_cipher.new(key)
            res_byte = bytes()
            for i in range(0, len(msg), max_length):
                res_byte += cipher.encrypt(msg[i:i + max_length].encode(default_encoding))
            return base64.b64encode(res_byte).decode(default_encoding)

    def rsa_decrypt(self, msg, pri_path, max_length=256):
            """
            RSA解密
            :param msg: 加密字符串
            :param pri_path: 私钥路径
            :param max_length: 1024bit的秘钥用128，2048bit的秘钥用256位
            :return:
            """
            key = self.get_key(pri_path)
            cipher = PKCS1_cipher.new(key)

            res_bytes = bytes()
            encrypt_data = base64.b64decode(msg)
            for i in range(0, len(encrypt_data), max_length):
                res_bytes += cipher.decrypt(encrypt_data[i:i + max_length], 0)
            return res_bytes.decode(default_encoding)

    def generate_sign(self, un_sign_data, pri_key):
            signer = Signature_pkcs1_v1_5.new(pri_key)
            digest = SHA256.new()
            digest.update(un_sign_data.encode("utf-8"))
            signed_data = signer.sign(digest)
            return base64.b64encode(signed_data).decode("utf-8 ")

    def verify_sign(self, un_sign_data, signature, pub_key):
            verifier = Signature_pkcs1_v1_5.new(pub_key)
            digest = SHA256.new()
            digest.update(un_sign_data.encode("utf-8"))
            return verifier.verify(digest, base64.b64decode(signature))

    def test_Crypt(self):
            original_msg = self.text
            encrypted_data = self.rsa_encrypt(original_msg, "./pub_key.pem")
            print("encrypt_data:", encrypted_data)
            decrypted_data = self.rsa_decrypt(encrypted_data, "./pri_key.pem")
            print("decrypt_data:", decrypted_data)

    def testVertify(self):
            data = "hello world" * 20
            signature = self.generate_sign(data, self.get_key("./pri_key.pem"))
            print("signature:", signature)
            is_ok = self.verify_sign(data, signature, self.get_key("./pub_key.pem"))
            print("is_ok:", is_ok)

    def print_key(self):
        print(RsaConfirm.publish_key)


rc = RsaConfirm()
rc.test_Crypt()
rc.testVertify()
