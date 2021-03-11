import re
import uuid

S = 1
P = -1


def do_format(txt):
    res_f = []
    queue_sql, queue_args = get_valid_lines(txt)
    sql_count = len(queue_sql)
    if sql_count <= 0:
        return res_f
    for i in range(sql_count):
        if not queue_args[i]:
            break
        res_f.append(format2sql({S: queue_sql[i], P: queue_args[i]}))
    return res_f


def get_valid_lines(txt):
    lines = txt.split('\n')
    p_sql = re.compile("==>.*Preparing:(.*)")
    p_args = re.compile("==>.*Parameters:(.*)")
    # 声明两个队列
    queue_sql, queue_args = [], []
    for line in lines:
        # 先分析sql
        ms = p_sql.search(line)
        # 再分析参数
        ma = p_args.search(line)
        if ms and ms.group(1):
            queue_sql.append(ms.group(1).strip())
        elif ma and ma.group(1):
            queue_args.append(ma.group(1).strip())
        else:
            print(line, "-->不是有效的行,丢弃...")
            continue
    return queue_sql, queue_args


def format2sql(pair):
    sql = pair[S]
    args = deal_args(pair[P])
    # 不考虑拼接字符串的sql中存在问号的情况,大概率?数就等于参数的数量
    idx = 0
    # 把问号换成特殊字符用于替换使用避免值中出现?导致重复
    new_place_flag = str(uuid.uuid1())
    sql = sql.replace('?', new_place_flag)
    max = sql.count(new_place_flag)
    while new_place_flag in sql and idx <= max:
        sql = sql.replace(new_place_flag, args[idx], 1)
        idx += 1
    return sql


quote_type = "String|Timestamp|Date|Time|LocalDate|LocalTime|LocalDateTime|"
direct_type = "Integer|Byte|Double|Float|Short|Long|BigDecimal|Boolean"


def deal_args(src):
    # 固定在参数后面加一位逗号,符合正则匹配
    src = src + ", "
    p = re.compile("((\S| )*?)\((" + quote_type + direct_type + ")\)( )?, ")
    args = []
    while p.search(src):
        m = p.search(src)
        if m:
            oa = m.group(1)
            if m.group(3) in quote_type:
                args.append("'" + oa + "'")
            else:
                args.append(oa)
            src = p.sub(repl="\f", string=src, count=1)
    return args


if __name__ == '__main__':
    pass
