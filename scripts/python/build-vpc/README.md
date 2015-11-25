### Create a VPC

<p>
This Python script creates a two or three availability-zone VPC in the AWS region of choice.

<b>Requirements:</b>
<ul>
 <li> Tested w/ python version 2.7 / boto version 2.38
 <li> Valid AWS API keys
 <li> The netaddr library --> https://pythonhosted.org/netaddr
</ul>

<b>Usage:</b>
<p>
<pre>
build-vpc.py
</pre>

<b>Arguments</b>
<ul>
 <li> Number of availability-zones (AZs) [ 2 or 3 ]
 <li> Region [ Any valid AWS region ]
 <li> KeyId [ AWS key.id ]
 <li> SecretId [ AWS secret_key.id ]
 <li> VPC CIDR size [ /25, /24, /23, /22 ]
 <li> Owner (for tagging) [ eng, cloudops, etc ]
 <li> Env (for tagging) [ dev, stage, prod, etc ]
</ul>

<b>Output:</b>
<p>
Using the VPC CIDR: 10.64.0.0/23 in 3 AZs
<br>
<pre>
./build-vpc.py
vpc-id:  vpc-d94d63bc      name:  eng-dev-vpc-uw2
sub-id:  subnet-fade8f8d   size:  10.64.0.0/27    zone:  us-west-2a
sub-id:  subnet-989caffd   size:  10.64.0.32/27   zone:  us-west-2b
sub-id:  subnet-9b6c04c2   size:  10.64.0.64/27   zone:  us-west-2c
sub-id:  subnet-e5de8f92   size:  10.64.0.128/25  zone:  us-west-2a
sub-id:  subnet-9b9caffe   size:  10.64.1.0/25    zone:  us-west-2b
sub-id:  subnet-9d6c04c4   size:  10.64.1.128/25  zone:  us-west-2c
</pre>

<b>To Do:</b>
<ul>
 <li> Expand subnet options.
</ul>
