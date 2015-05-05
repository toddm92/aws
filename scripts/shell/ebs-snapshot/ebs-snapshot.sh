#!/bin/bash
#
# Automated EBS Volume Snapshots
#
# This script will automatically create a snapshot of EBS volumes mathcing
# a TAG key/value pair. It will look for snapshots older than a retention
# period/date and remove them.
#
# Requirements:
#
#  * the awscli  (`sudo pip install awscli`)
#  * a valid profile in ~/.aws/config or ${AWS_CONFIG_FILE}
#  * MacOS `date` command/format
#
# Other things to do/try:
#
#  * schedule and run from Data Pipeline with an ec2 Role policy
#  * modify the script to handle/use the `date` command from other linux flavors
#

##
#
# snapshot retention period
#
RETENTION=7
#
# EBS volume tag key/value pair
#
KEY=Autosnap
VALUE=True
#
# Today's date
#
TODAY=`date "+%Y-%m-%d"`
#
# Defualt region
#
DREGION=us-west-2
#
##

# Usage statement
#
usage ()
{
  echo " Create automated EBS volume snapshots."
  echo " >> Usage: $0 --profile <profile_name> [ --region <AWS_region> ]"
  echo " >> --"
  echo " >> Default region: $DREGION"
  exit 1
}

check ()
{
if [ $? -ne 0 ]; then
  echo " Error: Couldn't find $1. Please check."
  exit 1
fi
}

# Find and assign our arguments
#
while [ $# -ne 0 ]; do
  case $1 in
    "--profile")
      shift; PROFILE=$1
      ;; 
    "--region")
      shift; REGION=$1
      ;; 
    *)
      shift
      ;;
  esac
done

if [ "$PROFILE" == "" ]; then
  usage
fi
if [ "$REGION" == "" ]; then
  REGION=$DREGION
fi

# Test for aws-cli installation
#
which aws > /dev/null 2>&1
check "the aws-cli commands"

# Test the profile
#
aws ec2 describe-regions --profile $PROFILE > /dev/null 2>&1
check "profile $PROFILE"

# Test the region
#
aws ec2 describe-availability-zones --region $REGION --profile $PROFILE > /dev/null 2>&1
check "region $REGION"

# Grab our EBS volumes (filter based on tag key/value pair)
#
declare -a volumes=(`aws ec2 describe-volumes --profile $PROFILE --region $REGION --output json --filters Name=tag:$KEY,Values=$VALUE --query Volumes[*].[VolumeId] | grep vol- | awk -F\" '{print $2}'`)

if [ ${#volumes[@]} -eq 0 ]; then
  echo "No volumes qualify for a snapshot."
else
  # Create a snapshot for each EBS volume
  #
  for vol in ${volumes[@]}; do
    echo "Creating snapshot for EBS volume, $vol..."
    aws ec2 create-snapshot --volume-id $vol --description "Automated snapshot" --profile $PROFILE --region $REGION
    echo ""
  done

fi

# Find and remove snapshots older than our retention period
#
declare -a snapshots=(`aws ec2 describe-snapshots --profile $PROFILE --region $REGION --output json --query Snapshots[*].[SnapshotId,StartTime] --filters "Name=status,Values=completed" "Name=description,Values=\"Automated snapshot\"" | grep -A1 snap | awk -F\" '{print $2}'`)

p_no=0  # position in the array
c_no=0  # loop counter

while [ ${#snapshots[@]} -gt $c_no ]; do
    
  snapid=${snapshots[$p_no]}
  let "p_no++"
  created=${snapshots[$p_no]}
  let "p_no++"
  date=`echo $created | sed 's/T/ /' | awk '{print $1}'`

  if [ $(((`date -jf %Y-%m-%d $TODAY +%s` - `date -jf %Y-%m-%d $date +%s`)/86400)) -ge $RETENTION ]; then
    aws ec2 delete-snapshot --snapshot-id $snapid --profile $PROFILE --region $REGION
    echo "$snapid has been deleted."
  ##else
  ##  echo "$snapid has been spared."  # for testing purposes
  fi

  c_no=$[c_no + 2]
done
#
exit 0
