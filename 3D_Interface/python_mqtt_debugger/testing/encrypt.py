from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

key = bytes([139, 190, 60, 202, 65, 17, 46, 241, 173, 243, 170, 221, 190, 150, 115, 6])

# encrypt data with AES
def aesEncrypt(data):    
    cipher = AES.new(key, AES.MODE_OFB)
    ct_bytes = cipher.encrypt(bytes(data))
    iv = cipher.iv
    ct = ct_bytes

    print("iv => ", list(bytearray(iv)))
    print("ct => ", list(bytearray(ct)))
    print("pt => ", list(bytearray(data)))
    
    
    return iv + ct

def aesEncryptString(data):
    return aesEncrypt(data.encode('utf-8'))