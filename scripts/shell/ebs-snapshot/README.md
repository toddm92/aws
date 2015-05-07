### Automated EBS Volume Snapshots

<p>
This BASH script will automatically create a snapshot of EBS volumes mathcing
a TAG key/value pair. It will look for snapshots older than a retention
period/date and remove them.

<p>
Can be run from cron once a day, or as desired.

<b>Requirements:</b>
<ul>
 <li> The awscli  (`sudo pip install awscli`)
 <li> A valid profile in ~/.aws/config or ${AWS_CONFIG_FILE} with the appropriate API keys
 <li> MacOS `date` command/format
</ul>

<p>
<b>An EBS volume snapshot will be created if:</b>
<ul>
 <li> The EBS volume is assigned the TAG key/value pair; "Autosnap/True"
</ul>

<b>A Snapshot will be removed only after meeting all of the following:</b>
<ul>
 <li> The snapshot status equals "complete"
 <li> It has the description, "Automated snapshot"
 <li> It's older than the specified retention period/date
</ul>

<b>Usage:</b>
<p>
<code>
ebs-snapshot.sh --profile \<profile_name\> [ --region \<region_name\> ]
</code>

<b>Output:</b>
<pre>
./ebs-snapshot.sh --profile eng --region us-west-2

Creating snapshot for EBS volume, vol-953dcf85...
{
    "Description": "Automated snapshot", 
    "Encrypted": false, 
    "VolumeId": "vol-953dcf85", 
    "State": "pending", 
    "VolumeSize": 10, 
    "Progress": null, 
    "StartTime": "2015-05-04T16:41:01.000Z", 
    "SnapshotId": "snap-e054ffa3", 
    "OwnerId": "XXXXXXXX5893"
}

snap-e29174a0 has been deleted.
snap-35097d70 has been deleted.
snap-b93d55e0 has been deleted.
snap-acaa78f4 has been deleted.
snap-1c212547 has been deleted.
snap-48c1ec12 has been deleted.
</pre>

<b>To Do:</b>
<ul>
 <li> Modify to handle/use the `date` command from other linux flavors (`date -d"$TODAY" +%s` AWS Linux)
</ul>

<hr>

<b> Running from Data Pipeline </b>
<p>
ebs-snapshots-dp.sh

<b>Requirements:</b>
<ul>
 <li> AWS AMI with the awscli installed
 <li> AWS Data Pipeline supported region
</ul>

<b>Usage:</b>
<p>
<code>
ebs-snapshot-dp.sh [ --region \<region_name\> ]
</code>

Pipeline Template (runs once a day)
<pre>
{
  "objects": [
    {
      "id": "DefaultSchedule",
      "name": "Every 1 day",
      "startAt": "FIRST_ACTIVATION_DATE_TIME",
      "type": "Schedule",
      "period": "1 days"
    },
    {
      "id": "ShellCommandActivityObj",
      "scriptUri": "s3://bucket/ebs-snapshot-dp.sh",
      "name": "ShellCommandActivityObj",
      "runsOn": {
        "ref": "EC2ResourceObj"
      },
      "type": "ShellCommandActivity",
      "stage": "true"
    },
    {
      "id": "Default",
      "scheduleType": "cron",
      "failureAndRerunMode": "CASCADE",
      "schedule": {
        "ref": "DefaultSchedule"
      },
      "name": "Default",
      "pipelineLogUri": "s3://bucket/logs/",
      "role": "DataPipelineDefaultRole",
      "resourceRole": "EC2AutosnapRole"
    },
    {
      "terminateAfter": "20 Minutes",
      "instanceType": "t1.micro",
      "id": "EC2ResourceObj",
      "imageId": "ami-ff527ecf",
      "name": "EC2ResourceObj",
      "securityGroupIds": "sg-01234567",
      "subnetId": "subnet-01234567",
      "type": "Ec2Resource"
    }
  ]
}
</pre>

EC2 Resource Role
<pre>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AutosnapPermissions",
            "Action": [
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeRegions",
                "ec2:DescribeSnapshotAttribute",
                "ec2:DescribeSnapshots",
                "ec2:DescribeTags",
                "ec2:DescribeVolumeAttribute",
                "ec2:DescribeVolumeStatus",
                "ec2:DescribeVolumes",
                "datapipeline:*",
                "s3:*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
</pre>
