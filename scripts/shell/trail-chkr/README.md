### Check CloudTrail Status

<p>
This BASH script checks the name and status of CloudTrail in all regions of your AWS account.

<b>Requirements:</b>
<ul>
 <li> The awscli  (`sudo pip install awscli`)
 <li> A valid profile in ~/.aws/config or ${AWS_CONFIG_FILE} with the appropriate API keys
</ul>

<b>Usage:</b>
<p>
<code>
trail-chkr.sh --profile \<profile_name\>
</code>

<b>To Do:</b>
<ul>
 <li> Replace the REGIONS variable with a dynamic array. Build with the `aws ec2 describe-regions` command
</ul>
