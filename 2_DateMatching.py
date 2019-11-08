#!/usr/bin/env python3
# coding: UTF-8

    import csv
    import os
    import pprint
    import pandas as pd
    import re
    import numpy as np
    import sys

# Pandasのカラムの設定（全てのPandas関数に適応される）
pd.set_option('display.max_rows', 1000)

######################
# データの読み込み＆整形
######################

### jamf

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
result_jamf = pd.concat([df_jamf_lower, df_jamf], axis=1)
# left = df_jamf_lower 
# right = df_jamf['J_MAC Address']
# result_jamf = left.join(right)
# jamf カラムを追加する
result_jamf['jamf'] = 1
# print(result_jamf)



### skysea (Mac)

# skyseaの特定の列だけを読み込む
df_skysea = pd.read_csv('/Users/ito-tomoyo/Desktop/skysea.csv', usecols=['コンピューター名', '端末機タイプ', 'MACアドレス 1', 'MACアドレス 2', 'MACアドレス 3', 'MACアドレス 4', 'MACアドレス 5', 'MACアドレス 6', 'MACアドレス 7', 'MACアドレス 8', 'MACアドレス 9']) #skysea
# カラムの名前を変える関数を追加する
df_skysea = df_skysea.rename(columns={'コンピューター名':'Computer Name', '端末機タイプ':'type', 'MACアドレス 1':'S_MAC Address 1', 'MACアドレス 2':'S_MAC Address 2', 'MACアドレス 3':'S_MAC Address 3', 'MACアドレス 4':'S_MAC Address 4', 'MACアドレス 5':'S_MAC Address 5', 'MACアドレス 6':'S_MAC Address 6', 'MACアドレス 7':'S_MAC Address 7', 'MACアドレス 8':'S_MAC Address 8', 'MACアドレス 9':'S_MAC Address 9'}) #skysea
# 特定の列の特定の文字列を抽出
df_skysea_mac = df_skysea.query('type.str.contains("Mac")', engine='python')
df_skysea_mac = df_skysea_mac.reset_index(drop=True)
# DataFrame は Valeをいじれないので、Seriesにして小文字に変更(macは小文字にしなくてOK)
df_skysea_mac['Computer Name'] = df_skysea_mac['Computer Name'].str.lower() 
# 数字、（）、ハイフンを削除する
df_skysea_mac['Computer Name'] = df_skysea_mac['Computer Name'].str.replace('\-\d$', '') 
df_skysea_mac['Computer Name'] = df_skysea_mac['Computer Name'].str.replace('\d$', '') 
df_skysea_mac['Computer Name'] = df_skysea_mac['Computer Name'].str.replace(' \(\d\)', '') 

# DataFrameにする
# df_skysea_lower = pd.DataFrame(df_skysea_lower.values)
# df_skysea_lower.columns = ['Computer Name']
# macのComputer NameをWINに合わせて15文字までに切っちゃう💫
df_skysea_mac['Computer Name'] = df_skysea_mac['Computer Name'].str.slice(0,15)
# df_skysea_mac = df_skysea_mac.apply(lambda x: x.str.slice(0, 15))
# print(df_skysea_mac)
# DataFrameの結合
# left = df_skysea_lower
# right = df_skysea.drop('Computer Name', axis=1)
# result_skysea_mac = left.join(right)
# result_skysea_mac = pd.merge(df_skysea_lower, df_skysea, on='Computer Name', how='outer')
# skysea カラムを追加する
df_skysea_mac['skysea'] = 2
# print(df_skysea)
# df_skysea.to_csv('/Users/ito-tomoyo/Desktop/to_csv_skysea_mac.csv', header = True)


### skysea (Win)

# skyseaの特定の列だけを読み込む
df_skysea = pd.read_csv('/Users/ito-tomoyo/Desktop/skysea.csv', usecols=['コンピューター名', '端末機タイプ', 'MACアドレス 1', 'MACアドレス 2', 'MACアドレス 3', 'MACアドレス 4', 'MACアドレス 5', 'MACアドレス 6', 'MACアドレス 7', 'MACアドレス 8', 'MACアドレス 9']) #skysea
# カラムの名前を変える関数を追加する
df_skysea = df_skysea.rename(columns={'コンピューター名':'Computer Name', '端末機タイプ':'type', 'MACアドレス 1':'S_MAC Address 1', 'MACアドレス 2':'S_MAC Address 2', 'MACアドレス 3':'S_MAC Address 3', 'MACアドレス 4':'S_MAC Address 4', 'MACアドレス 5':'S_MAC Address 5', 'MACアドレス 6':'S_MAC Address 6', 'MACアドレス 7':'S_MAC Address 7', 'MACアドレス 8':'S_MAC Address 8', 'MACアドレス 9':'S_MAC Address 9'}) #skysea
# 特定の列の特定の文字列を抽出
df_skysea_win = df_skysea.query('type.str.contains("Win")', engine='python')
df_skysea_win = df_skysea_win.reset_index(drop=True)
# DataFrame は Valeをいじれないので、Seriesにして小文字に変更(macは小文字にしなくてOK)
df_skysea_win['Computer Name']= df_skysea_win['Computer Name'].str.lower() 
# 数字、（）、ハイフンを削除する
df_skysea_win['Computer Name'] = df_skysea_win['Computer Name'].str.replace('\-\d$', '') 
df_skysea_win['Computer Name'] = df_skysea_win['Computer Name'].str.replace('\d$', '') 
df_skysea_win['Computer Name'] = df_skysea_win['Computer Name'].str.replace(' \(\d\)', '') 
# DataFrameにする
# df_skysea_lower = pd.DataFrame(df_skysea_lower.values)
# df_skysea_lower.columns = ['Computer Name']
# DataFrameの結合
# left = df_skysea_lower
# right = df_skysea.drop('Computer Name', axis=1)
# result_skysea_win = left.join(right)
# result_skysea_win = pd.merge(df_skysea_lower, df_skysea, on='Computer Name', how='outer')
# skysea カラムを追加する
df_skysea_win['skysea'] = 2
# result_skysea_win.to_csv('/Users/ito-tomoyo/Desktop/to_csv_skysea_win.csv', header = True)


### Skysea(Mac&Win) (Win)は '名前' を '最終ログインユーザー'に置き換えている
skysea_marge = pd.concat([df_skysea_mac, df_skysea_win], ignore_index=True, sort = True)
# print(skysea_marge)
# csvで出力
# skysea_marge.to_csv('/Users/ito-tomoyo/Desktop/to_csv_cylance_marge.csv', header = True)
# result_skysea_win = pd.merge(df_skysea_lower, df_skysea, on='Computer Name', how='outer')


### cylance(Mac)

# cylanceの特定の列だけを読み込む
df_cylance = pd.read_csv('/Users/ito-tomoyo/Desktop/cylance.csv', usecols=['名前', 'MACアドレス', 'ゾーン', '最終接続日', '最終ログインユーザー']) #cylance
# カラムの名前を変える関数を追加する
df_cylance = df_cylance.rename(columns={'名前':'Computer Name', 'MACアドレス':'C_MAC Address', 'ゾーン':'zone', '最終接続日':'Last connect', '最終ログインユーザー':'Last login user'}) #cylance
# 特定の列の特定の文字列を抽出
df_cylance_mac = df_cylance.query('zone.str.contains("Mac")', engine='python')
df_cylance_mac = df_cylance_mac.reset_index(drop=True)
# MACaddressを「,」区切りで分割
df_cylance_mac['C_MAC Address'] = df_cylance_mac['C_MAC Address'].str.split(',', expand=True) #cylance
# print(df_cylance_split)
# DataFrame は Valeをいじれないので、Seriesにして小文字に変更
df_cylance_mac['Computer Name'] = df_cylance_mac['Computer Name'].str.lower() 
df_cylance_mac['Last login user'] = df_cylance_mac['Last login user'].str.lower() 
# df_cylance_lower_2 = df_cylance ['Last login user'].str.lower() 
# 数字、（）、ハイフンを削除する
df_cylance_mac['Computer Name'] = df_cylance_mac['Computer Name'].str.replace('\-\d$', '') 
df_cylance_mac['Computer Name'] = df_cylance_mac['Computer Name'].str.replace('\-\d$', '') 
df_cylance_mac['Computer Name'] = df_cylance_mac['Computer Name'].str.replace('\d$', '') 
df_cylance_mac['Computer Name'] = df_cylance_mac['Computer Name'].str.replace(' \(\d\)', '') 
# print(df_cylance_lower)

# DataFrameにする
# df_cylance_lower = pd.DataFrame(df_cylance_lower.values)
# df_cylance_lower.columns = ['Computer Name']
# macのComputer NameをWINに合わせて15文字までに切っちゃう💫
df_cylance_mac['Computer Name'] = df_cylance_mac['Computer Name'].str.slice(0,15)
# DataFrameの結合
#left = df_cylance_lower
#right = df_cylance_split
#result_cylance = left.join(right)
# Zoneカラムを追加する
#left = result_cylance
#right = df_cylance ['zone']
#result_cylance_mac = left.join(right)
# Last connectカラムを追加する
# left = result_cylance
# right = df_cylance ['Last connect']
# result_cylance = left.join(right)
# Last userカラムを追加する
#left = result_cylance_mac
#right = df_cylance_lower_2
#result_cylance_mac = left.join(right)
# cylance カラムを追加する
df_cylance_mac['cylance'] = 3
# csvで出力
# df_cylance_mac.to_csv('/Users/ito-tomoyo/Desktop/to_csv_cylance_mac.csv', header = True)


### cylance(Win) '名前' を '最終ログインユーザー'に置き換えている

# cylanceの特定の列だけを読み込む
df_cylance = pd.read_csv('/Users/ito-tomoyo/Desktop/cylance.csv', usecols=['名前', 'MACアドレス', 'ゾーン', '最終接続日', '最終ログインユーザー']) #cylance
# カラムの名前を変える関数を追加する
df_cylance = df_cylance.rename(columns={'名前':'Last login user', 'MACアドレス':'C_MAC Address', 'ゾーン':'zone', '最終接続日':'Last connect', '最終ログインユーザー':'Computer Name'}) #cylance
# 特定の列の特定の文字列を抽出
df_cylance_win = df_cylance.query('zone.str.contains("Win")', engine='python')
df_cylance_win = df_cylance_win.reset_index(drop=True)
# MACaddressを「,」区切りで分割
df_cylance_win['C_MAC Address'] = df_cylance_win['C_MAC Address'].str.split(',', expand=True) #cylance
# DataFrame は Valeをいじれないので、Seriesにして小文字に変更
df_cylance_win['Computer Name'] = df_cylance_win['Computer Name'].str.lower() 
df_cylance_win['Last login user'] = df_cylance_win['Last login user'].str.lower() 
# 数字、（）、ハイフンを削除する
df_cylance_win['Computer Name'] = df_cylance_win['Computer Name'].str.replace('\-\d$', '') 
df_cylance_win['Computer Name'] = df_cylance_win['Computer Name'].str.replace('\d$', '') 
df_cylance_win['Computer Name'] = df_cylance_win['Computer Name'].str.replace(' \(\d\)', '') 
df_cylance_win['Computer Name'] = df_cylance_win['Computer Name'].str.replace(r'^freee\\', '') 
df_cylance_win['Computer Name'] = df_cylance_win['Computer Name'].str.replace(r'\\freee$', '') 

# DataFrameにする
# df_cylance_lower = pd.DataFrame(df_cylance_lower.values)
# df_cylance_lower.columns = ['Computer Name']

# WINはLastLoginUserのComputer Nameをにしているので、15文字までに切っちゃう）💫
df_cylance_win['Computer Name'] = df_cylance_win['Computer Name'].str.slice(0,15)

# DataFrameの結合
# left = df_cylance_lower
# right = df_cylance_split
# result_cylance = left.join(right)

# Zoneカラムを追加する
# left = result_cylance
# right = df_cylance ['zone']
# result_cylance_win = left.join(right)
# Last connectカラムを追加する
# left = result_cylance
# right = df_cylance ['Last connect']
# result_cylance = left.join(right)
# Last userカラムを追加する
# left = result_cylance
# right = df_cylance ['Last login user']
# result_cylance_win = left.join(right)
# left = result_cylance_win
# right = df_cylance_lower_2
# result_cylance_win = left.join(right)
# cylance カラムを追加する
# result_cylance_win['cylance'] = 3
# csvで出力
# df_cylance_win[.to_csv('/Users/ito-tomoyo/Desktop/to_csv_cylance_win.csv', header = True)


### cylance(Mac&Win) (Win)は '名前' を '最終ログインユーザー'に置き換えている
cylance_marge = pd.concat([df_cylance_mac, df_cylance_win], ignore_index=True, sort = True)
cylance_marge.to_csv('/Users/ito-tomoyo/Desktop/to_csv_cylance_marge.csv', header = True)
# result_skysea_win = pd.merge(df_skysea_lower, df_skysea, on='Computer Name', how='outer')

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
# DataFrameにする
df_stafflist_lower = pd.DataFrame(df_stafflist_lower.values)
# 列名の指定
df_stafflist_lower.columns = ['Computer Name']
# 'Department'カラムの追加
left = df_stafflist_lower
right = df_stafflist ['Department']
result_stafflist = left.join(right)
# staff list カラムを追加する
result_stafflist['staff list'] = 4
# print(result_stafflist)
#　csvで出力
# result_stafflist.to_csv('/Users/ito-tomoyo/Desktop/stafflist_update.csv', header = True)


######################
# データの突合
######################

# Cylanceの NameとLast loginが同じでないものを確認する
cylance_marge['check'] = (cylance_marge['Computer Name'] == cylance_marge['Last login user'])
#　csvで出力
cylance_marge.to_csv('/Users/ito-tomoyo/Desktop/check.csv', header = True)


# stafflistにあってskyseaにないList 💫
skysea_add_target = result_stafflist.merge(skysea_marge, left_on='Computer Name', right_on='Computer Name', how='left')
# sort
skysea_add_target  = skysea_add_target.sort_values('Computer Name')
# csvで出力
skysea_add_target.to_csv('/Users/ito-tomoyo/Desktop/skysea_delete_target.csv', header = True)


# stafflistにあってcylanceにないList 💫
cylance_add_target = result_stafflist.merge(cylance_marge, left_on='Computer Name', right_on='Computer Name', how='left')
# sort
cylance_add_target  = cylance_add_target.sort_values('Computer Name')
# csvで出力
cylance_add_target.to_csv('/Users/ito-tomoyo/Desktop/cylance_add_target.csv', header = True)

# CylanceにあってJamfにない 💫


# JamfにあってCylanceにない 💫


# skysea(mac)にあってstaff listにないもの。（skyseaは名前苗字の順番ではない場合があってそれが入ってしまう）
# not_containing_skysea = pd.merge(df_skysea_lower_mac, result_stafflist, how='left', on='Computer Name')
# print(not_containing_skysea)
# sort
# not_containing_skysea  = not_containing_skysea.sort_values('Computer Name')
# csvで出力
# not_containing_skysea.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_not_containing_skysea_mac.csv', header = True)


# staff listにあってskysea(win))にないもの。（skyseaは名前苗字の順番ではない場合があってそれが入ってしまう）
# not_containing_skysea = pd.merge(df_skysea_lower, result_stafflist, how='left', on='Computer Name')
# print(not_containing_skysea)
# sort
# not_containing_skysea  = not_containing_skysea.sort_values('Computer Name')
# csvで出力
# not_containing_skysea.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_not_containing_skysea_win.csv', header = True)




# skysea入ってないList
# not_containing_skysea = pd.merge(result_stafflist, result_skysea, how='left', on='Computer Name')
# print(not_containing_skysea)
# sort
# not_containing_skysea  = not_containing_skysea.sort_values('Computer Name')
# csvで出力
# not_containing_skysea.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_not_containing_skysea.csv', header = True)

# jamf入ってないリスト(名簿とCylance突合したものに,Jamfを突合させた)
# result_stafflist_cylance = pd.merge(result_stafflist, result_cylance, how='left', on='Computer Name')
# not_containing_jamf = pd.merge(result_stafflist_cylance, result_jamf, how='left', on='Computer Name')
# sort
# not_containing_jamf  = not_containing_jamf.sort_values('Computer Name')
# csvで出力
# not_containing_jamf.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_not_containing_jamf.csv', header = True)


# 2データA（jamf,skysea)の突合
# result_jamf_skysea = pd.merge(result_skysea, result_jamf, how='left', on='Computer Name')

# 2データB（skysea,cylance)の突合
# result_skysea_cylance = pd.merge(result_skysea, result_cylance, how='left', on='Computer Name')
# csvで出力
# result_skysea_cylance.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_2result_all.csv', header = True)

# 3データ（jamf&skysea,cylance)の突合
# result_3 = pd.merge(result_jamf_skysea, result_cylance, how='left', on='Computer Name')
# sort
# result_3  = result_3 .sort_values('Computer Name')
# 'macbook と freee を含まないもの抽出
# result_2  = result_2[~result_2['Computer Name'].str.contains('macbook')]
# result_3  = result_3[~result_3['Computer Name'].str.contains('freee')]
# csvで出力
# result_3.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_3result_all.csv', header = True)

# 4データ（jamf,skysea & cylance + 名簿)の突合
# result_all = pd.merge(result_3, result_stafflist, how='left', on='Computer Name')
# sort
# result_all  = result_all.sort_values('Computer Name')
# 'macbook と freee を含まないもの抽出（ここ理屈わかってない（~）⭐️）
# result_all  = result_all[~result_all['Computer Name'].str.contains('macbook')]
# result_all  = result_all[~result_all['Computer Name'].str.contains('freee')]
# csvで出力
# result_all.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_4result_all.csv', header = True)


