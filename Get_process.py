#!/usr/bin/env python3
# coding: UTF-8

import csv
import os
import shutil
import pandas as pd
import re
import sys
import boto3
from zipfile import ZipFile
import datetime
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", help="date YYYY/MM/DD", default=yesterday.strftime('%Y/%m/%d')) 
args = parser.parse_args()
if args.date:
    print(args.date)


#------------#
# 備忘録
#------------#
# ディレクトリ一覧取得
#def listup_dirs(bucket='', prefix=''):
#    dirs = list()
#    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter='/')
#    for content in response.get('CommonPrefixes'):
#        dir = re.sub('^' + prefix, '', content.get('Prefix'))
#        dirs.append(dir)
#    return dirs

 #   with open('stdout.csv', 'w') as out_file:
 #       writer = csv.writer(out_file)
 #       writer.writerow(('USER', 'PID', '%CPU', '%MEM', 'VSZ', 'RSS', 'TT', 'STAT', 'STARTED', 'TIME' 'COMMAND'))
 #       writer.writerows(lines)


# まるっとコピーして、Outputフォルダに配置
#             shutil.copytree('./Template', './Output/Template')
# Templateフォルダ名の変更
#             os.rename('./Output/Template', './Output/' +file) 
# print(len(columns)) # カラムが何行あるか計算してくれる」

#boto3
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html
#    with open('FILE_NAME', 'wb') as f:
#        s3.download_fileobj('BUCKET_NAME', 'OBJECT_NAME', f)


#データの冒頭5行を取得
#df_commands.head()

#データの末尾5行を取得
#df_commands.tail()

#データの型の確認
#df_commands.info()

#------------#
# コマンドメモ
#------------#
# saml2aws login でログインする → onelgin pw入力 → python S3.py でスクリプト実行する
# saml2aws login --skip-prompt -a csirt
# aws s3 ls でちゃんと入れているか確認する
# aws s3 ls s3://freee-cylance-upload/
# 2こ上の階層に移動する：cd ..
# unzip
# 現在のフォルダにコピーする（aws s3 cp  s3://freee-cylance-upload/process_list/yoshizawa-risa.local_85AED71282BE4FAE8D5A39FDE4AFB57B.zip .）
# diff FILE_NAME ~/Downloads/DenySSH.csv 

# S3に所定のフォルダを作るプログラムが必要な気がする。


#0.S3の初期設定
s3 = boto3.client('s3')
bucket = "freee-cylance-upload"

# ファイル一覧取得
def listup_objects(bucket='', prefix=''):
    next_token = ''
    objects = list()
    while True:
        if next_token == '':
            response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix) #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2
        else:
            response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, ContinuationToken=next_token)
        if 'Contents' in response:
            contents = response['Contents']
            for content in contents:
                relative_prefix = re.sub('^' + prefix, '', content['Key'])
                objects.append(relative_prefix)
        if 'NextContinuationToken' in response:
            next_token = response['NextContinuationToken']
        else:
            break
    return objects

#1.s3 bucket name prefix (ファイル名を問い合わせる)(prefixとはディレクトリのこと)
#2.filenamelist を取得する
files = listup_objects(bucket=bucket, prefix=args.date) #日付変える
print(files)

#3.ファイルをダウンロードして保存する
commands = []
users = {}

totals = []
for file in files:
    print("filename...{}".format(file))
    if re.search('\.zip$', file) is None:
        continue
    s3.download_file(bucket, args.date+file, "./Process/FILE_NAME.zip") #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file
    print("download...{}".format(file))
    person_name = file.split('_')[0].strip('/')
    print(person_name)

#4.Zipファイル解凍する
    os.chdir('./Process')
    with ZipFile("./FILE_NAME.zip") as existing_zip:
        existing_zip.extractall('') # 展開されるディレクトリのパスを指定する。省略するとカレントディレクトリに解凍される。

#5.sudo out の pc aws の process name など出力
    with open('./1/stdout', 'r') as in_file: # 行を分割する
        lines = in_file.read().splitlines()
        counts = {}
        with open('./Output/' + person_name +'.txt', 'w') as f: # .txt に書き込み
#   lines = (line.split(" ") 
            for line in lines:
#        print("{}".format(line)) #("{}\n".format(line))
                columns = line.split()
                if len(columns) > 10:  # 10以下なら
                    del(columns[0:10]) # 0から10を削除する
                    line = ' '.join(columns) # colimsからlineに変える
                    command = re.split(' -', line)[0] # ( -) を取り除くやつ追加する
                    f.write("{},{}\n".format(person_name, command))
                    commands.append({"Name":person_name, "Command":command})
                    if counts.get(command) == None:
                        counts[command] = 0
                    counts[command] += 1
                    #l_nested = [{'name': 'Alice', 'age': 25, 'id': {'x': 2, 'y': 8}},
                    #{'name': 'Bob', 'id': {'x': 10, 'y': 4}}]
                    #if counts.get(command) == None:
                    #    counts[command] = {}
                    #if counts[command].get(person_name) == None:
                    #   counts[command][person_name] = 0
                    #counts[command][person_name] += 1

                    #if counts.get(command):
                    #    counts[command]+= 1
                    #else:
                    #    counts[command]= 1
                    #if users.get(command)== None:
                    #    users[command]= []
                    #users[command].append(person_name)
                #    print(command)
        totals.append({"Name":person_name,"Command":counts})

pd.set_option('display.max_columns', 10)
print(pd.DataFrame(totals))
print(pd.io.json.json_normalize(totals))

# processごとのCOUNT
df_commands = pd.DataFrame(commands)
df_commands.to_csv('./commands.csv', header = True)
#df_totals = pd.DataFrame(totals, index=['i',])
#print(df_totals.describe())

# processごとのCOUNT
# df_users = pd.DataFrame(users, index=['i',])
# print(df_users.describe())

#------------#
#７.集計・分類
#------------#
#df_commands.pivot_table("Command",     #集計する変数の指定
#    aggfunc="sum",  # 集計の仕方の指定
#    fill_value=0,   # 該当する値がない場合の埋め値の指定
    #rows="class",     # 行方向に残す変数の指定
#    columns="Command")   #列方向に展開する変数の指定



#------------#
#7.ダウンロードしたファイル削除
#------------#
# ダウンロードしたファイルを保存するためのフォルダパ スを指定する 
#path = 'FILE_NAME'
# ダウンロードした、ファイルを削除する
#os.remove(path) 
# ダウンロードした、ファイルごとディレクトリを削除する
#shutil.rmtree("1") 

# 同じフォルダ作成する
# os.makedirs(path, exist_ok=True) 
# ディレクトリの存在有無を確認
# print(os.path.isdir(path))

 # loop 終わり

#------------#
#8.結果をCSVで出力（未来的にはElasticsearchで表示させたい）
#------------#
# csvで出力
# XXXXXXX.to_csv('/Users/ito-tomoyo/Desktop/get_process.csv', header = True)
# print(result)