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

######################
# データの読み込み＆整形
######################

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
# csvで出力
result_stafflist.to_csv('/Users/ito-tomoyo/Desktop/test.csv', header = True)


######################
# データの突合
######################

# skysea入ってないList
not_containining_jskysea = pd.merge(result_stafflist, result_skysea, how='left', on='Computer Name')
# sort
not_containining_jskysea  = not_containining_jskysea.sort_values('Computer Name')
# csvで出力
not_containining_jskysea.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_not_containining_skysea.csv', header = True)

# jamf入ってないリスト(名簿とCylance突合したものに,Jamfを突合させた)
result_stafflist_cylance = pd.merge(result_stafflist, result_cylance, how='left', on='Computer Name')
not_containining_jamf = pd.merge(result_stafflist_cylance, result_jamf, how='left', on='Computer Name')
# sort
not_containining_jamf  = not_containining_jamf.sort_values('Computer Name')
# csvで出力
not_containining_jamf.to_csv('/Users/ito-tomoyo/Desktop/to_csv_out_not_containining_jamf.csv', header = True)

exit
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

