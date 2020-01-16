#!/usr/bin/env python3
# coding: UTF-8

import csv
import os
import pandas as pd
import codecs as cd
import re
import sys

def exception_list(df):
    with open('/Users/ito-tomoyo/Practice/ExceptionList.csv',  newline='') as f:
        dataReader = csv.reader(f)
        for row in dataReader:
             # print("{} {}".format(row[0],row[1]))
            df['Computer Name'] = df['Computer Name'].str.replace(row[0], row[1]) 
            if 'Last login user' in df.columns:
                df['Last login user'] = df['Last login user'].str.replace(row[0], row[1]) 
    return df

def normalize(df):
    df['Computer Name'] = df['Computer Name'].str.lower() 
    df['Computer Name'] = df['Computer Name'].str.replace(r'^freeecs\\', '') 
    df['Computer Name'] = df['Computer Name'].str.replace(r'\\freee$', '') 
    df['Computer Name'] = df['Computer Name'].str.replace(r'\\admin', '') 
    df['Computer Name'] = df['Computer Name'].str.replace(r'^freee\\', '') 
    df['Computer Name'] = df['Computer Name'].str.replace('\-\d$', '') 
    df['Computer Name'] = df['Computer Name'].str.replace('\d$', '') 
    df['Computer Name'] = df['Computer Name'].str.replace(' \(\d\)', '') 
    if 'Last login user' in df.columns:
        df['Last login user'] = df['Last login user'].str.lower() 
        df['Last login user'] = df['Last login user'].str.replace('\-\d$', '') 
        df['Last login user'] = df['Last login user'].str.replace('\d$', '') 
        df['Last login user'] = df['Last login user'].str.replace(' \(\d\)', '') 
    return df

def Ignore_Location(df): #stafflistにだけ読み込ませる
    df.drop(df[(df['type'] == '業務委託') & (df['Location'] == '新宿')].index, inplace=True)
    df.drop(df[(df['type'] == '業務委託') & (df['Location'] == '九州')].index, inplace=True)
    df.drop(df[(df['type'] == '業務委託') & (df['Location'] == '札幌')].index, inplace=True)
    df.drop(df[(df['type'] == '業務委託') & (df['Location'] == '広島')].index, inplace=True)
    df.drop(df[(df['Location'] == 'リモート')].index, inplace=True)
    df.drop(df[(df['Status'] == '休職')].index, inplace=True)
    

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
df_jamf = normalize(df_jamf)
df_jamf = exception_list(df_jamf)
# jamf カラムを追加する
df_jamf['jamf'] = 1
# print(result_jamf)


# 重複したMac Addressのチェック 
df_cylance = pd.read_csv('/Users/ito-tomoyo/Desktop/cylance.csv', usecols=['名前', 'MACアドレス', 'ゾーン']) #cylance
# MACaddressを「,」区切りで分割
df_cylance['MACアドレス'] = df_cylance['MACアドレス'].str.split(',', expand=True) #cylance
df_cylance = df_cylance.pivot_table(values=['ゾーン'], index=['MACアドレス'], columns=['ゾーン'], aggfunc='sum')
# csvで出力
df_cylance.to_csv('/Users/ito-tomoyo/Desktop/Mac_Address_Check.csv', header = True) 
# print(df_cylance)

### skysea (Mac)
# skyseaの特定の列だけを読み込む
# with codecs.open('/Users/ito-tomoyo/Desktop/skysea.csv',"r", "Shift-JIS", "ignore") as file:
#    df_skysea = pd.read_table(file, delimiter=",")
df_skysea = pd.read_csv('/Users/ito-tomoyo/Desktop/skysea.csv', encoding="shift-jis", usecols=['コンピューター名', '端末機タイプ', 'MACアドレス 1', 'MACアドレス 2', 'MACアドレス 3', 'MACアドレス 4', 'MACアドレス 5', 'MACアドレス 6', 'MACアドレス 7', 'MACアドレス 8', 'MACアドレス 9']) #skysea
# df_skysea = pd.read_csv('/Users/ito-tomoyo/Desktop/skysea.csv', usecols=['コンピューター名', '端末機タイプ', 'MACアドレス 1', 'MACアドレス 2', 'MACアドレス 3', 'MACアドレス 4', 'MACアドレス 5', 'MACアドレス 6', 'MACアドレス 7', 'MACアドレス 8', 'MACアドレス 9']) #skysea
# カラムの名前を変える関数を追加する
df_skysea = df_skysea.rename(columns={'コンピューター名':'Computer Name', '端末機タイプ':'type', 'MACアドレス 1':'S_MAC Address 1', 'MACアドレス 2':'S_MAC Address 2', 'MACアドレス 3':'S_MAC Address 3', 'MACアドレス 4':'S_MAC Address 4', 'MACアドレス 5':'S_MAC Address 5', 'MACアドレス 6':'S_MAC Address 6', 'MACアドレス 7':'S_MAC Address 7', 'MACアドレス 8':'S_MAC Address 8', 'MACアドレス 9':'S_MAC Address 9'}) #skysea
# 特定の列の特定の文字列を抽出
df_skysea_mac = df_skysea.query('type.str.contains("Mac")', engine='python')
df_skysea_mac = df_skysea_mac.reset_index(drop=True)
# DataFrame は Valeをいじれないので、Seriesにして小文字に変更(macは小文字にしなくてOK)
# 数字、（）、ハイフンを削除する
df_skysea_mac = normalize(df_skysea_mac)
df_skysea_mac = exception_list(df_skysea_mac)
# skysea カラムを追加する
df_skysea_mac['skysea'] = 2
# print(df_skysea)
# df_skysea.to_csv('/Users/ito-tomoyo/Desktop/to_csv_skysea_mac.csv', header = True)


### skysea (Win)
# skyseaの特定の列だけを読み込む
df_skysea = pd.read_csv('/Users/ito-tomoyo/Desktop/skysea.csv', encoding="shift-jis", usecols=['コンピューター名', '端末機タイプ', 'MACアドレス 1', 'MACアドレス 2', 'MACアドレス 3', 'MACアドレス 4', 'MACアドレス 5', 'MACアドレス 6', 'MACアドレス 7', 'MACアドレス 8', 'MACアドレス 9']) #skysea
# カラムの名前を変える関数を追加する
df_skysea = df_skysea.rename(columns={'コンピューター名':'Computer Name', '端末機タイプ':'type', 'MACアドレス 1':'S_MAC Address 1', 'MACアドレス 2':'S_MAC Address 2', 'MACアドレス 3':'S_MAC Address 3', 'MACアドレス 4':'S_MAC Address 4', 'MACアドレス 5':'S_MAC Address 5', 'MACアドレス 6':'S_MAC Address 6', 'MACアドレス 7':'S_MAC Address 7', 'MACアドレス 8':'S_MAC Address 8', 'MACアドレス 9':'S_MAC Address 9'}) #skysea
# 特定の列の特定の文字列を抽出
df_skysea_win = df_skysea.query('type.str.contains("Win")', engine='python')
df_skysea_win = df_skysea_win.reset_index(drop=True)
# DataFrame は Valeをいじれないので、Seriesにして小文字に変更(macは小文字にしなくてOK)
# 数字、（）、ハイフンを削除する
df_skysea_win = normalize(df_skysea_win)
df_skysea_win['skysea'] = 2
# result_skysea_win.to_csv('/Users/ito-tomoyo/Desktop/to_csv_skysea_win.csv', header = True)
### Skysea(Mac&Win) (Win)は '名前' を '最終ログインユーザー'に置き換えている
skysea_marge = pd.concat([df_skysea_mac, df_skysea_win], ignore_index=True, sort = True)
# macのComputer NameをWINに合わせて15文字までに切っちゃう
skysea_marge['Computer Name'] = skysea_marge['Computer Name'].str.slice(0,13)
# csvで出力
# skysea_marge.to_csv('/Users/ito-tomoyo/Desktop/to_csv_skysea_marge.csv', header = True)


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
# 数字、（）、ハイフンを削除する
df_cylance_mac = normalize(df_cylance_mac)
df_cylance_mac = exception_list(df_cylance_mac)
# cylance カラムを追加する
df_cylance_mac['cylance'] = 3
# csvで出力
df_cylance_mac.to_csv('/Users/ito-tomoyo/Desktop/to_csv_cylance_mac.csv', header = True)

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
# 数字、（）、ハイフンを削除する
df_cylance_win = normalize(df_cylance_win)
df_cylance_win = exception_list(df_cylance_win)
# cylance カラムを追加する
df_cylance_win['cylance'] = 3
# csvで出力
# df_cylance_win[.to_csv('/Users/ito-tomoyo/Desktop/to_csv_cylance_win.csv', header = True)


### cylance(Mac&Win) (Win)は '名前' を '最終ログインユーザー'に置き換えている
cylance_marge = pd.concat([df_cylance_mac, df_cylance_win], ignore_index=True, sort = True)

# csvで出力
cylance_marge.to_csv('/Users/ito-tomoyo/Desktop/to_csv_cylance_marge2.csv', header = True)

# staff listの特定の列を読み込む
df_stafflist = pd.read_csv('/Users/ito-tomoyo/Desktop/stafflist.csv', header=1, usecols=['Name', '部署', '雇用形態', '勤務地', '就業状況']) #staff list
# カラムの名前を変える関数を追加する
df_stafflist = df_stafflist.rename(columns={'Name':'Computer Name', '部署':'Department', '雇用形態':'type', '勤務地':'Location', '就業状況':'Status'}) #staff list
# スペース区切りで列を分割する
df_stafflist_split  = df_stafflist['Computer Name'].str.split('\s', expand=True)
# catを使って列を一つに
df_stafflist['Computer Name'] = (df_stafflist_split[1].str.cat(df_stafflist_split[0], sep='-'))
#名前が間違っている人の置き換え
df_stafflist = normalize(df_stafflist)
df_stafflist = exception_list(df_stafflist)
df_Location = Ignore_Location(df_stafflist)

#対象外Listに基づき削除 
with open('/Users/ito-tomoyo/Practice/IgnoreList.csv',  newline='') as z:
    dataReader = csv.reader(z)
    for row in dataReader:
         df_stafflist = df_stafflist[df_stafflist['Computer Name'] != row[0]]
         # print("{}".format(row[0]))

# WINはLastLoginUserのComputer Nameをにしているので、15文字までに切っちゃう）
df_stafflist['Computer Name'] = df_stafflist['Computer Name'].str.slice(0,13)
# staff list カラムを追加する
df_stafflist['staff list'] = 4

# print(df_stafflist)
#　csvで出力
df_stafflist.to_csv('/Users/ito-tomoyo/Desktop/stafflist_update.csv', header = True)


######################
# データの突合
######################

# Cylanceの NameとLast loginが同じでないものを確認する
cylance_marge['check'] = (cylance_marge['Computer Name'] == cylance_marge['Last login user'])
# macのComputer NameをWINに合わせて15文字までに切っちゃう
cylance_marge['Computer Name'] = cylance_marge['Computer Name'].str.slice(0,13)
cylance_marge['Last login user'] = cylance_marge['Last login user'].str.slice(0,13)
#　csvで出力
cylance_marge.to_csv('/Users/ito-tomoyo/Desktop/check.csv', header = True)
# 重複した行の数をカウント


# stafflistにあってskyseaにないList 💫
skysea_add_target = df_stafflist.merge(skysea_marge, left_on='Computer Name', right_on='Computer Name', how='left')
# sort
skysea_add_target = skysea_add_target.sort_values('Computer Name')
# csvで出力
skysea_add_target.to_csv('/Users/ito-tomoyo/Desktop/skysea_add_target.csv', header = True)
# print(skysea_add_target.duplicated(subset='Computer Name'))


# stafflistにあってcylanceにないList 💫
cylance_add_target = df_stafflist.merge(cylance_marge, left_on='Computer Name', right_on='Computer Name', how='left')
# sort
cylance_add_target  = cylance_add_target.sort_values('Computer Name')
# 違いがあるものだけだす
# cylance_add_target = df_stafflist.concat([df_stafflist['Computer Name'],cylance_marge['Computer Name']]).drop_duplicates(keep=False)
# csvで出力
cylance_add_target.to_csv('/Users/ito-tomoyo/Desktop/cylance_add_target.csv', header = True)


# skysea_add_targetにあってcylance_add_targetにないList
Comparison = skysea_add_target.merge(cylance_add_target, left_on='Computer Name', right_on='Computer Name', how='left')
# sort
Comparison  = Comparison.sort_values('Computer Name')
# csvで出力
cylance_add_target.to_csv('/Users/ito-tomoyo/Desktop/Comparison.csv', header = True)


# CylanceにあってJamfにない 
# JamfにあってCylanceにない 

