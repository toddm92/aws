### Security Group Checker

<p>
This Python script checks your AWS security groups in all regions for "open" (i.e. 0.0.0.0/0) statements and reports the results.

<b>Requirements:</b>
<ul>
 <li> Tested w/ python version 2.7 / boto version 2.34
 <li> A valid profile in ~/.aws/config or ${AWS_CONFIG_FILE} with the appropriate API keys
</ul>

<b>Usage:</b>
<p>
<code>
sg-chkr.py --profile \<profile_name\>
</code>

<b>Output:</b>
<p>
<pre>
./sg-chkr.py --profile eng

Region: us-east-1
Number of SGs: 29 

WARNING: Open security group >>> launch-wizard-1 ( sg-6b72f506 )
Proto: tcp 	Ports: 22 	 22 	Source: [0.0.0.0/0] 

WARNING: Open security group >>> launch-wizard-2 ( sg-5ff54632 )
Proto: tcp 	Ports: 0 	 65535 	Source: [0.0.0.0/0] 

WARNING: Open security group >>> launch-wizard-3 ( sg-6b4b230f )
Proto: tcp 	Ports: 22 	 22 	Source: [0.0.0.0/0] 

WARNING: Open security group >>> app-server ( sg-9b505afe )
Proto: tcp 	Ports: 8080 	 8080 	Source: [0.0.0.0/0] 

WARNING: Open security group >>> rds-launch-wizard ( sg-5062e234 )
Proto: tcp 	Ports: 3306 	 3306 	Source: [0.0.0.0/0] 


Region: eu-west-1
Number of SGs: 7 


Region: ap-northeast-1
Number of SGs: 1 


Region: us-west-1
Number of SGs: 1 


Region: us-west-2
Number of SGs: 6 

WARNING: Open security group >>> launch-wizard-1 ( sg-5dfde938 )
Proto: tcp 	Ports: 22 	 22 	Source: [0.0.0.0/0] 

WARNING: Open security group >>> gateway-elb ( sg-85111ae0 )
Proto: tcp 	Ports: 80 	 80 	Source: [0.0.0.0/0] 


Region: ap-southeast-1
Number of SGs: 1 


Region: ap-southeast-2
Number of SGs: 1 


Region: sa-east-1
Number of SGs: 1 


Region: eu-central-1
Number of SGs: 1 
</pre>

<b>To Do:</b>
<ul>
 <li> ...
</ul>
