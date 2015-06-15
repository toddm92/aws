### Create Trails

This Python script will enable CloudTrail in all regions for an AWS account.

It does the following:
<ol>
  <li> Creates a new SNS topic.
  <li> Assigns the appropriate CloudTrail permissions to the new SNS topic.
  <li> Creates a new trail in each region and enables logging.
  <li> Subscribes the SNS topic to an existing SQS queue (for the SplunkAppForAWS app).
</ol>

<b>Requirements:</b>
<ul>
 <li> Tested w/ python version 2.7 / boto version 2.34
 <li> Valid AWS API keys
</ul>

<b> Usage: </b>

<pre>
  create-trail.py -n &lt;client-name&gt; -k &lt;key&gt; -s &lt;secret&gt;

    -n &lt;client-name&gt; : client or service name
    -k &lt;key&gt;         : aws access key id
    -s &lt;secret&gt;      : aws secret access key

   == CloudOps central account naming convention ==
    * S3 bucket: "&lt;client-name&gt;-central-cloudtrail-logs"
    * SQS queue: "&lt;client-name&gt;-central-cloudtrail-queue"
</pre>
