
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
t = [['_' for i in range(w)] for j in range(h)]

#-----------------------------------------------------------
def split(regexp = r'_|\^', str = ""):
    return list(filter(lambda w: len(w) > 0, re.split(regexp, str)))

def transpose(matrix):
    u"""
    正方行列matrixを転地した行列を返す
    """
    return list(reversed(list( zip(*matrix) )))

def str_join(list, delimiter=''):
    u"""
    与えられた各要素をStringにして連結する。
    """
    return delimiter.join([ str(s) for s in list ])

def show(table, v_array, h_array):
    u"""
    テーブルの状態を表示する
    """
    w = len(v_array)
    h = len(h_array)

    v_max = max([ len(c) for c in v_array ] )
    h_max = max([ len(c) for c in h_array ] )

    ret_str = ""

    # V array
    vz_array = [[' '] * (v_max - len(c)) for c in v_array]
    vr = [ list(reversed(s)) for s in v_array ]
    z = [ [str(ii) for ii in i]  + j for (i,j) in zip(vr, vz_array) ]
    vl = transpose(z)
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

def apply_h(y, t, proc):
    u"""
    行に対してprocを実行してテーブルtへ反映する
    """
    hl = h_array[y]
    t[y] = proc(hl, t[y])

def apply_v(x, t, proc):
    u"""
    列に対してprocを実行してテーブルtへ反映する
    """
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

# ----------------------------------------------------------------
def is_complete_line(hl, line):
    u"""
    ある列または行(line)が完成したかどうか判定する。
    行 or 列 が確定していれば Trueを返す
    """
    if line.count("_") == 0 :
        return True

    s = ""
    for c in line:
        s += c
    splited = split(r'_|\^', s)
    return [ len(e) for e in splited] == hl

def fix_line(hl, line):
    u"""
    行/列 が確定していれば、空いているところに不使用マーク(^)を付ける
    """
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
    variable = len(line) - tightan # 動かせる余地

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


# ----------------------------------------------------------------
print( show(t, v_array, h_array))

print("まずは前処理として、確定コマを探す")
apply_all(t, fix_easy)
apply_all(t, fix_line)
print( show(t, v_array, h_array))
print("未確定のコマを確定していく")


def find_avairable_patterns(l, line):
    u"""
    lineについて、配置可能なパターンをすべて返す。
    """
    # Todo: 分割前の位置を覚えておかないと書き戻せない
    areas = split(r'\^', str_join(line))

    # 再帰で配置可能なパターンを探索
    patterns = find_avairable_patterns_sub(len(areas), l, areas, [], [])

    print("------------")
    print(areas)
    print(patterns)

    if len(patterns) > 1:
        # Todo: パターンの中で共通する部分を塗る
        return line

    return line


def find_avairable_patterns_sub(max_depth, least_l, least_area, result, results, d = 1):
    if d >= max_depth:
        result.append(least_l)
        results.append(result)
        return results

    for i in range(len(least_l)+1):
        tmp_res = list(result)
        tmp_res.append(least_l[0:i])
        ls = least_l[i:]
        find_avairable_patterns_sub(max_depth, ls, least_area[1:], tmp_res, results, d+1)

    return results

for y in range(len(h_array)):
    print(find_avairable_patterns(h_array[y], t[y]))



# ----------------------------------------------------------------
# print( show(t, v_array, h_array))
