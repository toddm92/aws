#!/bin/bash
#
# Checks CloudTrail status in all regions 
# Requires:
#  * the aws-cli 
#  * a valid profile in ~/.aws/config or ${AWS_CONFIG_FILE}

# Usage statement
#
usage ()
{
  echo " Checks CloudTrail status in all regions."
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
REGIONS=("us-east-1" "eu-west-1" "ap-northeast-1" "us-west-1" "us-west-2" "ap-southeast-1" "ap-southeast-2" "sa-east-1") 
PROFILE=$2

# Test for the aws-cli
#
which aws > /dev/null 2>&1
check "the aws-cli commands"

# Test the profile
#
aws ec2 describe-regions --profile $PROFILE > /dev/null 2>&1
check "profile $PROFILE"

# Check each region..
# main loop
#
for rg in ${REGIONS[@]}; do

  status=False
  printf "\nChecking $rg...\n"
  name=`aws cloudtrail describe-trails --profile $PROFILE --region $rg | grep \"Name\": | awk -F': "' '{print $2}' | sed s/\",//`

  if [ "$name" != "" ]; then
    printf "CloudTrail Name: $name\n"
    logging=`aws cloudtrail get-trail-status --name $name --profile $PROFILE --region $rg | grep IsLogging | awk '{print $2}' | sed s/,//`

    if [ $logging == "true" ]; then
      status=True
    fi
  fi

  printf "Enabled: $status\n"
done
#
# end main loop

echo ""
echo "Happy trails!"
exit 0
