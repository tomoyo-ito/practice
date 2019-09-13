#!/usr/bin/env python3
# coding: UTF-8

import csv
import os
import pprint
import pandas as pd
import re
import numpy as np

# Pandasのカラムの設定（全てのPandas関数に適応される）
pd.set_option('display.max_rows', 10)

# jamfの特定の列だけを読み込む
df_jamf = pd.read_csv('/Users/ito-tomoyo/Desktop/jamf.csv', usecols=['Computer Name', 'MAC Address']) #jamf
# カラムの名前を変える関数を追加する
df_jamf = df_jamf.rename(columns={'Computer Name':'Computer Name', 'MAC Address':'J_MAC Address'}) #jamf
# MACaddressの：を-に置換
df_jamf = df_jamf.replace(':', '-', regex = True) #jamf
# DataFrame は Valeをいじれないので、Seriesにして小文字に変更
df_jamf_lower = df_jamf['Computer Name'].str.lower() 
# DataFrameにする
df_jamf_lower = pd.DataFrame(df_jamf_lower.values)
df_jamf_lower.columns = ['Computer Name']
# DataFrameの結合
left = df_jamf_lower 
right = df_jamf['J_MAC Address']
result_jamf = left.join(right)
# jamf カラムを追加する
result_jamf['jamf'] = 1
# print(result_jamf)
# df_jamf_merge = df_jamf.merge(pd.DataFrame(data = [df_jamf_lower.values] * len(df_jamf_lower), columns = df_jamf_lower.index, index=df_jamf.index), left_index=True, right_index=True)

# skyseaの特定の列だけを読み込む
df_skysea = pd.read_csv('/Users/ito-tomoyo/Desktop/skysea.csv', usecols=['コンピューター名', 'MACアドレス 1', 'MACアドレス 2', 'MACアドレス 3', 'MACアドレス 4', 'MACアドレス 5', 'MACアドレス 6', 'MACアドレス 7', 'MACアドレス 8', 'MACアドレス 9']) #skysea
# カラムの名前を変える関数を追加する
df_skysea = df_skysea.rename(columns={'コンピューター名':'Computer Name', 'MACアドレス 1':'S_MAC Address 1', 'MACアドレス 2':'S_MAC Address 2', 'MACアドレス 3':'S_MAC Address 3', 'MACアドレス 4':'S_MAC Address 4', 'MACアドレス 5':'S_MAC Address 5', 'MACアドレス 6':'S_MAC Address 6', 'MACアドレス 7':'S_MAC Address 7', 'MACアドレス 8':'S_MAC Address 8', 'MACアドレス 9':'S_MAC Address 9'}) #skysea
# DataFrame は Valeをいじれないので、Seriesにして小文字に変更
df_skysea_lower = df_skysea ['Computer Name'].str.lower() 
# DataFrameにする
df_skysea_lower  = pd.DataFrame(df_skysea_lower.values)
df_skysea_lower.columns = ['Computer Name']
# DataFrameの結合
left = df_skysea_lower
right = df_skysea.drop('Computer Name', axis=1)
result_skysea = left.join(right)
# print(result_skysea)
# skysea カラムを追加する
result_skysea['skysea'] = 2
# print(result_skysea)



# cylanceの特定の列だけを読み込む
df_cylance = pd.read_csv('/Users/ito-tomoyo/Desktop/cylance.csv', usecols=['名前', 'MACアドレス', 'ゾーン', '最終接続日', '最終ログインユーザー']) #cylance
# カラムの名前を変える関数を追加する
df_cylance = df_cylance.rename(columns={'名前':'Computer Name', 'MACアドレス':'C_MAC Address', 'ゾーン':'Zone', '最終接続日':'Last connect', '最終ログインユーザー':'Last login user'}) #cylance
# MACaddressを「,」区切りで分割
df_cylance_split = df_cylance ['C_MAC Address'] .str.split(',', expand=True) #cylance
# print(df_cylance_split)
# DataFrame は Valeをいじれないので、Seriesにして小文字に変更
df_cylance_lower = df_cylance ['Computer Name'].str.lower() 
# DataFrameにする
df_cylance_lower = pd.DataFrame(df_cylance_lower.values)
df_cylance_lower.columns = ['Computer Name']
# DataFrameの結合
left = df_cylance_lower
right = df_cylance_split
result_cylance = left.join(right)
# cylance カラムを追加する
result_cylance['cylance'] = 3
# Zoneカラムを追加する
left = result_cylance
right = df_cylance ['Zone']
result_cylance = left.join(right)
# Last connectカラムを追加する
left = result_cylance
right = df_cylance ['Last connect']
result_cylance = left.join(right)
# Last userカラムを追加する
left = result_cylance
right = df_cylance ['Last login user']
result_cylance = left.join(right)
 # print(result_cylance)



# staff listの特定の列を読み込む
df_stafflist = pd.read_csv('/Users/ito-tomoyo/Desktop/stafflist.csv', header=1, usecols=['Name', '部署']) #staff list
# カラムの名前を変える関数を追加する
df_stafflist = df_stafflist.rename(columns={'Name':'Computer Name', '部署':'Department'}) #staff list
# print(type(df_stafflist))
# スペース区切りで列を分割する
df_stafflist_split  = df_stafflist['Computer Name'].str.split('\s', expand=True)
# print(type(df_stafflist))
# カラムの名前を変える関数を追加する
# df_stafflist = df_stafflist.rename(columns={0:'Name3', 2:'Name1'}) #staff list
# カラムの順序を指定する(最初の：は「すべての行を取る」を意味し、:: – 1は列を逆方向に進むことを意味)
# #df_stafflist = df_stafflist.iloc[:, ::-1]
# 列を追加する
# df_stafflist[2] = '-' 
# 並び順の指定
# df_stafflist = df_stafflist.iloc[:,[1, 2, 0]]
# catを使って列を一つに
df_stafflist_split = (df_stafflist_split[1].str.cat(df_stafflist_split[0], sep='-'))
# データのタイプ確認する
# print(type(df_stafflist))
# 小文字にする
df_stafflist_lower = df_stafflist_split.str.lower() 
# DataFrameにする（ここ理屈わかってない⭐️）
df_stafflist_lower = pd.DataFrame(df_stafflist_lower.values)
# 列名の指定
df_stafflist_lower.columns = ['Computer Name']
# 'Department'カラムの追加
left = df_stafflist_lower
right = df_stafflist ['Department']
result_df_stafflist = left.join(right)
# csvで出力
result_df_stafflist.to_csv('/Users/ito-tomoyo/Desktop/test.csv', header = True)


# print(df_stafflist)
# ０と1の列を入れ替える
# df_stafflist_lower = df_stafflist_lower.str.split('\s', expand=True)
# スペースを-に変更する
# df_stafflist = df_stafflist.replace('\s', '-', regex = True) #staff list
# '-'区切りで前後入れ替える
# DataFrameにする
# df_stafflist_lower = pd.DataFrame(df_stafflist_lower.values)
# df_stafflist_lower.columns = ['Name']





# 2データ（jamf,skysea)の突合
result_jamf_skysea = pd.merge(result_skysea, result_jamf, how='left', on='Computer Name')
# sort
# result_jamf_skysea = result_jamf_skysea.sort_values('Computer Name')
# print(result_jamf_skysea)
# csvで出力
# result_jamf_skysea.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_result_skysea_jamf.csv', header = True)

# 3データ（jamf&skysea,cylance)の突合
result_3 = pd.merge(result_jamf_skysea, result_cylance, how='left', on='Computer Name')
# sort
result_3  = result_3 .sort_values('Computer Name')
# 'macbook と freee を含まないもの抽出
result_3  = result_3[~result_3['Computer Name'].str.contains('macbook')]
result_3  = result_3[~result_3['Computer Name'].str.contains('freee')]
# print(result_3)
# csvで出力
result_3.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_3result_all.csv', header = True)

# 4データ（jamf,skysea & cylance + 名簿)の突合
result_all = pd.merge(result_3, result_df_stafflist, how='left', on='Computer Name')
# sort
result_all  = result_all.sort_values('Computer Name')
# 'macbook と freee を含まないもの抽出（ここ理屈わかってない（~）⭐️）
result_all  = result_all[~result_all['Computer Name'].str.contains('macbook')]
result_all  = result_all[~result_all['Computer Name'].str.contains('freee')]
# print(result_all)

# csvで出力
result_all.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_4result_all.csv', header = True)


exit

# 特定の列を比較する(cylanceにあって、jamfにないList) cylanceはwinも範囲に入ってるので
df_diff = df_cylance[~df_cylance['Computer Name'].isin(df_jamf['Computer Name'])]['Computer Name']
# csvで出力
#df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_cylance_jamf_diff.csv', header = True)

# 特定の列を比較する(cylanceにあって、skyseaにないList) 
df_diff = df_cylance[~df_cylance['Computer Name'].isin(df_skysea['Computer Name'])]['Computer Name']
# csvで出力
#df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_cylance_skesea_diff.csv', header = True)

# 特定の列を比較する(jamfにあって、cylanceにないList) 特殊なComputer Name、退職した人？
df_diff = df_jamf[~df_jamf['Computer Name'].isin(df_cylance['Computer Name'])]['Computer Name']
# csvで出力
#df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_jamf_cylance_diff.csv', header = True)

# 特定の列を比較する(jamfにあって、skyseaにないList) 特殊なComputer Name、退職した人？
df_diff = df_jamf[~df_jamf['Computer Name'].isin(df_skysea['Computer Name'])]['Computer Name']
# csvで出力
#df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_jamf_skysea_diff.csv', header = True)

# 特定の列を比較する(skyseaにあって、cylanceにないList) 
df_diff = df_skysea[~df_skysea['Computer Name'].isin(df_cylance['Computer Name'])]['Computer Name']
# csvで出力
#df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_skesea_cylance_diff.csv', header = True)

# 特定の列を比較する(skyseaにあって、jamfにないList) skyseaにはwinあるから・・・
df_diff = df_skysea[~df_skysea['Computer Name'].isin(df_jamf['Computer Name'])]['Computer Name']
# csvで出力
# df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_skesea_jamf_diff.csv', header = True)

exit








##################################################################
# 下記はただのメモです
##################################################################


# 特定の列を比較する(jamfにあって、skyseaにないList)
#df_diff = df_jamf[~df_jamf['Computer Name'].isin(df_skysea['Computer Name'])]['Computer Name']
# csvで出力
#df_diff.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out.csv')

# 特定の列を比較する(skyseaにあって、jamfにないList)
#df_diff2 = df_skysea[~df_skysea['Computer Name'].isin(df_jamf['Computer Name'])]['Computer Name']
# csvで出力
#df_diff2.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out2.csv')

# Pandas の insin を使って差分があるところを確認する（isin は同じものが含まれている列はTrueを返し、違っていればFalseを返す）
#df_jamf['比較用の列'] = df_jamf[['Computer Name', 'MAC Address']].apply(lambda x: '{}_{}'.format(x[0], x[1]), axis=1)
#df_skysea['比較用の列'] = df_skysea[['Computer Name', 'MAC Address']].apply(lambda x: '{}_{}'.format(x[0], x[1]), axis=1)

# 特定の列を比較する(jamfにあって、skyseaにないList)
#df_diff = df_jamf[~df_jamf['比較用の列'].isin(df_skysea['比較用の列'])]

# その結果を出力する（同じ階層に）
# print(df_diff)



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

#-------------

# cylanceの特定の列だけを読み込む
df_cylance = pd.read_csv('/Users/ito-tomoyo/Desktop/cylance.csv', usecols=['名前', 'MACアドレス', 'ゾーン', '最終接続日', '最終ログインユーザー']) #cylance
# カラムの名前を変える関数を追加する
df_cylance = df_cylance.rename(columns={'名前':'Computer Name', 'MACアドレス':'C_MAC Address', 'ゾーン':'Zone', '最終接続日':'Last connect', '最終ログインユーザー':'Last login user'}) #cylance
# MACaddressを「,」区切りで分割
df_cylance_split = df_cylance ['C_MAC Address'] .str.split(',', expand=True) #cylance
# print(df_cylance_split)
# DataFrame は Valeをいじれないので、Seriesにして小文字に変更
df_cylance_lower = df_cylance ['Computer Name'].str.lower() 
# DataFrameにする
df_cylance_lower = pd.DataFrame(df_cylance_lower.values)
df_cylance_lower.columns = ['Computer Name']
# DataFrameの結合
left = df_cylance_lower
right = df_cylance_split
result_cylance = left.join(right)
# cylance カラムを追加する
result_cylance['cylance'] = 3
# Zoneカラムを追加する
left = result_cylance
right = df_cylance ['Zone']
result_cylance = left.join(right)
# Last connectカラムを追加する
left = result_cylance
right = df_cylance ['Last connect']
result_cylance = left.join(right)
# Last userカラムを追加する
left = result_cylance
right = df_cylance ['Last login user']
result_cylance = left.join(right)
# csvで出力
# result_cylance esult_stafflist.to_csv('/Users/ito-tomoyo/Desktop/result_cylance.csv', header = True)

# staff listの特定の列を読み込む
df_stafflist = pd.read_csv('/Users/ito-tomoyo/Desktop/stafflist.csv', header=1, usecols=['Name', '部署']) #staff list
# カラムの名前を変える関数を追加する
df_stafflist = df_stafflist.rename(columns={'Name':'Computer Name', '部署':'Department'}) #staff list
# スペース区切りで列を分割する
df_stafflist_split  = df_stafflist['Computer Name'].str.split('\s', expand=True)
# catを使って列を一つに
df_stafflist_split = (df_stafflist_split[1].str.cat(df_stafflist_split[0], sep='-'))
# 小文字にする
df_stafflist_lower = df_stafflist_split.str.lower() 
# DataFrameにする（ここ理屈わかってない⭐️）
df_stafflist_lower = pd.DataFrame(df_stafflist_lower.values)
# 列名の指定
df_stafflist_lower.columns = ['Computer Name']
# 'Department'カラムの追加
left = df_stafflist_lower
right = df_stafflist ['Department']
result_stafflist = left.join(right)
# print(result_stafflist)
# csvで出力
# result_stafflist.to_csv('/Users/ito-tomoyo/Desktop/stafflist.csv', header = True)


######################
# データの突合
######################

# データを結合すると欠損値(NaN)が出来てしまう問題を解決したい
# not_containing_skysea = pd.concat([result_stafflist.reset_index(drop=True), result_skysea.index(drop=True)], axis=1)
# skysea入ってないList
not_containing_skysea = pd.merge(result_stafflist, result_skysea, how='left', on='Computer Name')
print(not_containing_skysea)
# sort
not_containing_skysea  = not_containing_skysea.sort_values('Computer Name', how='left', on='Computer Name')
# csvで出力
not_containing_skysea.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_not_containing_skysea.csv', header = True)

# jamf入ってないリスト(名簿とCylance突合したものに,Jamfを突合させた)
result_stafflist_cylance = pd.merge(result_stafflist, result_cylance, how='left', on='Computer Name')
not_containing_jamf = pd.merge(result_stafflist_cylance, result_jamf, how='left', on='Computer Name')
# sort
not_containing_jamf  = not_containing_jamf.sort_values('Computer Name')
# csvで出力
not_containing_jamf.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_not_containing_jamf.csv', header = True)


# 2データ（jamf,skysea)の突合
result_jamf_skysea = pd.merge(result_skysea, result_jamf, how='left', on='Computer Name')

# 3データ（jamf&skysea,cylance)の突合
result_3 = pd.merge(result_jamf_skysea, result_cylance, how='left', on='Computer Name')
# sort
result_3  = result_3 .sort_values('Computer Name')
# 'macbook と freee を含まないもの抽出
result_3  = result_3[~result_3['Computer Name'].str.contains('macbook')]
result_3  = result_3[~result_3['Computer Name'].str.contains('freee')]
# csvで出力
result_3.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_3result_all.csv', header = True)

# 4データ（jamf,skysea & cylance + 名簿)の突合
result_all = pd.merge(result_3, result_stafflist, how='left', on='Computer Name')
# sort
result_all  = result_all.sort_values('Computer Name')
# 'macbook と freee を含まないもの抽出（ここ理屈わかってない（~）⭐️）
result_all  = result_all[~result_all['Computer Name'].str.contains('macbook')]
result_all  = result_all[~result_all['Computer Name'].str.contains('freee')]
# csvで出力
result_all.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_4result_all.csv', header = True)

