def quote(txt, div_flag, pre, after):
    res = []
    for s in txt.split(div_flag):
        res.append(pre + s + after)
    return res
