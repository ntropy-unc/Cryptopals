import base64
from Crypto.Cipher import AES

ciphertext = base64.b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
cipher = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB)
nonce, counter = bytearray(b'\x00' * 8), bytearray(b'\x00' * 8)
plain = b''

for level in range(len(ciphertext) // 16):
    next = cipher.encrypt(bytes(nonce + counter))
    block = bytes(ciphertext[level * 16: (level + 1) * 16])
    plain += b''.join([(x ^ y).to_bytes(1, 'little') for x, y in zip(block, next)])
    counter[0] += 1

print(f'Plaintext: {plain}')

