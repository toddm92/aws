#!/bin/bash
#
# Build a Route 53 Health Check security group containing AWS health check CIDRs
# Requires:
#  * the aws-cli 
#  * a valid profile in ~/.aws/config or ${AWS_CONFIG_FILE}

# Usage statement
#
usage ()
{
  echo " Build a Route 53 Health Check security group in your VPC."
  echo " >> Usage: $0 --profile <profile_name>"
  exit 1
}

check ()
{
if [ $? -ne 0 ]; then
  echo " Error: Couldn't find $1. Please check."
  exit 1
fi
}

# Test for args
#
if [[ $# -ne 2 || $1 != "--profile" ]] ; then
  usage 
fi

# Our variables
#
NAME=route53-healthchk
DESC=Route-53-health-check-security-group
PORT=5300
PROFILE=$2

# Test for the aws-cli
#
which aws > /dev/null 2>&1
check "the aws-cli commands"

# Test the profile
#
aws ec2 describe-regions --profile $PROFILE > /dev/null 2>&1
check "profile $PROFILE"

# Get the VPC-Id
# 
echo -n "Enter your VPC-Id: "
 read VPCId

# Test for valid VPC-Id
#
aws ec2 describe-vpcs --vpc-ids $VPCId --profile $PROFILE > /dev/null 2>&1
check "VPC-Id $VPCId"

# Grab the AWS health check IP CIDRs
#
R53CIDRS=`curl https://ip-ranges.amazonaws.com/ip-ranges.json 2> /dev/null | grep -B2 ROUTE53_HEALTHCHECKS | grep prefix | awk -F\" '{print $4}'`

# Create our security group and record the Id
#
echo -n "Creating R53 health check security group "

aws ec2 create-security-group --group-name $NAME --description $DESC --vpc-id $VPCId --profile $PROFILE > /tmp/sg-id.$$
SGId=`cat /tmp/sg-id.$$ | grep GroupId | awk -F': "' '{print $2}' | sed -e s/\"//`

# Populate the security group
#
for cidr in ${R53CIDRS}; do
  aws ec2 authorize-security-group-ingress --group-id $SGId --protocol tcp --port $PORT --cidr $cidr --profile $PROFILE
  echo -n "."
done

# Tag it
#
aws ec2 create-tags --resources $SGId --tags Key=Name,Value=$NAME --profile $PROFILE

echo -n " done!"
echo ""
echo "Security group Id: $SGId"

# Clean up
#
rm -f /tmp/sg-id.$$

exit 0
