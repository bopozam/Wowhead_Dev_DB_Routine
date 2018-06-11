#!/usr/bin/python
import time
import boto3
import botocore
import datetime
import fnmatch
import os
import re
import socket

Today = datetime.datetime.now().strftime('%y-%m-%d')
Weekly = datetime.timedelta(weeks=1)
db_identifier = 'wowhead-mysql-staging-%s' %Today
rds = boto3.client('rds', region_name='us-east-1')
route53 = boto3.client('route53', region_name='us-east-1')
zone_id = '/hostedzone/Z174UMT6MD8IR8'
#boto3.set_stream_logger('botocore')

try:
# get all of the db instances
    dbs = rds.describe_db_instances()
    for db in dbs['DBInstances']:
        print ("%s %s") % (
            db['DBInstanceIdentifier'])
except Exception as error:
	print error
