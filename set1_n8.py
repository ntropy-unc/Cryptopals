with open('8.txt') as f:
    for line in f.readlines():
        line = line.strip()
        check_rep = set()

        for x in range(len(line) // 16):
            test = line[x * 16: (x + 1) * 16]
            if test in check_rep:
                print(line)
                break
            else:
                check_rep.add(test)
