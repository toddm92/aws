#!/bin/bash
#
# Checks CloudTrail status in all regions 
#
# added option (-d) to delete trails - TM
#
# Requires:
#
#  * the aws-cli 
#  * a valid profile in ~/.aws/config or ${AWS_CONFIG_FILE}

# Usage statement
#
usage ()
{
  echo ""
  echo " Checks CloudTrail status in all regions."
  echo " >> Usage: $0 -p <profile_name> [ -d ]"
  echo ""
  echo " >>  -p  : profile name (in ~/.aws/config)"
  echo " >>  -d  : (optional) delete trails"
  echo ""
  exit 1
}

check ()
{
if [ $? -ne 0 ]; then
  echo " Error: Couldn't find $1. Please check."
  exit 1
fi
}

delete=0

while getopts "p:dh" opt; do
  case $opt in
    p)
      PROFILE=$OPTARG
      ;;
    d)
      delete=1
      ;;
    [h?])
      usage
      exit
      ;;
  esac
done

# Region variable
#
REGIONS=("us-east-1" "eu-west-1" "ap-northeast-1" "us-west-1" "us-west-2" "ap-southeast-1" "ap-southeast-2" "sa-east-1" "eu-central-1")

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
  name=`aws cloudtrail describe-trails --profile $PROFILE --region $rg --output json | grep \"Name\": | awk -F\" '{print $4}'`

  if [ "$name" != "" ]; then
    printf "CloudTrail Name: $name\n"
    logging=`aws cloudtrail get-trail-status --name $name --profile $PROFILE --region $rg --output json | grep IsLogging | awk '{print $2}' | sed s/,//`

    if [ $logging == "true" ]; then
      status=True
    fi
  fi

  printf "Enabled: $status\n"

  if [[ $delete -eq 1 ]] && [[ "$name" != "" ]]; then
    printf ">> Deleting trail $name.\n"
    aws cloudtrail delete-trail --name $name --profile $PROFILE --region $rg
  fi

done
#
# end main loop

echo ""
echo "Happy trails!"
exit 0
