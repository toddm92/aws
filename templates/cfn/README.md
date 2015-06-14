### AWS CloudFormation Templates

<ol>
  <li><b> autoscale-healthyhost-template.json </b>
  <br> CloudWatch and AutoScaling work together to monitor ELB/instances and maintain the total number of desired instances in the pool.</br>
  <p>
  <li><b> bastion-template.json </b>
  <br> Bastion host on-demand. Launch a bastion (jump host) into a public subnet to access your VPC via SSH.  Terminate the server when unused. </br>
  <p>
  <li><b> cloudwatch-iam-alarms-template.json </b>
  <br> Creates CloudTrail IAM API activity alarms for CloudWatch logs. </br>
  <p>
  <li><b> elasticache-template.json </b>
  <br> Creates an ElastiCache cluster in a VPC. </br>
  <p>
  <li><b> elb-template.json </b>
  <br> Secure public facing SSL ELB template.  Create and manage your SSL cipher policy. </br> 
  <p>
  <li><b> iam-poweruser-template.json </b>
  <br> Creates an IAM "power user" group and inline policy. </br>
  <p>
  <li><b> nat-instance-template.json </b>
  <br> Deploys a NAT instance with enhanced network capabilities into a public subnet. <br>
  <p>
  <li><b> vpc-beanstalk-template.json </b>
  <br> Creates a VPC with four subnets in two availability zones. Launches an Elastic Beanstalk environment. </br>
  <p>
  <li><b> vpc-elasticache-template.json </b>
  <br> Creates a VPC with four subnets in two availability zones. Calls the elasticache-template.json nested stack. </br>
  <p>
  <li><b> vpc-wNAToption-template.json </b>
  <br> VPC architecture template. Creates a VPC in 1-to-3 availability-zones, 1-to-6 subnets with optional NAT instances in each public subnet/AZ. </br>

</ol>
