#!/usr/bin/python
import time
import boto3
import botocore
import datetime
import fnmatch
import os
import re

Today = datetime.datetime.now().strftime("%y-%m-%d")
TimeDelta = datetime.timedelta(days=5)
BeforeToday = datetime.datetime.now() - datetime.timedelta(days=1)

Yesterday = Today - 60*60*24
if fileCreation < twodays_ago:
    print "File is more than two days old"

def main():
    db_identifier = 'wowhead-mysql-staging-%s' %BeforeToday.strftime("%y-%m-%d")
    rds = boto3.client('rds', region_name='us-east-1')
    instances = rds.get_all_dbinstances.all()

    try:
	for instance in rds.get_all_dbinstances():
		print instance.id	#Prints all existing instances#
		if instance.id =< db_identifier
			print db_identifier

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


#    running = True
#    while running:
#        response = rds.describe_db_instances(DBInstanceIdentifier=db_identifier)
#
#        db_instances = response['DBInstances']
#        if len(db_instances) != 1:
#            raise Exception('Whoa cowboy! More than one DB instance returned; this should never happen')
#
#        db_instance = db_instances[0]
#
#        status = db_instance['DBInstanceStatus']
#
#        print 'Last DB status: %s' % status
#
#        time.sleep(5)
#        if status == 'available':
#            endpoint = db_instance['Endpoint']
#            host = endpoint['Address']
#            # port = endpoint['Port']
#
#            print 'DB instance ready with host: %s' % host
#            running = False


if __name__ == '__main__':
    main()

