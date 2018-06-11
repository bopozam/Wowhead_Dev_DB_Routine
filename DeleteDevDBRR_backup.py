#!/usr/bin/python
import time
import boto3
import botocore
import datetime
import fnmatch
import os
import re
import socket
import sys

Today = datetime.datetime.now().strftime('%y-%m-%d')
Weekly = datetime.timedelta(weeks=1)
db_identifier = 'wowhead-mysql-staging-%s' %Today
rds = boto3.client('rds', region_name='us-east-1')
route53 = boto3.client('route53', region_name='us-east-1')
zone_id = '/hostedzone/Z174UMT6MD8IR8'
#boto3.set_stream_logger('botocore')


from boto.rds import connect_to_region
from datetime import datetime, timedelta

try:
	days = int(sys.argv[1])
except IndexError:
	days = 7

delete_time = datetime.utcnow() - timedelta(days=days)

filters = {
	'db-instance-id': 'wowhead-mysql-staging*'
}

print 'Deleting any instances older than {days} days'.format(days=days)

instances = rds.describe_db_instances()

deletion_counter = 0
size_counter = 0

# for db in instances['DBInstances']:
#         print (db['DBInstanceIdentifier'])
# except Exception as error:
# 	print error

for instance in instances:
	print instance
	create_time = datetime.strptime(
		instance.InstanceCreateTime,
		'%y-%m-%d'
	)

	if create_time < delete_time:
		print 'Deleting {id}'.format(id=instance.id)
		deletion_counter = deletion_counter + 1
		size_counter = size_counter + instance.volume_size
		# Just to make sure you're reading!
		instance.delete(dry_run=True)

print 'Deleted {number} instances totalling {size} GB'.format(
	number=deletion_counter,
	size=size_counter
)
