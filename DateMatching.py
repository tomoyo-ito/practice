#!/usr/bin/env python3
# coding: UTF-8

import csv
import os
import pprint
import pandas as pd
import re

# Pandasのカラムの設定（全てのPandas関数に適応される）
pd.set_option('display.max_rows', 1500)

# jamfの特定の列だけを読み込む
df_jamf = pd.read_csv('/Users/ito-tomoyo/Desktop/jamf.csv', usecols=['Computer Name', 'MAC Address']) #jamf
# MACaddressの：を-に置換
df_jamf = df_jamf.replace(':', '-', regex = True) #jamf
#print(df_jamf)

# skyseaの特定の列だけを読み込む
df_skysea = pd.read_csv('/Users/ito-tomoyo/Desktop/skysea.csv', usecols=['コンピューター名', 'MACアドレス 1']) #skysea
# カラムの名前を変える関数を追加する
df_skysea = df_skysea.rename(columns={'コンピューター名':'Computer Name', 'MACアドレス 1':'MAC Address'}) #skysea
#print(df_skysea)

# cylanceの特定の列だけを読み込む
df_cylance = pd.read_csv('/Users/ito-tomoyo/Desktop/cylance.csv', usecols=['名前', 'MACアドレス']) #cylance
# カラムの名前を変える関数を追加する
df_cylance = df_skysea.rename(columns={'名前':'Computer Name', 'MACアドレス':'MAC Address'}) #cylance
#print(df_cylance)

# 特定の列を比較する(cylanceにあって、jamfにないList) cylanceはwinも範囲に入ってるので
df_diff = df_cylance[~df_cylance['Computer Name'].isin(df_jamf['Computer Name'])]['Computer Name']
# csvで出力
df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_cylance_jamf_diff.csv', header = True)

# 特定の列を比較する(cylanceにあって、skyseaにないList) ⭐存在しない（ちゃんと比較できなかったのかも）
df_diff = df_cylance[~df_cylance['Computer Name'].isin(df_skysea['Computer Name'])]['Computer Name']
# csvで出力
df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_cylance_skesea_diff.csv', header = True)

# 特定の列を比較する(jamfにあって、cylanceにないList) 特殊なComputer Name、退職した人？
df_diff = df_jamf[~df_jamf['Computer Name'].isin(df_cylance['Computer Name'])]['Computer Name']
# csvで出力
df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_jamf_cylance_diff.csv', header = True)

# 特定の列を比較する(jamfにあって、skyseaにないList) 特殊なComputer Name、退職した人？
df_diff = df_jamf[~df_jamf['Computer Name'].isin(df_skysea['Computer Name'])]['Computer Name']
# csvで出力
df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_jamf_skysea_diff.csv', header = True)

# 特定の列を比較する(skyseaにあって、cylanceにないList) ⭐存在しない （ちゃんと比較できなかったのかも）
df_diff = df_skysea[~df_skysea['Computer Name'].isin(df_cylance['Computer Name'])]['Computer Name']
# csvで出力
df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_skesea_cylance_diff.csv', header = True)

# 特定の列を比較する(skyseaにあって、jamfにないList) skyseaにはwinあるから・・・
df_diff = df_skysea[~df_skysea['Computer Name'].isin(df_jamf['Computer Name'])]['Computer Name']
# csvで出力
df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_skesea_jamf_diff.csv', header = True)

exit
# 特定の列を比較する(jamfにあって、skyseaにないList)
#df_diff = df_jamf[~df_jamf['Computer Name'].isin(df_skysea['Computer Name'])]['Computer Name']
# csvで出力
#df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out.csv')

# 特定の列を比較する(skyseaにあって、jamfにないList)
#df_diff2 = df_skysea[~df_skysea['Computer Name'].isin(df_jamf['Computer Name'])]['Computer Name']
# csvで出力
#df_diff2.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out2.csv')

# Pandas の insin を使って差分があるところを確認する（isin は同じものが含まれている列はTrueを返し、違っていればFalseを返す）
df_jamf['比較用の列'] = df_jamf[['Computer Name', 'MAC Address']].apply(lambda x: '{}_{}'.format(x[0], x[1]), axis=1)
df_skysea['比較用の列'] = df_skysea[['Computer Name', 'MAC Address']].apply(lambda x: '{}_{}'.format(x[0], x[1]), axis=1)

# 特定の列を比較する(jamfにあって、skyseaにないList)
df_diff = df_jamf[~df_jamf['比較用の列'].isin(df_skysea['比較用の列'])]

# その結果を出力する（同じ階層に）
# print(df_diff)






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