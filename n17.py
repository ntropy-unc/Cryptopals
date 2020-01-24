from base64 import b64decode

with open('17.txt') as f:
    for l in f.readlines():
        print(b64decode(l.strip()))
