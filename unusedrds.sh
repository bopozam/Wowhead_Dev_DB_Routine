osname=$( uname )
if [[ $osname == "Darwin" ]]; then
  date="gdate"
else
  date="date"
fi

MYVER="0.1"
MYHOST=$(hostname -s)
MYDATETIME=$($date +%Y%m%d%H%M)
MYDATE=$($date +%Y%m%d)
UTCDATE=$($date -u +%Y-%m-%dT%H:%M:%S)
STARTDATE=$($date -u -d '1 hour ago' "+%Y-%m-%dT%H:%M:%S")
period=3600

echo "end   = $UTCDATE"
echo "start = $STARTDATE"
servers=$(aws rds describe-db-instances --output text --query 'DBInstances[*].{DBInstanceIdentifier:DBInstanceIdentifier,InstanceCreateTime:InstanceCreateTime,DBInstanceStatus:DBInstanceStatus}' | grep available)

if [ "$?" != "0" ]
then
	# STOP Process
	# Future, send email/slack alert
	echo "Cannot connect to AWS. Verify you have the aws cli installed and configured" 1>&2
	exit 1
fi

echo "---------------------------------------------------------------------------------"
#echo "$servers"
IFS=$'\n'       # make newlines the only separator
for j in $servers
do
	server=$(echo "$j" | cut -f1 -d$'\t')
	update=$(echo "$j" | cut -f3 -d$'\t')
	connections=$(aws cloudwatch get-metric-statistics --metric-name DatabaseConnections --start-time $STARTDATE --end-time $UTCDATE --period $period --namespace AWS/RDS --statistics Maximum --dimensions Name=DBInstanceIdentifier,Value=$server --output text --query 'Datapoints[0].{Maximum:Maximum}')
	if [ "$connections" == "0.0" ]
		then
		echo "Server $server has been up since $update"
		echo "There have been $connections maximun connections in the last hour"
		echo "To terminate this instance run one of the following commands:"
		echo "aws rds delete-db-instance --db-instance-identifier $server --final-db-snapshot-identifier ${server}-final-${MYDATE}"
		echo "aws rds delete-db-instance --db-instance-identifier $server --skip-final-snapshot"
		echo "---------------------------------------------------------------------------------"
	fi
done