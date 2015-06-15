#!/usr/bin/env python
#
# Python Version: 2.7
#
# Enables CloudTrail logging in all AWS regions
#

# Must be the first line
from __future__ import print_function

import boto.cloudtrail
import boto.sns
import sys, getopt

REGIONS = ( 'us-east-1',  'eu-west-1',  'ap-northeast-1',
            'us-west-1', 'us-west-2', 'ap-southeast-1',
            'ap-southeast-2', 'sa-east-1', 'eu-central-1' )

def abbr_region(region):
    if region == 'us-east-1':
        aregion = 'ue1'
    if region == 'eu-west-1':
        aregion = 'ew1'
    if region == 'ap-northeast-1':
        aregion = 'an1'
    if region == 'us-west-1':
        aregion = 'uw1'
    if region == 'us-west-2':
        aregion = 'uw2'
    if region == 'ap-southeast-1':
        aregion = 'as1'
    if region == 'ap-southeast-2':
        aregion = 'as2'
    if region == 'sa-east-1':
        aregion = 'se1'
    if region == 'eu-central-1':
        aregion = 'ec1'

    return aregion

def usage():
    """Usage Statement"""

    print("""
  create-trail.py -n <client-name> -k <key> -s <secret>

    -n <client-name> : client or service name
    -k <key>         : aws access key id
    -s <secret>      : aws secret access key

   == CloudOps central account naming convention ==
    * S3 bucket: "<client-name>-central-cloudtrail-logs"
    * SQS queue: "<client-name>-central-cloudtrail-queue"
    """)

    exit()

argv = sys.argv[1:]
name = ''
key = ''
secret = ''

# Check our args
#
try:
    opts, args = getopt.getopt(argv,"hn:k:s:",["name=","key=","secret="])
except getopt.GetoptError:
    usage()

for opt, arg in opts:
    if opt in ("-n", "--name"):
        name = arg
    elif opt in ("-k", "--key"):
        key = arg
    elif opt in ("-s", "--secret"):
        secret = arg
    elif opt == "-h":
        usage()

if name == "" or key == "" or secret == "" or len(sys.argv) != 7:
    usage()

# Setup our names
#
trail = name + '-cloudtrail'
bucket = name + '-central-cloudtrail-logs'
queue = 'arn:aws:sqs:us-east-1:578167444557:' + name + '-central-cloudtrail-queue'

#print('Name =', trail)
#print('Bucket =', bucket)
#print('Queue =', queue)

reg_total = len(REGIONS)
reg_no = 0

# (main loop)
#
while reg_total > 0:

    reg_name = REGIONS[reg_no]

    try:
        snsconn = boto.sns.connect_to_region(reg_name, aws_access_key_id=key, aws_secret_access_key=secret)
        ctconn = boto.cloudtrail.connect_to_region(reg_name, aws_access_key_id=key, aws_secret_access_key=secret)
    except:
        print('>> Failed to establish a connection. Please check your key/secret values.')
        exit()

    # Check if trail already exists
    # 
    try:
        trail_response = ctconn.describe_trails()
    except:
        print('>> Something went wrong. Please check your key/secret values.')
        exit()

    if len(trail_response['trailList']):
        print('A trail already exists in the', reg_name, 'region.')

    else:
        # Create our SNS topic
        #
        snstopic = trail + '-' + abbr_region(reg_name)

        try:
            topic_response = snsconn.create_topic(snstopic)
        except:
            print('>> Failed to create SNS topic.')
            exit()
        sns_arn = topic_response[u'CreateTopicResponse'][u'CreateTopicResult'][u'TopicArn']

        snsconn.add_permission(sns_arn, 'CloudTrail', [ 'arn:aws:iam::903692715234:root',
                                                        'arn:aws:iam::859597730677:root',
                                                        'arn:aws:iam::814480443879:root',
                                                        'arn:aws:iam::216624486486:root',
                                                        'arn:aws:iam::086441151436:root',
                                                        'arn:aws:iam::388731089494:root',
                                                        'arn:aws:iam::284668455005:root',
                                                        'arn:aws:iam::113285607260:root',
                                                        'arn:aws:iam::035351147821:root' ], 'Publish')

        # Create our new trail
        #
        print('Creating trail in the', reg_name, 'region...', end = '')

        try:
            ctconn.create_trail(trail, bucket, sns_topic_name=snstopic)
        except:
            print('\n>> Failed to create trail in the', reg_name, 'region. Check the bucket name and make sure it exists.')
            snsconn.delete_topic(sns_arn)
            exit()
        ctconn.start_logging(trail)

        # SQS queue subscription
        #
        try:
            snsconn.subscribe(sns_arn, 'sqs', queue)
        except:
            print('\n>> Pending subscription to the queue', queue, 'failed.')
            ctconn.delete_trail(trail)
            snsconn.delete_topic(sns_arn)
            exit()
        print(' done.')

    reg_no += 1
    reg_total -= 1
#
# (end main loop)
