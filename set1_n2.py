from binascii import unhexlify, hexlify

inp = b"1c0111001f010100061a024b53535009181c"
key = b"686974207468652062756c6c277320657965"

inp = unhexlify(inp)
print(inp) # After hex decoding

key = unhexlify(key)

inp = ''.join([chr(x ^ y) for x, y in zip(inp, key)])
print(inp)

inp = hexlify(bytes(inp.encode()))
print(inp)
