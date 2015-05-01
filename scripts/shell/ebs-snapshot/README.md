### Automated EBS Volume Snapshots

<p>
This script will automatically create a snapshot of EBS volumes mathcing
a TAG key/value pair. It will look for snapshots older than a retention
period/date and remove them.

<p>
Can be run from cron once a day, or as desired.

<p>
<b>EBS volume snapshot creation requirement:</b>
<ul>
 <li> EBS volumes assigned the TAG key/value pair; "Autosnap/True"
</ul>

<b>Snapshot removal requirements:</b>
<ul>
 <li> Snapshots taken from a volume assigned the TAG key/value pair; "Autosnap/True"
 <li> Status equals "complete"
 <li> Has the description TAG; "Automated snapshot"
 <li> Is older than the specified retention period/date
</ul>

<b>To Do:</b>
<ul>
 <li> Schedule and run from Data Pipeline with an ec2 Role policy
 <li> Modify to handle/use the `date` command from other linux flavors
</ul>
