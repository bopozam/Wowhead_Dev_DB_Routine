import time

import boto3
import botocore

import datetime
import fnmatch
import os
import re

Today = datetime.datetime.now().strftime("%y-%m-%d")
Weekly = datetime.timedelta(weeks=1)

def main():
    db_identifier = 'wowhead-mysql-staging-%s' %Today
    rds = boto3.client('rds', region_name='us-east-1')
    try:
        rds.promote_read_replica(DBInstanceIdentifier=db_identifier,)
        print 'Promoting RDS Read Replica instance with ID: %s' % db_identifier
    except botocore.exceptions.ClientError as e:
        if 'InvalidDBInstanceState' in e.message:
            print 'DB Instance %s is not a read replica, continuing to poll ...' % db_identifier
        else:
            raise


    running = True
    while running:
        response = rds.describe_db_instances(DBInstanceIdentifier=db_identifier)

        db_instances = response['DBInstances']
        if len(db_instances) != 1:
            raise Exception('Whoa cowboy! More than one DB instance returned; this should never happen')

        db_instance = db_instances[0]

        status = db_instance['DBInstanceStatus']

        print 'Last DB status: %s' % status

        time.sleep(5)
        if status == 'available':
            endpoint = db_instance['Endpoint']
            host = endpoint['Address']
            # port = endpoint['Port']

            print 'DB instance ready with host: %s' % host
            running = False


if __name__ == '__main__':
    main()

