from hashlib import sha256
from base64 import b64encode
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BS = 16
pad = lambda s: bytes(s + (BS - len(s) % BS) * chr(BS - len(s) % BS), 'utf-8')
unpad = lambda s : s[0:-ord(s[-1:])]

class AESCipher:

    def __init__( self, key ):
        self.key = bytes(key, 'utf-8')
        self.nonce = get_random_bytes(15);

    def encrypt( self, message):
        cipher = AES.new(self.key, AES.MODE_OCB, nonce=self.nonce)
        ciphertext, self.mac = cipher.encrypt_and_digest(message)
        return ciphertext

    def decrypt( self, ciphertext ):
        cipher = AES.new(self.key, AES.MODE_OCB, nonce=self.nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, self.mac)
        return plaintext

# message = b"\n\t\x10\x17\x18\x05%\xe4\xae\x88B\n\x0b\x08\x01\x10\x06\x18\x05%\x87\x17\xabB\n\x0b\x08\x02\x10\x16\x18\x18%\x9b'\x86B\n\x0b\x08\x03\x10\x0c\x18\x11%\xbe\x1a[C\n\x0b\x08\x04\x10\x15\x18\x17%\x00\xeb/B\n\x0b\x08\x05\x10\r\x18\x06%\xe4\xeb\xa0C\n\x0b\x08\x06\x10\x0e\x18\x07%\xfa\xe2\xd0B\n\x0b\x08\x07\x10\x0b\x18\x11%\xf0\x98\xa6C\n\x0b\x08\x08\x10\x19\x18\x12%\xf7\xa61C\n\x0b\x08\t\x10\n\x18\x12%\xcb\xa6\x8dC\n\x0b\x08\n\x10\x13\x18\t%\x8f1jC\n\x0b\x08\x0b\x10\x05\x18\x10%\xe6:\x81C\n\x0b\x08\x0c\x10\x14\x18\x14%5\x1d\x82C\n\x0b\x08\r\x10\x05\x18\x17%\xd3\xc8\xadC\n\x0b\x08\x0e\x10\x18\x18\x15%q\x93\xe9B\n\x0b\x08\x0f\x10\x0e\x18\x05%\xdbT\xdeB\n\x0b\x08\x10\x10\x07\x18\x08%\x14\x1b1B\n\x0b\x08\x11\x10\x14\x18\x07%E|\x81C\n\x0b\x08\x12\x10\x17\x18\x06%\x16\xec\xdaB\n\x0b\x08\x13\x10\x19\x18\x12%\xbd\x818C"
# cipher = AESCipher('mysecretpassword')
# encrypted = cipher.encrypt(message)
# decrypted = cipher.decrypt(encrypted) 

# print(encrypted)
# print(decrypted)

# print(message == decrypted)