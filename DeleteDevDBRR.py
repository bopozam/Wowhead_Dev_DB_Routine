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
BeforeToday = datetime.datetime.now() - datetime.timedelta(days=1)
Yesterday = datetime.datetime.now() - 60*60*24

if fileCreation < twodays_ago:
    print "File is more than two days old"

def delete():
    db_identifier = 'wowhead-mysql-staging-%s' %BeforeToday.strftime("%y-%m-%d")
    rds = boto3.client('rds', region_name='us-east-1')
    instances = rds.get_all_dbinstances.all()

    try:
	for instance in rds.get_all_dbinstances():
		print instance.id	#Prints all existing instances#

	if db_identifier < Yesterday;
		print db_identifier "is older"
        ###rds.delete_db_instance(DBInstanceIdentifier='wowhead-mysql-staging-18-05-30', SkipFinalSnapshot=True)
        print 'Deleting RDS Read Replica instance with ID: %s' % db_identifier
    except botocore.exceptions.ClientError as e:
        if 'DBInstanceAlreadyExists' in e.message:
            print 'DB instance %s exists already, continuing to poll ...' % db_identifier
        elif 'InvalidParameterValue' in e.message:
            print 'DB instance %s does not exist, continuing to poll ...' % db_identifier
        else:
            raise

if __name__ == '__delete__':
    delete()

