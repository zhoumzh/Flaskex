import re

S = 1
P = -1
T = 'type'
C = 'txt'


def do_format(txt):
    res = get_valid_lines(txt)
    res = get_pairs(res)
    res_f = []
    for pair in res:
        res_f.append(format2sql(pair))
    return res_f


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
        if ms and ms.group(2):
            queue.append({T: S, C: ms.group(2).strip()})
        elif ma and ma.group(2):
            # 固定在参数后面加一位逗号,符合正则匹配
            queue.append({T: P, C: ma.group(2).strip() + ","})
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


def get_pairs(queue):
    res = []
    pair = {}
    olen = len(queue)
    for _ in range(olen):
        if len(pair) == 0:
            pair[S] = queue.pop(front_sql_idx(queue))
        elif len(pair) == 1:
            pair[P] = queue.pop(front_params_idx(queue))
        if len(pair) == 2:
            res.append(pair.copy())
            pair.clear()
    return res


def format2sql(pair):
    sql = pair[S][C]
    args = deal_args(pair[P][C])
    # 不考虑拼接字符串的sql中存在问号的情况,大概率?数就等于参数的数量
    idx = 0
    max = sql.count('?')
    while '?' in sql and idx <= max:
        sql = sql.replace('?', args[idx], 1)
        idx += 1
    return sql


quote_type = "String|TimeStamp|"
direct_type = "Integer|Byte|Double|Float"


def deal_args(src):
    p = re.compile("(\S+)\((" + quote_type + direct_type + ")\),( )?")
    args = []
    while p.search(src):
        m = p.search(src)
        if m:
            oa = m.group(1)
            if m.group(2) in quote_type:
                args.append("'" + oa + "'")
            else:
                args.append(oa)
            src = p.sub(repl="", string=src, count=1)
    return args


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
