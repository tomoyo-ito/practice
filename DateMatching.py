#!/usr/bin/env python3
# coding: UTF-8

import csv
import os
import pprint
import sets
import pandas as pd


# 特定の列だけを読み込む場合 
jamf_header_usecols = pd.read_csv('/Users/ito-tomoyo/Desktop/jamf-test.csv', usecols=['Computer Name', 'MAC Address'])
skysea_header_usecols = pd.read_csv('/Users/ito-tomoyo/Desktop/skysea-hardware-list.csv', usecols=[0, 11])

# 読み込んだ列を結合する場合
merge = pd.concat([jamf_header_usecols, skysea_header_usecols], axis=1)
print(merge)

# 特定の列を比較する

# その結果を出力する（同じ改装に）

# 一応動く #
#def make_lines_set(path):
#    f = open(path, 'r')
#    lines = f.readlines() # 1行ずつ読み込む
#    sets = set(lines) # set型にすると重複がなくなる
#    f.close()
#    return sets

# 読み込みたいファイルを指定する
#jamf = make_lines_set('/Users/ito-tomoyo/Desktop/jamf-test.csv')                      
#skysea = make_lines_set('/Users/ito-tomoyo/Desktop/skysea-hardware-list.csv')
 
# jamf-test.csv にのみ存在する行を出力したい
#results = jamf.difference(skysea)
#for result in results:
#    print(result)


# 練習（殴り書き）# 

#ret = skysea_header_usecols[~skysea_header_usecols.ID.isin(jamf_header_usecols.ID)]
#ret.to_csv('merge.csv', index=None)
#print(ret)


#with open('/Users/ito-tomoyo/Desktop/jamf-test.csv') as f:
#    reader = csv.reader(f, delimiter=' ')
#    l = [row for row in reader]
#print(l)


# csvデータを読み込み用で開く
# csv_file = open('/Users/ito-tomoyo/Desktop/jamf-test.csv')
# リスト形式
# f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
#辞書形式
# f = csv.DictReader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

# print(csv_file)
# csv_file = os.path.abspath("jamf-test.csv")