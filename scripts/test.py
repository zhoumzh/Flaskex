p = [0, 2, 1, 3, 6, 8, 5]


def test_modify():
    for i in range(len(p)):
        print(i, "len=", len(p))
        p.pop(i)
        print(p)


def test_find(queue, target):
    for i in range(len(queue)):
        if target == queue[i]:
            return i


if __name__ == '__main__':
    print(test_find(p, 9))
