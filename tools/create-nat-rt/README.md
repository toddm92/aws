### Build VPC NAT Route Tables

This Python tool creates one or more route tables in an existing VPC.  Used for sending specific traffic (prefixes) thru a NAT gateway.

**Requirements:**

* Tested w/ python version 2.7 / boto version 2.38
* Valid AWS API keys/ profile

**Usage:**

```
create-nat-rt.py
```

**Output:**

```
./create-nat-rt.py

    This tool creates one or more route tables in a VPC specified by the user.

    It depends on the following information:
      -A valid VPC Id (with an existing igw) - i.e. vpc-d74084b2
      -One or more valid NAT instance Ids - i.e. i-dda86df7
      -A plain text file named "routes.txt" located in the current working directory

       routes.txt should contain one CIDR address per line in the form:
        54.246.41.217/32
        176.34.169.223/32
        54.228.73.202/32
        ...

    Modify the "PROFILE" variable as needed.
    

Enter your vpc-id: vpc-d9b462bc
Enter the NAT instance id for this route table: i-d807c102
Populating routes..
Creating default route..
Route Table name? Nat-AZ-1
New Route Table Id for nat-az-1 : rtb-bccaf3d9

Create another Route Table? y
Enter the NAT instance id for this route table: i-d807d203
Populating routes..
Creating default route..
Route Table name? Nat-AZ-2
New Route Table Id for nat-az-2 : rtb-86caf3e3

Create another Route Table? n
```

New route-table:

```
aws ec2 describe-route-tables --route-table-ids rtb-bccaf3d9 --profile eng --region us-west-2
{
    "RouteTables": [
        {
            "RouteTableId": "rtb-bccaf3d9",
            "VpcId": "vpc-d9b462bc",
            "Routes": [
                {
                    "InstanceOwnerId": "757867887354",
                    "DestinationCidrBlock": "46.137.161.154/32",
                    "InstanceId": "i-d807c102",
                    "NetworkInterfaceId": "eni-d6f1088c",
                    "Origin": "CreateRoute",
                    "State": "active"
                },
                {
                    "InstanceOwnerId": "757867887354",
                    "DestinationCidrBlock": "54.220.89.165/32",
                    "InstanceId": "i-d807c102",
                    "NetworkInterfaceId": "eni-d6f1088c",
                    "Origin": "CreateRoute",
                    "State": "active"
                },
                {
                    "InstanceOwnerId": "757867887354",
                    "DestinationCidrBlock": "54.246.95.224/32",
                    "InstanceId": "i-d807c102",
                    "NetworkInterfaceId": "eni-d6f1088c",
                    "Origin": "CreateRoute",
                    "State": "active"
                },
                { ...
                },
            ],
            "Associations": [],
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "nat-az-1"
                }
            ],
            "PropagatingVgws": []
        }
    ]
}
```
