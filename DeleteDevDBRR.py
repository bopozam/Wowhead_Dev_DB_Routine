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

def all_rds_instances(region, page_size=20):
    """
    Gets all the RDS instances in a generator (lazy iterator) so you can implement it as:
    `for instance in all_rds_instances(region):`

    page_size [explain what this does] should be bound between 20 and 100.
    """
    marker = ""
    pool = []
    while True:
        for instance in pool:
            yield instance

        if marker is None:
            break
        result = rds.describe_db_instances(Filters=[{"Name": "db-instance-id","Values": ["wowhead-mysql-staging*"]},], MaxRecords=100, Marker=marker)
        marker = result.get("Marker")
        pool = result.get("DBInstances")

for instance in all_rds_instances({"region": "us-east-1"}):
    print instance["Endpoint"]["Address"]

