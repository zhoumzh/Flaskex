import re

T = 'type'
C = 'txt'
S = 1
P = -1


def do_format(txt):
    res = []
    get_pairs(res, {}, get_valid_lines(txt))
    return res


def get_valid_lines(txt):
    lines = txt.split('\n')
    p_sql = re.compile("==>( )+Preparing:(.*)")
    p_args = re.compile("==>( )+Parameters:(.*)")
    queue = []
    for line in lines:
        # 先分析sql
        ms = p_sql.search(line)
        # 再分析参数
        ma = p_args.search(line)
        if ms.group(1):
            queue.append({T: S, C: ms.group(1).strip()})
        elif ma.group(1):
            queue.append({T: P, C: ma.group(1).strip()})
        else:
            print(line, "-->不是有效的行,丢弃...")
            continue
    # 排除掉第一个是参数的情况
    if len(queue) > 0:
        if queue[0][T] == P:
            queue.pop(0)
        # 排除掉最后一个是sql的情况
        if queue[-1][T] == S:
            queue.pop()
    return queue


def get_pairs(res, pair, queue):
    if len(pair) == 0:
        pair[S] = queue.pop(front_sql_idx(queue))
    elif len(pair) == 1:
        pair[P] = queue.pop(front_params_idx(queue))
    else:
        res.append(pair)
        pair.clear()
    if not is_scrap(queue):
        get_pairs(res, pair, queue)


def is_scrap(queue):
    s = 0
    for q in queue:
        s += q[T]
    return abs(s) == len(queue)


def front_sql_idx(queue):
    for i in range(len(queue)):
        if queue[i][T] == S:
            return i


def front_params_idx(queue):
    for i in range(len(queue)):
        if queue[i][T] == P:
            return i


if __name__ == '__main__':
    pass
