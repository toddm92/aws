### AWS CloudFormation Templates

<ol>
  <li> autoscale-healthyhost-template.json
  <br> CloudWatch and AutoScaling work together to monitor ELB/instances and maintain the total number of desired instances in the pool.</br>
  <p>
  <li> bastion-template.json
  <br> Bastion host on-demand. Launch a bastion (jump host) into a public subnet to access your VPC via SSH.  Terminate the server when unused. </br>
  <p>
  <li> cloudwatch-iam-alarms-template.json
  <br> Creates CloudTrail IAM API activity alarms for CloudWatch logs. </br>
  <p>
  <li> elasticache-template.json
  <br> Creates an ElastiCache cluster in a VPC. </br>
  <p>
  <li> elb-template.json
  <br> Secure public facing SSL ELB template.  Create and manage your SSL cipher policy. </br> 
  <p>
  <li> iam-poweruser-template.json
  <br> Creates an IAM "power user" group and inline policy. </br>
  <p>
  <li> nat-instance-template.json
  <br> Deploys a NAT instance with enhanced network capabilities into a public subnet. <br>
  <p>
  <li> vpc-beanstalk-template.json
  <br> Creates a VPC with four subnets in two availability zones. Launches an Elastic Beanstalk environment. </br>
  <p>
  <li> vpc-elasticache-template.json
  <br> Creates a VPC with four subnets in two availability zones. Calls the elasticache-template.json nested stack. </br>
  <p>
  <li> vpc-wNAToption-template.json

</ol>
