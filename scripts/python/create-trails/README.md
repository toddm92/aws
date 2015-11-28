### Create Trails

This Python script will enable CloudTrail in all regions for an AWS account.  Design note: Both the CloudTrail S3 bucket and SQS queue should be located in a seperate secured central account.

It does the following:
<ol>
  <li> Creates a new SNS topic.
  <li> Assigns the appropriate CloudTrail permissions to the new SNS topic.
  <li> Creates a new trail in each region and enables logging.
  <li> Subscribes the SNS topic to a SQS queue (for the SplunkAppForAWS app).
</ol>

<b>Requirements:</b>
<ul>
 <li> Tested w/ python version 2.7 / boto version 2.38
 <li> Valid AWS API keys
 <li> An existing S3 bucket with CloudTrail policy
 <li> An existing SQS queue ARN
</ul>

<b>Design:</b>

(![Trails Design](https://s3-us-west-2.amazonaws.com/toddm92/public/diagrams/cloudtrail-design.jpg)

<b> Usage: </b>

<pre>
  create-trail.py -n &lt;client-name&gt; -k &lt;key&gt; -s &lt;secret&gt;

    -n &lt;client-name&gt; : client or service name
    -k &lt;key&gt;         : aws access key id
    -s &lt;secret&gt;      : aws secret access key
    -h               : print this usage statement

   == Naming convention ==
    * S3 bucket: "&lt;client-name&gt;-central-cloudtrail-logs"
    * SQS queue: "&lt;client-name&gt;-central-cloudtrail-queue"
</pre>

<b> Output: </b>

<pre>
./create-trails2.py -n test -k XXXX -s XXXX
Creating trail in us-east-1..
Creating trail in ap-northeast-1..
Creating trail in eu-west-1..
Creating trail in ap-southeast-1..
Creating trail in ap-southeast-2..
A trail already exists in the us-west-2 region.
Creating trail in us-west-1..
Creating trail in eu-central-1..
Creating trail in sa-east-1..
</pre>

<b> To Do: </b>
<ul>
  <li> Clean up work
</ul>
