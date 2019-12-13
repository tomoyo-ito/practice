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
today = datetime.datetime.now() #- datetime.timedelta(days=1)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", help="date YYYY/MM/DD", default=today.strftime('%Y/%m/%d')) 
args = parser.parse_args()
if args.date:
    print(args.date)


#------------#
# 備忘録
#------------#

#------------#
# コマンドメモ
#------------#
# saml2aws login でログインする → onelgin pw入力 → python S3.py でスクリプト実行する
# saml2aws login --skip-prompt -a csirt
# aws s3 ls でちゃんと入れているか確認する
# aws s3 ls s3://freee-cylance-upload/
# 2こ上の階層に移動する：cd ..
# unzip
# 現在のフォルダにコピーする（aws s3 cp  s3://freee-cylance-upload/browser/2019/12/13/user-name.local_85AED71282BE4FAE8D5A39FDE4AFB57B.zip .）
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
files = listup_objects(bucket=bucket, prefix="browser/" + args.date) #日付変える
print(files)

#3.ファイルをダウンロードして保存する
commands = []
for file in files:
    print("filename...{}".format(file))
    if re.search('\.zip$', file) is None:
        continue
    s3.download_file(bucket, args.date+file, "./browser/FILE_NAME.zip") #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file
    print("download...{}".format(file))
    person_name = file.split('_')[0].strip('/')
    print(person_name)

#4.Zipファイル解凍する
    os.chdir('./browser')
    with ZipFile("./FILE_NAME.zip") as existing_zip:
        existing_zip.extractall('') # 展開されるディレクトリのパスを指定する。省略するとカレントディレクトリに解凍される。

#

# csvに出力する
df_commands = pd.DataFrame(commands)
df_commands.to_csv('./commands.csv', header = True)

