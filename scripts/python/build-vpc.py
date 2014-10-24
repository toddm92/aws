#!/usr/bin/env python
#
# Python Version: 2.7
# Build a VPC

# Must be the first line
from __future__ import print_function

import sys
import boto.vpc
import boto.ec2

# Default variables
REGIONS = ( 'us-east-1', 'eu-west-1', 'ap-northeast-1', 'us-west-1', 'us-west-2', 'ap-southeast-1', 'ap-southeast-2', 'sa-east-1', 'eu-central-1' )
THREEAZREGIONS = ( 'us-east-1', 'eu-west-1', 'us-west-2' )

VPC_CIDR =  '10.10.0.0/20'
SUBNETS = ( '10.10.0.0/24',  '10.10.1.0/24',  '10.10.2.0/24',
            '10.10.3.0/24',  '10.10.4.0/24',  '10.10.5.0/24',
            '10.10.6.0/24',  '10.10.7.0/24',  '10.10.8.0/24' )

def abbr_region(region):
    if region == 'us-east-1':
        aregion = 'ue1'
    if region == 'eu-west-1':
        aregion = 'ew1'
    if region == 'ap-northeast-1':
        aregion = 'an1'
    if region == 'us-west-1':
        aregion = 'uw1'
    if region == 'us-west-2':
        aregion = 'uw2'
    if region == 'ap-southeast-1':
        aregion = 'as1'
    if region == 'ap-southeast-2':
        aregion = 'as2'
    if region == 'eu-central-1':
        aregion = 'ec1'

    return aregion
   
def usage1():
    print("""
        Creates a VPC in 1-3 availability-zones.  You should create at a minimum, 1 Subnet per AZ.
        At each Subnet tier, a new route-table with a default route and a new NACL is created.

    """)

def usage2():
    print("\t* use: --profile <profile_name>")
    print("\t  profile_name from your ~/.boto (~/.aws/config)\n\n")

    exit()

def tag_it(resource_id, resource):
    """Tag Resources"""

    name = owner + "-" + env + "-" + resource + "-" + abbr_reg
    conn.create_tags(resource_id, { 'Name' : name }, dry_run=False)

def syntax_error():
    print("Something went wrong.  Please check your syntax..")

# Check for arguments
#
args = len(sys.argv)
if args != 3:
    usage1()
    usage2()

if '--profile' in (str(sys.argv[1]).lower()):
    profile = str(sys.argv[2]).lower()
else:
    usage2()

# Get owner/service and env info
#
owner = ""
while len(owner) == 0:
    print("Enter the Owner or Service (i.e. cloudops): ", end = "")
    owner = raw_input().lower()
    owner = owner.replace(' ', '')

env = ""
while len(env) == 0:
    print("Enter the Environment (i.e. prod, stage, dev): ", end = "")
    env = raw_input().lower()
    env = env.replace(' ', '')

# Get the region
#
region = 'blah'
while region not in (REGIONS):
    region = raw_input("Enter the AWS region: ")

# Abbr region
abbr_reg = abbr_region(region)

myregion = boto.ec2.get_region(region_name=region)
try:
    conn = boto.vpc.VPCConnection(profile_name=profile, region=myregion)
except boto.provider.ProfileNotFoundError:
    print("\nERROR: Please check your profile_name in ~/.boto and try again..\n")
    usage2()

# Get number of AZs
#
if region in (THREEAZREGIONS):
    az_max = 3
else:
    az_max = 2

az_no = 0
while az_no > int(az_max) or int(az_no) == 0:
    try:
        print("\nEnter up to", az_max, "AZs..")
        az_no = raw_input("Enter the number of availability-zones: ")
        az_no = int(az_no)
    except ValueError:
        print("Please enter a number..")

# Get number of Subnets
#
sub_no = 0
sub_max = int(az_no) * 3
while sub_no > int(sub_max) or int(sub_no) == 0: 
    try:
        print("\nEnter the total number of subnets desired, not to exceed", sub_max, "subnets.." )
        sub_no = raw_input("Total number of subnets: ")
        sub_no = int(sub_no)
    except ValueError:
        print("Please enter a number..")

# Create the VPC
#
running = True
while running:
    try:
        print("\nEnter your VPC CIDR block [", VPC_CIDR, "]: ", end = "")
        cidr = str(raw_input())
        if cidr == "":
            cidr = VPC_CIDR

        print("Creating VPC..")
        vpc = conn.create_vpc(cidr, instance_tenancy='default')
        conn.modify_vpc_attribute(vpc.id, enable_dns_support=True)
        conn.modify_vpc_attribute(vpc.id, enable_dns_hostnames=True)
        running = False
    except boto.exception.EC2ResponseError:
        syntax_error()
tag_it(vpc.id, "vpc")

# Create an igw
#
print("Creating igw..")
igw = conn.create_internet_gateway()
conn.attach_internet_gateway(igw.id, vpc.id)
tag_it(igw.id, "igw")

# Counters and lists needed for the main loop
#
all_azs = conn.get_all_zones()
az_total = 0
az_count = 1
az_list = [ ]
sub_total = 0
sub_list = [ ]
tag_tier = 'public'
tag_tier_no = 1
tag_sub_no = 1

# main loop
#
while sub_no != 0:

    # Get the zones
    running = True
    while running:
        try:
            print("")
            if az_total < az_no:
                new_az_name = str(all_azs[az_total])
                new_az_name = new_az_name[5:]
                print("Enter the zone name for AZ-" + str(az_count) + " [", new_az_name, "]: ", end = "")
                az_name = raw_input()
                if az_name == "":
                    az_name = new_az_name

                conn.get_all_zones(zones=az_name)
                az_list.append(az_name)
                az_total += 1
                az_count += 1
            running = False
        except boto.exception.EC2ResponseError:
            syntax_error()

    # Create our subnets
    running = True
    while running:
        try:
            print("Enter the CIDR for " + tag_tier + " subnet in zone,", az_list[len(sub_list)], "[", SUBNETS[sub_total], "]: ", end = "")
            subnet_cidr = raw_input()
            if subnet_cidr == "":
                subnet_cidr = SUBNETS[sub_total]

            subnet_cidr = str(subnet_cidr)
            subnet = conn.create_subnet(vpc.id, subnet_cidr, availability_zone=az_list[len(sub_list)])
            tag_it(subnet.id, tag_tier + str(tag_tier_no) + "-subnet" + str(tag_sub_no))
            sub_list.append(subnet.id)
            sub_total += 1
            sub_no -= 1
            tag_sub_no += 1
            running = False
        except boto.exception.EC2ResponseError:
            syntax_error()
            
    # Create our route tables and NACLs
    if az_no == len(sub_list):
        print("\nCreating route-table..")
        route_table = conn.create_route_table(vpc.id)
        conn.create_route(route_table.id, '0.0.0.0/0', igw.id)
        tag_it(route_table.id, tag_tier + str(tag_tier_no) + "-rtb")

        print("Creating NACL..")
        network_acl = conn.create_network_acl(vpc.id)
        tag_it(network_acl.id, tag_tier + str(tag_tier_no) + "-nacl")
        if tag_tier == 'private':
            # Ingress
            conn.create_network_acl_entry(network_acl.id, 100, -1, 'allow', cidr, egress=False)
            conn.create_network_acl_entry(network_acl.id, 200, 6, 'allow', '0.0.0.0/0', egress=False, port_range_from='1024', port_range_to='65535')
            conn.create_network_acl_entry(network_acl.id, 300, 17, 'allow', '0.0.0.0/0', egress=False, port_range_from='1024', port_range_to='65535')
            # Egress
            conn.create_network_acl_entry(network_acl.id, 100, -1, 'allow', cidr, egress=True)
            conn.create_network_acl_entry(network_acl.id, 200, 6, 'allow', '0.0.0.0/0', egress=True, port_range_from='443', port_range_to='443')
            conn.create_network_acl_entry(network_acl.id, 300, 6, 'allow', '0.0.0.0/0', egress=True, port_range_from='80', port_range_to='80')
        else:
            conn.create_network_acl_entry(network_acl.id, 100, -1, 'allow', '0.0.0.0/0', egress=False)
            conn.create_network_acl_entry(network_acl.id, 100, -1, 'allow', '0.0.0.0/0', egress=True)

        for sub in sub_list:
            conn.associate_route_table(route_table.id, sub)
            conn.associate_network_acl(network_acl.id, sub)

        sub_list = [ ]
        tag_sub_no = 1

        if tag_tier == "private":
            tag_tier_no += 1
        tag_tier = 'private'

# end of main loop

# Output info
#
print("\n** VPC creation complete. ** \n\nVPC Id :", vpc.id)

subnet_list = conn.get_all_subnets(filters={ "vpcId":vpc.id })
print("AZ total :", az_total, "\nSubnets :")
for sub in subnet_list:
    print(sub.id)
