#!/usr/bin/env python
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
	days = int(sys.argv[1])
except IndexError:
	days = 7

delete_time = datetime.utcnow() - timedelta(days=days)

print 'Deleting any instances older than {days} days'.format(days=days)

deletion_counter = 0

try:
# get all of the db instances
	dbs = rds.describe_db_instances()
	db_instances = dbs['DBInstances']
	db_instance = db_instances[0]
	create_time = db_instance['InstanceCreateTime']

	running = True
    while running:
		for db in dbs['DBInstances']:
			print 'Instance: %s' % db_instance #'was created on: %s' % create_time


		for ct in dbs['DBInstances']:
			create_time = ct['InstanceCreateTime'].strftime('%y-%m-%d')
			instance = ct['DBInstanceIdentifier']

		#if (create_time < delete_time.strftime('%y-%m-%d') and instance == 'wowhead-mysql-staging-*'):
		if create_time < delete_time.strftime('%y-%m-%d') :
			print 'Deleting %s:' % instance


# try:
#     response = rds.delete_db_instance(
#         DBInstanceIdentifier=db,
#         SkipFinalSnapshot=True)
#     print response
# except Exception as error:
#     print error