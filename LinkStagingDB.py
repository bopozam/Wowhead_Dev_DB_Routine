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

def main():
	
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
	    ip_list = []
#	    ais = socket.getaddrinfo(host,0)
	    ais = socket.getaddrinfo(host, None)[0]
            ip_addr = ais[4][0]
            if ais[0] == socket.AF_INET6:
                ip_addr = re.sub(r'^0*', '', ip_addr)
                ip_addr = re.sub(r':0*', ':', ip_addr)
                ip_addr = re.sub(r'::+', '::', ip_addr)
            node = ip_addr
 
            print 'DB instance ready with host: %s' % host
            print 'DB instance ready with IP: %s' % node

## Route 53 ##
	print 'Route53 host ID for mysql.wowhead.com.: %s' % zone_id

	#changeIP = route53.change_resource_record_sets(
	route53.change_resource_record_sets(
		HostedZoneId=zone_id,
		ChangeBatch={
			'Changes': [
				{
					'Action': 'UPSERT',
					'ResourceRecordSet': {
						'Name': 'devdb.mysql.wowhead.com.',
						'Type': 'A',
						'TTL': 900,
						'ResourceRecords': [
							{
								'Value': '%s' % node
							}
						]
					}
				}
			]
		}
	)
	
	print changeIP
	
        running = False


if __name__ == '__main__':
    main()

