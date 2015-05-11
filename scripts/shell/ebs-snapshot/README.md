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
</pre>

<b>To Do:</b>
<ul>
 <li> Modify to handle/use the `date` command from other linux flavors
 <li> Add the necessary logic to run from either cmd-line (i.e. --profile) or Data Pipeline.
</ul>

<b>Notes:</b>

AWS Linux Date
<code>
`date -d"$TODAY" +%s`
</code>

EC2 Resource Role Policy (Tested w/ Data Pipeline)
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
