from os import urandom
from Crypto.Cipher import AES
from n11 import *

def params_dict(s):
    ans = dict()
    for e in s.split('&'):
        k, v = e.split('=')
        ans[k] = v
    return ans

def dict_params(d):
    return b'&'.join(['{}={}'.format(k, v).encode() for k, v in d.items()])

def profile_for(email):
    email = email.replace('&', '').replace('=', '')
    obj = {
        'email': email,
        'uid': 10,
        'role': 'user'
    }
    return dict_params(obj)

def ECB_Decrypt(data, key):
    data = pad(data)
    return AES.new(key, AES.MODE_ECB).decrypt(data)

def CBC_Decrypt(data, key, iv=b"\x00" * 16):
    data = pad(data)
    plain = b''
    for i in range(len(data) // 16):
        block = data[i * 16:(i + 1) * 16]
        inp = ECB_Decrypt(block, key)
        plain += b''.join([bytes([x ^ y]) for x, y in zip(inp, iv)])
        iv = block
    return plain

def profile_admin(attacker, key):
    block_len = len(oracle('', key))
    for i in range(1, 100):
        test = len(oracle('A' * i, key))
        if test != block_len:
            block_len = i - 1
            break
    # block_len = 9
    fake = "hiya@goog.admin" + "\x00" * 11
    enc_admin = oracle(fake, key)[16:32]
    print(ECB_Decrypt(enc_admin, key))
    pad = "a" * 9 + "@c.e" # We could brute force. However, assuming we know format of str, 19 + x % 16 = 0
    ans = oracle(pad, key)
    ans = ans[:len(ans) - 16] + enc_admin
    return ans

def oracle(email, key):
    return ECB_Encrypt(profile_for(email), key)

def unoracle(data, key):
    return params_dict(ECB_Decrypt(data, key).decode())

if __name__ == '__main__':
    # print(params_dict("foo=bar&baz=qux&zap=zazzle"))
    key = urandom(16)
    email = "foo@bar.com"
    attacker = oracle(email, key)
    modified = profile_admin(attacker, key)
    print(unoracle(modified, key))
