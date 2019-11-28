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

# ディレクトリ一覧取得
#def listup_dirs(bucket='', prefix=''):
#    dirs = list()
#    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter='/')
#    for content in response.get('CommonPrefixes'):
#        dir = re.sub('^' + prefix, '', content.get('Prefix'))
#        dirs.append(dir)
#    return dirs

#1.s3 bucket name prefix (ファイル名を問い合わせる)(prefixとはディレクトリのこと)
#2.filenamelist を取得する
files = listup_objects(bucket=bucket, prefix="2019/11/20") #日付変える
print(files)

#3.ファイルをダウンロードして保存する
for file in files:
    print("download...{}".format(file))
    s3.download_file(bucket, "2019/11/20" +file, "./Process/FILE_NAME") #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file
    print(file)

#boto3
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html
#    with open('FILE_NAME', 'wb') as f:
#        s3.download_fileobj('BUCKET_NAME', 'OBJECT_NAME', f)

#4.Zipファイル解凍する
    with ZipFile("./Process/FILE_NAME") as existing_zip:
# 展開されるディレクトリのパスを指定する。省略するとカレントディレクトリに解凍される。
        existing_zip.extractall('')

# 行を分割する
    with open('./Process/1/stdout', 'r') as in_file:
        lines = in_file.read().splitlines()
#   lines = (line.split(" ") 
        for line in lines:
#        print("{}".format(line)) #("{}\n".format(line))
            columns = line.split()
            if len(columns) > 10:  # print(len(columns)) # カラムが何行あるか計算してくれる
                del(columns[0:10])
# まるっとコピーして、Outputフォルダに配置
                shutil.copytree('./Process/Template', './Process/Output/Template')
# Templateフォルダ名の変更
                os.rename('./Process/Output/Template', './Process/Output/' +file) 
# sample.txt に書き込み
                with open('./Process/Output/Template/sample.txt', 'w') as f:
                    print(" ".join(columns), file=f)


 #   with open('stdout.csv', 'w') as out_file:
 #       writer = csv.writer(out_file)
 #       writer.writerow(('USER', 'PID', '%CPU', '%MEM', 'VSZ', 'RSS', 'TT', 'STAT', 'STARTED', 'TIME' 'COMMAND'))
 #       writer.writerows(lines)

#------------#
#5.sudo out の pc aws の process name など出力
#------------#



#------------#
#6.集計・分類
#------------#




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