def quote(txt, div_flag, pre, after):
    if div_flag == '\\n':
        div_flag = '\n'
    res = []
    sp = txt.split(div_flag)
    for s in sp:
        res.append(pre + s + after)
    return res
