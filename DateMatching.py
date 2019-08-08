#!/usr/bin/env python3
# coding: UTF-8

import csv
import os
import pprint
import pandas as pd
import re


# 特定の列だけを読み込む（読み込み先の指定、項目の指定は後々変更する。ただ、タプルの中のリストって要素変更できないみたい。iniに変更できない。）
df_jamf = pd.read_csv('/Users/ito-tomoyo/Desktop/jamf-test.csv', usecols=['Computer Name', 'MAC Address']) #jamf
df_skysea = pd.read_csv('/Users/ito-tomoyo/Desktop/jamf-test2.csv', usecols=['Computer Name', 'MAC Address']) #skysea（未来的には）

# Pandas の insin を使って差分があるところを確認する（isin は同じものが含まれている列はTrueを返し、違っていればFalseを返す）
df_jamf['比較用の列'] = df_jamf[['Computer Name', 'MAC Address']].apply(lambda x: '{}_{}'.format(x[0], x[1]), axis=1)
df_skysea['比較用の列'] = df_skysea[['Computer Name', 'MAC Address']].apply(lambda x: '{}_{}'.format(x[0], x[1]), axis=1)

# カラムの名前を揃える関数を追加する
# HogeHoge

# 特定の列を比較する(header_usecols1にあって、header_usecols2にないList)
df_diff = df_jamf[~df_jamf['比較用の列'].isin(df_skysea['比較用の列'])]['Computer Name']

# その結果を出力する（同じ改装に）
print(df_diff)






##################################################################
# 下記はただのメモです
##################################################################

## 一応動く ##  
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



## 練習（殴り書き ##  
#header_usecols2 = pd.read_csv('/Users/ito-tomoyo/Desktop/skysea-hardware-list.csv', usecols=['コンピューター名', 'MACアドレス 1']) #skysea 
# 読み込んだ列を結合する場合
# merge = pd.concat([header_usecols1, header_usecols2], axis=1)
# merge.rename = pd.concat([jamf_header_usecols, header_usecols2], axis=1)
# merge = jamf_header_usecols[~header_usecols2['Computer Name'].isin(skysea_header_usecols[2])]
# print(merge)

# 特定の列を比較する
#def check(usecols):
#    if re.match(jamf_header_usecols in skysea_header_usecols, usecols):
#        print()
#    else:
#        print()

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