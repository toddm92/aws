#!/bin/bash
#
# Automated EBS Volume Snapshots
# (Tested with AWS Data Pipeline)
#
# This script will automatically create a snapshot of EBS volumes mathcing
# a TAG key/value pair. It will look for snapshots older than a retention
# period/date and remove them.
#
# Requirements:
#
#  * the awscli  (`sudo pip install awscli`)
#  * AWS Linux `date` command/format
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
    "--region")
      shift; REGION=$1
      ;; 
    *)
      shift
      ;;
  esac
done

if [ "$REGION" == "" ]; then
  REGION=$DREGION
fi

echo "Region: $REGION"
echo ""

# Test for aws-cli installation
#
which aws > /dev/null 2>&1
check "the aws-cli commands"

# Test the region
#
aws ec2 describe-availability-zones --region $REGION > /dev/null 2>&1
check "region $REGION"

# Grab our EBS volumes (filter based on tag key/value pair)
#
declare -a volumes=(`aws ec2 describe-volumes --region $REGION --output json --filters Name=tag:$KEY,Values=$VALUE --query Volumes[*].[VolumeId] | grep vol- | awk -F\" '{print $2}'`)

if [ ${#volumes[@]} -eq 0 ]; then
  echo "No volumes qualify for a snapshot."
else
  # Create a snapshot for each EBS volume
  #
  for vol in ${volumes[@]}; do
    echo "Creating snapshot for EBS volume, $vol..."
    aws ec2 create-snapshot --volume-id $vol --description "Automated snapshot" --region $REGION
    echo ""
  done

fi

# Find and remove snapshots older than our retention period
#
declare -a snapshots=(`aws ec2 describe-snapshots --region $REGION --output json --query Snapshots[*].[SnapshotId,StartTime] --filters "Name=status,Values=completed" "Name=description,Values=\"Automated snapshot\"" | grep -A1 snap | awk -F\" '{print $2}'`)

p_no=0  # position in the array
c_no=0  # loop counter

while [ ${#snapshots[@]} -gt $c_no ]; do
    
  snapid=${snapshots[$p_no]}
  let "p_no++"
  created=${snapshots[$p_no]}
  let "p_no++"
  date=`echo $created | sed 's/T/ /' | awk '{print $1}'`

  if [ $(((`date -d"$TODAY" +%s` - `date -d"$date" +%s`)/86400)) -ge $RETENTION ]; then
    aws ec2 delete-snapshot --snapshot-id $snapid --region $REGION
    echo "$snapid has been deleted."
  fi

  c_no=$[c_no + 2]
done
#
exit 0
