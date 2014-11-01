#!/bin/bash
#
# Checks the age of active AWS access keys
# Requires:
#  * the aws-cli 
#  * a valid profile in ~/.aws/config or ${AWS_CONFIG_FILE}
#  * MacOS `date` command/format

# Usage statement
#
usage ()
{
  echo " Checks the age of active AWS access keys."
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
#DAYS_OLD=90
PROFILE=$2
TODAY=`date "+%Y-%m-%d"`

# Test for the aws-cli
#
which aws > /dev/null 2>&1
check "the aws-cli commands"

# Test the profile
#
aws ec2 describe-regions --profile $PROFILE > /dev/null 2>&1
check "profile $PROFILE"

# Grab our IAM users
#
declare -a users=(`aws iam list-users --profile $PROFILE | grep UserName | sort | awk -F\" '{print $4}'`)

# (main loop)
#
for u in ${users[@]}; do
  echo "Checking keys for user, $u..."

  # Get the user's key(s) status and creation date for each
  #
  declare -a status=(`aws iam list-access-keys --profile $PROFILE --user-name $u | grep -A1 Status | awk -F\" '{print $4}'`)

  i_key=0  # no. of inactive keys
  a_key=0  # no. of active keys
  s_no=0   # position in the array

  # Check each key in the array
  #
  for s in ${status[@]}; do
    if [ "$s" == "Active" ]; then
      let "s_no++"
      let "a_key++"

      # Get active key creation date and compare it to today's date
      #
      kcd=`echo ${status[$s_no]} | sed 's/T/ /' | awk '{print $1}'`
      echo " * Active key $a_key is $(((`date -jf %Y-%m-%d $TODAY +%s` - `date -jf %Y-%m-%d $kcd +%s`)/86400)) days old"

      elif [ "$s" == "Inactive" ]; then
        let "i_key++"
        let "s_no++"
      else
        let "s_no++"
    fi
  done

  # Report non-active key status
  #
  if [ $i_key != 0 ]; then
    if [ $i_key = 1 ]; then
      echo " * $i_key inactive key"
    else
      echo " * $i_key inactive keys"
    fi
  elif [ $a_key = 0 ]; then
    echo " * No access keys"
  fi

echo ""
done

#
# (end main loop)
exit 0
