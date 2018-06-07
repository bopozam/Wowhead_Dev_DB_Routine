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

def all_rds_instances(config):
    """
    Gets all the RDS instances in a generator (lazy iterator) so you can implement it as:
    `for instance in all_rds_instances(config):`
    """
    marker = ""
    rds = boto3.client('rds', region_name=config["region"])
    pool = []

    # min 20, max 100
    page_size = 20
    while True:
        if len(pool) < 1:
            if marker is None:
                break
            # populate a local pool of instances
            result = rds.describe_db_instances(MaxRecords=page_size, Marker=marker)
            marker = result.get("Marker")
            pool = result.get("DBInstances")

        if len(pool) > 0:
            this_instance = pool.pop()
            yield this_instance


# def delete():
#     rds = boto3.client('rds', region_name='us-east-1')
# 	
#     
#     try:
#     	old_instance = rds.describe_db_instances(DBInstanceIdentifier='wowhead-mysql-staging-'.)
#     	db_instances = old_instance['DBInstances']
#     	db_instance = db_instances[0]
#     	
# 		InstanceCreateTime = db_instance['InstanceCreateTime']
# 		
#         print 'Creating RDS Read Replica instance with ID: %s' % db_identifier
#     except botocore.exceptions.ClientError as e:
#         if 'DBInstanceAlreadyExists' in e.message:
#             print 'DB instance %s exists already, continuing to poll ...' % db_identifier
#         else:
#             raise
# 
# 
#     running = True
#     while running:
#         response = rds.describe_db_instances(DBInstanceIdentifier=db_identifier)
# 
#         db_instances = response['DBInstances']
#         if len(db_instances) != 1:
#             raise Exception('More than one DB instance returned; this should never happen')
# 
#         db_instance = db_instances[0]
# 
#         status = db_instance['DBInstanceStatus']
# 
#         print 'Last DB status: %s' % status
# 
#         time.sleep(5)
#         if status == 'available':
#             endpoint = db_instance['Endpoint']
#             host = endpoint['Address']
#             # port = endpoint['Port']
# 
# #             print 'DB instance ready with host: %s' % host
#             running = False
# 
# 
# if __name__ == '__delete__':
#     delete()
# 
