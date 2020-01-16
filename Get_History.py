#!/usr/bin/env python3
# coding: UTF-8

import csv
import os
import shutil
import pandas as pd
import re
import sys
import boto3
import glob
import sqlite3
from contextlib import closing
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

# proper
# 初期設定
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

# ディレクトリ作成
os.makedirs('./browser', exist_ok=True) 

#3.ファイルをダウンロードして保存する
commands = []
for file in files:
    print("filename...{}".format(file))
    if re.search('\.zip$', file) is None:
        continue
    path = 'browser/'+args.date+file
    print("download...{}".format(path))
    s3.download_file(bucket, path, "./browser/FILE_NAME.zip") #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file
    person_name = file.split('_')[0].strip('/')
    print(person_name)

#4.Zipファイル解凍する
    os.chdir('./browser')
    with ZipFile("./FILE_NAME.zip") as existing_zip:
        existing_zip.extractall('') # 展開されるディレクトリのパスを指定する。省略するとカレントディレクトリに解凍される。

# 5 条件を満たすパスの一覧を再帰的に取得する（glob）
#    path1 = './1/Chrome/*/History'
#    Chrome = glob.glob(path1)
#    path2 = './1/Safari/*/History.db'
#    Safari = glob.glob(path2)
#    path3 = './1/IE/*/WebCacheV01.dat'
#    IE = glob.glob(path3)

# 指定したディレクトリ内の全てのファイル名を出力
    print(glob.glob('./1/Chrome/*/History'))
    print(glob.glob('./1/Safari/*/History.db'))
    print(glob.glob('./1/IE/*/WebCacheV01.dat'))
 
# DBに接続する。接続先の名前がpath1。
    for p in glob.glob('./1/Safari/*/History.db'):
        print(p)
        dbname = p
# データを取得する
# ここのsqliteを書き換える。時間とタイトルの列を追加する。Idでまーじすることで出力させる
        sql = select datetime(v.visit_time/1000000-11644473600,'unixepoch','localtime') as visit_time, u.url from visits as v left outer join urls as u on v.url = u.id where v.visit_time/1000000-11644473600 >limit 10; 
        with closing(sqlite3.connect(dbname)) as conn:
            c = conn.cursor()
            c.execute(sql)
            result = c.fetchall()
            print(result)
 #SELECT データを取得するカラム名 FROM テーブル WHERE 条件式 ORDER BY カラム名 並び順 LIMIT 取得したい件数;

# URLがわかるテーブル(Safari)
# history_items 

# start tiem と end time と url がわかる(Safari)
# history_tombstones


# コネクタ作成。dbnameの名前を持つDBへ接続する。
#    with closing(sqlite3.connect(dbname)) as conn:
#        c.execute("select * from users")
#        result = c.fetchall()
#        print(result)
# ここから好きなだけクエリを打つ
# cur.execute('create table students(id integer, name text);')
# 処理をコミット
# conn.commit()
# 接続を切断
# conn.close()

# csvに出力する
#df_commands = pd.DataFrame(commands)
#df_commands.to_csv('./commands.csv', header = True)