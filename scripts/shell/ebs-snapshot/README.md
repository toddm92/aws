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

<b>A Snapshot will be removed only after meeting all of the following conditions:</b>
<ul>
 <li> The snapshot was taken from a volume assigned the above TAG key/value pair
 <li> It's status equals "complete"
 <li> Has the description; "Automated snapshot"
 <li> Is older than the specified retention period/date
</ul>

<b>Usage:</b>
<p>
<code>
ebs-snapshot.sh --profile \<profile_name\> [ --region \<region_name\> ]
</code>

<b>To Do:</b>
<ul>
 <li> Schedule and run from Data Pipeline with an ec2 Role policy
 <li> Modify to handle/use the `date` command from other linux flavors
</ul>
