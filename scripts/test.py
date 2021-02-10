from scripts.functions import formate_mybatis as fm

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
    lst = fm.deal_args(
        "LW433B10LW40(Integer), 33B103M1004197(String), 3M1004197(String), 0(Integer), 44(Integer)")
    print(lst)
