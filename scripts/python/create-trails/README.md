### Create Trails

This python script will enable CloudTrail in all regions for an AWS account.

It does the following:
<ol>
  <li> Creates a new SNS topic.
  <li> Assigns the appropriate CloudTrail permissions to the new SNS topic.
  <li> Creates a new trail in each region and enables logging.
  <li> Subscribes the SNS topic to a SQS queue (for the SplunkAppForAWS app).
</ol>

<b> Usage </b>
