#!/usr/bin/env python
#
# Python Version: 2.7
# Boto Version 2.38
#
# Enable CloudTrail logging in all AWS regions
#

# Must be the first line
from __future__ import print_function

import boto.cloudtrail
import boto.sns
import sys, getopt


def get_regions():
  """ Build a region list """

  reg_list = []
  for reg in boto.cloudtrail.regions():
    if reg.name == 'us-gov-west-1' or reg.name == 'cn-north-1':
      continue
    reg_list.append(reg)

  return reg_list

def abbr_region(region):
  abbr = 'nul'
  if region == 'us-east-1':      abbr = 'ue1'
  if region == 'eu-west-1':      abbr = 'ew1'
  if region == 'ap-northeast-1': abbr = 'an1'
  if region == 'us-west-1':      abbr = 'uw1'
  if region == 'us-west-2':      abbr = 'uw2'
  if region == 'ap-southeast-1': abbr = 'as1'
  if region == 'ap-southeast-2': abbr = 'as2'
  if region == 'eu-central-1':   abbr = 'ec1'
  if region == 'sa-east-1':      abbr = 'se1'

  return abbr

def usage():
    """ Usage statement """

    print("""
  create-trail.py -n <client-name> -k <key> -s <secret>

    -n <client-name> : client or service name
    -k <key>         : aws access key id
    -s <secret>      : aws secret access key
    -h               : print this usage statement

   == CloudOps central account naming convention ==
    * S3 bucket: "<client-name>-central-cloudtrail-logs"
    * SQS queue: "<client-name>-central-cloudtrail-queue"
    """)

    exit(1)

def get_args():
  """ Check the arguments """

  argv = sys.argv[1:]
  name = ''
  key = ''
  secret = ''

  try:
    opts, args = getopt.getopt(argv,'hn:k:s:',['name=','key=','secret='])
  except getopt.GetoptError:
    usage()

  for opt, arg in opts:
    if opt in ('-n', '--name'):     name = arg
    elif opt in ('-k', '--key'):    key = arg
    elif opt in ('-s', '--secret'): secret = arg
    elif opt == '-h':               usage()

  if name == '' or key == '' or secret == '' or len(sys.argv) != 7:
    usage()

  return name, key, secret

def create_topic(snsconn, snstopic, trail, queue):
  """ Create the SNS topic """

  try:
    topic_response = snsconn.create_topic(snstopic)
  except boto.exception.BotoServerError as e:
    print('SNS: ' + e.message)
    exit(1)

  sns_arn = topic_response[u'CreateTopicResponse'][u'CreateTopicResult'][u'TopicArn']
  try:
    snsconn.add_permission(sns_arn, 'CloudTrail', [ 'arn:aws:iam::903692715234:root',
                                                    'arn:aws:iam::859597730677:root',
                                                    'arn:aws:iam::814480443879:root',
                                                    'arn:aws:iam::216624486486:root',
                                                    'arn:aws:iam::086441151436:root',
                                                    'arn:aws:iam::388731089494:root',
                                                    'arn:aws:iam::284668455005:root',
                                                    'arn:aws:iam::113285607260:root',
                                                    'arn:aws:iam::035351147821:root' ], 'Publish')
  except boto.exception.BotoServerError as e:
    print('SNS: ' + e.message)
    exit(1)

  snsconn.subscribe(sns_arn, 'sqs', queue)

def create_trail(ctconn, snstopic, trail, bucket, region):
  """ Create a new trail """

  try:
    ctconn.create_trail(trail, bucket, sns_topic_name=snstopic)
  except Exception as e:
    print('TRAIL: S3 bucket ' + bucket + ' may not exist or have an incorrect policy!')
    #snsconn.delete_topic(sns_arn)
    exit(1)
  else:
    print('Creating trail in ' + region + '..')
    ctconn.start_logging(trail)


def main():
  """ Do the work """

  name, key, secret = get_args()
  regions = get_regions()

  trail = name + '-cloudtrail'
  bucket = name + '-central-cloudtrail-logs'
  queue = 'arn:aws:sqs:us-east-1:578167444557:' + name + '-central-cloudtrail-queue'

  for region in regions:

    ctconn = boto.cloudtrail.connect_to_region(region.name, aws_access_key_id=key, aws_secret_access_key=secret)
    try:
      trail_response = ctconn.describe_trails()
    except boto.exception.BotoServerError as e:
      print(e.message)
      exit(1)
    else:
      if len(trail_response['trailList']):
        print('A trail already exists in the', region.name, 'region.')
        continue

    snsconn = boto.sns.connect_to_region(region.name, aws_access_key_id=key, aws_secret_access_key=secret)

    abbr = abbr_region(region.name); snstopic = trail + '-' + abbr
    create_topic(snsconn, snstopic, trail, queue)
    create_trail(ctconn, snstopic, trail, bucket, region.name)

if __name__ == "__main__":

  main()
