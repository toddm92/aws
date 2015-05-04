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
 <li> Schedule and run from Data Pipeline with an ec2 Role policy
 <li> Modify to handle/use the `date` command from other linux flavors
</ul>
