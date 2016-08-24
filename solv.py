
# coding: UTF-8

import re

w,h = 7,7
v_array = [[3],[5],[2,3],[6],[6],[5],[3]]
h_array = [[2,2],[7],[2,4],[7],[5],[3],[1]]

# これは以下のようになる。
#             2
#       3  5  3  6  6  5  3
#     ----------------------
# 2  2|    x  x     x  x
#    7| x  x  x  x  x  x  x
# 2  4| x  x     x  x  x  x
#    7| x  x  x  x  x  x  x
#    5|    x  x  x  x  x
#    3|       x  x  x
#    1|          x


print("--------------------")

t = [['_' for i in range(w)] for j in range(h)]

def show(table, v_array, h_array):
    w = len(v_array)
    h = len(h_array)

    v_max = max([ len(c) for c in v_array ] )
    h_max = max([ len(c) for c in h_array ] )

    ret_str = ""

    # V array
    vz_array = [[' '] * (v_max - len(c)) for c in v_array]
    vr = [ list(reversed(s)) for s in v_array ]
    z = [ [str(ii) for ii in i]  + j for (i,j) in zip(vr, vz_array) ]
    vl = list(reversed(list( zip(*z) )))  # transpose
    for l in vl:
        ret_str += " " * h_max * 2
        for c in l:
            ret_str += (" " + c)
        ret_str += "\n"

    # H array
    for y in range(h):
        h_list = h_array[y]
        h_list = [' '] * (h_max - len(h_list)) + h_list
        for c in h_list:
            ret_str += (" " + str(c))

        for c in table[y]:
            ret_str += ( " " + c)

        ret_str += "\n"
    return ret_str
print( show(t, v_array, h_array))



def apply_h(y, t, proc):
    '''
    行に対してprocを実行してテーブルtへ反映する
    '''
    hl = h_array[y]
    t[y] = proc(hl, t[y])

def apply_v(x, t, proc):
    '''
    列に対してprocを実行してテーブルtへ反映する
    '''
    vl = v_array[x]
    vv = [ hl[x] for hl in t ]
    vv = proc(vl, vv)
    for y in range(h):
        t[y][x] = vv[y]

def apply_all(t, proc):
    h = len(t)
    w = len(t[0])
    for y in range(h):
        apply_h(y, t, proc)
    for x in range(w):
        apply_v(x, t, proc)



# 行 or 列 が確定していれば Trueを返す
def is_complete_line(hl, line):
    '''
    ある列または行(line)が完成したかどうか判定する
    '''
    if line.count("_") == 0 :
        return True

    s = ""
    for c in line:
        s += c
    splited = list(filter(lambda w: len(w) > 0, re.split(r'_|\^', s)))
    return [ len(e) for e in splited] == hl

# 行 or 列 が確定していれば、空いているところに不使用マーク(^)を付ける
def fix_line(hl, line):
    if is_complete_line(hl, line):
        return list(map( lambda e: '^' if e == '_' else e, line ))
    else :
        return line

# 確定コマを探す
def fix_easy(hl, line):
    '''
    ある1行 or 1列に対して、確定してマークできるところにチェックを入れる
    hl : 問題として与えられる連続するマーク数
    line : hlがさす行
    '''
    line = list(line) # clone

    tightan  = sum(hl) + (len(hl) - 1) # 何マス必要か
    variable = w - tightan # 動かせる余地

    # 確定できるところを探す
    s = 0
    for x in range(len(hl)):
        e = hl[x]
        fix_cnt = e - variable
        if fix_cnt > 0: # 確定できる！
            begin_index = s + x + variable
            end_index   = begin_index + fix_cnt
            line[begin_index:end_index] = (['x'] * fix_cnt)
        s += e
    return line

print("まずは前処理として、確定コマを探す")
apply_all(t, fix_easy)
apply_all(t, fix_line)
print( show(t, v_array, h_array))

print("未確定のコマを確定していく")



print( show(t, v_array, h_array))
