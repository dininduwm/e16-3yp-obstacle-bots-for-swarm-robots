from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

key = bytes([139, 190, 60, 202, 65, 17, 46, 241, 173, 243, 170, 221, 190, 150, 115, 6])

# encrypt data with AES OFB
def aesEncrypt(data):    
    cipher = AES.new(key, AES.MODE_OFB)
    ct_bytes = cipher.encrypt(bytes(data))
    iv = cipher.iv
    ct = ct_bytes    
    return iv + ct

def aesDecrypt(data):
    iv = data[0:16]
    ct = data[16:] 
    cipher = AES.new(key, AES.MODE_OFB, iv = iv)
    decrypted = cipher.decrypt(ct)
    return decrypted


def aesEncryptString(data):
    return aesEncrypt(data.encode('utf-8'))


