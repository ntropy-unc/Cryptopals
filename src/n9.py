def padder(text, size=20):
    times = (size - len(text)) % size
    return text + bytes([times]) * times


print(padder(b"YELLOW SUBMARINE"))
print(padder(b"YELLOW SUBMARINE YELLOW SUBMARINE"))
