#!/usr/bin/env python3
# coding: UTF-8

import csv
import os
import pprint
import pandas as pd
import re
import sys
import math


with open('/Users/ito-tomoyo/Desktop/ExceptionList.csv',  newline='') as f:
    dataReader = csv.reader(f)
    for row in dataReader:
        pprint