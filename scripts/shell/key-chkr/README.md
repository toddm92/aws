### Check IAM Users API Key Age

<p>
This BASH script checks the age of the API keys for all your IAM users.
It's good a practice to rotate these keys every 60 to 90 days.

<p>
Can be run from cron once a day, or as desired.


<b>Requirements:</b>
<ul>
 <li> The awscli  (`sudo pip install awscli`)
 <li> A valid profile in ~/.aws/config or ${AWS_CONFIG_FILE} with the appropriate API keys
 <li> MacOS `date` command/format
</ul>

<b>Usage:</b>
<p>
<code>
key-chkr.sh --profile \<profile_name\>
</code>
