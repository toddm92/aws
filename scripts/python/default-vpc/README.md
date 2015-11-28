### Remove Those Default VPCs

<p>
This Python script attempts to delete those pesky default VPCs in all regions from your AWS account.
<p>
<b>Warning:</b> 
<br>
Deleting the default VPC is a permanent action.
<br>
You must contact AWS Support if you want to create a new default VPC.

<b>Requirements:</b>
<ul>
 <li> Tested w/ python version 2.7 / boto version 2.38
 <li> Valid AWS API keys
</ul>

<b>Usage:</b>
<p>
<pre>
default-vpc.py
</pre>

<b>Output:</b>
<p>
<pre>
./default-vpc.py
US-EAST-1
vpc-id:  vpc-5ece013b
Removing igw-id:  igw-845fa8e1
Removing sub-id:  subnet-b178188b
Removing sub-id:  subnet-5835381e
Removing sub-id:  subnet-17dcf13f
Removing sub-id:  subnet-267e9e51
Removing rtb-id:  rtb-ef40828a
Removing acl-id:  acl-942cedf1
Removing sgp-id:  sg-f1038894
Removing vpc-id:  vpc-5ece013b
AP-NORTHEAST-1
vpc-id:  vpc-b1ae4ad4
Removing igw-id:  igw-45cada27
Removing sub-id:  subnet-75eafd01
Removing sub-id:  subnet-6f6f5b29
Removing rtb-id:  rtb-cfc126aa
Removing acl-id:  acl-9dbc5bf8
Removing sgp-id:  sg-64f71901
Removing vpc-id:  vpc-b1ae4ad4
EU-WEST-1
vpc-id:  vpc-aef615cb
Removing igw-id:  igw-25504e47
Removing sub-id:  subnet-0a1fe26f
Removing sub-id:  subnet-68fbc52e
Removing sub-id:  subnet-439f8637
Removing rtb-id:  rtb-a950bfcc
Removing acl-id:  acl-97e807f2
Removing sgp-id:  sg-f148b094
Removing vpc-id:  vpc-aef615cb
AP-SOUTHEAST-1
vpc-id:  vpc-a9b257cc
Removing igw-id:  igw-fdbeaf9f
Removing sub-id:  subnet-184d456c
Removing sub-id:  subnet-d5e60db0
Removing vpc-id:  vpc-a9b257cc
AP-SOUTHEAST-2
vpc-id:  vpc-e5719480
Removing igw-id:  igw-12b1a170
Removing sub-id:  subnet-1d937a78
Removing sub-id:  subnet-4ec4d13a
Removing vpc-id:  vpc-e5719480
US-WEST-2
vpc-id:  none
US-WEST-1
vpc-id:  vpc-b08992d2
Removing igw-id:  igw-dce5f5be
Removing sub-id:  subnet-c6436c80
Removing sub-id:  subnet-e2f81487
Removing vpc-id:  vpc-b08992d2
EU-CENTRAL-1
vpc-id:  vpc-068a6d6f
Removing igw-id:  igw-8a7296e3
Removing sub-id:  subnet-2f50b746
Removing sub-id:  subnet-68898f10
Removing vpc-id:  vpc-068a6d6f
SA-EAST-1
vpc-id:  vpc-dc288ab9
Removing igw-id:  igw-d89180ba
Removing sub-id:  subnet-da1bf8bf
Removing sub-id:  subnet-8f4c10c9
Removing sub-id:  subnet-13d4d467
Removing vpc-id:  vpc-dc288ab9
</pre>

<b>To Do:</b>
<ul>
 <li> Add a simple verify check.
</ul>
