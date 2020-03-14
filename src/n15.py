def pad_validator(msg):
    assert len(msg) % 16 == 0
    padding = msg[-1]
    for x in range(len(msg) - 1, len(msg) - 1 - padding, -1):
        assert msg[x] == padding
    return msg[:len(msg) - padding] # What if "ICE ICE BABY\x04\x03\x02\x01"?

if __name__ == '__main__':
    try:
        print(pad_validator(b"ICE ICE BABY\x05\x05\x05\x05"))
    except:
        print("Bad caught 1")
    try:
        print(pad_validator(b"ICE ICE BABY\x01\x02\x03\x04"))
    except:
        print("Bad caught 2")
    print(pad_validator(b"ICE ICE BABY\x04\x04\x04\x04"))
