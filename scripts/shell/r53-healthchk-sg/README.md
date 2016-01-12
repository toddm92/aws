### R53 HealthCheck Security Group

This BASH script creates a Route 53 healthcheck VPC security group.  It grabs a list of AWS CIDRs used to perform health checks
on your services (ELBs, EC2 instances, etc.) and builds a security group that only permits these CIDRs.

Moved into its own repo:

https://github.com/toddm92/r53-healthchk-sg
