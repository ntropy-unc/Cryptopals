from base64 import b64encode
from binascii import unhexlify

inp = b"49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
res = unhexlify(inp) # Turn input from hex bytes to string. If inp is just bytes, to turn it into a str, use decode.
print(res)
res = b64encode(res)
print(res)
