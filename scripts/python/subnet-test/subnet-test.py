#!/usr/bin/env python
#
# Python Version: 2.7
#
# Test VPC subnet creation in all available zones 
# Used for older AWS accounts with both ec2-classic and default-VPC options

# Must be the first line
from __future__ import print_function

import boto.vpc
import boto.ec2
import sys

# ** Modify these variables as needed **
PROFILE = 'eng'  # (from your ~/.boto)
REGIONS = ( 'us-east-1',  'eu-west-1',  'ap-northeast-1',
            'us-west-1', 'us-west-2', 'ap-southeast-1',
            'ap-southeast-2', 'sa-east-1', 'eu-central-1' )
# **

# Dummy varibles
VPC_CIDR =  '10.10.0.0/16'
SUBNETS = ( '10.10.0.0/24',  '10.10.1.0/24',  '10.10.2.0/24',
            '10.10.3.0/24',  '10.10.4.0/24',  '10.10.5.0/24' )

def usage():
    """Usage Statement"""

    print("""

  Testing VPC subnet creation in all availabe zones..

   * Use "-v" (verbose mode) to print error messages (if any) to the screen

    """)

# Print usage
usage()

# Find args
VERBOSE = 'False'
args = len(sys.argv)
if args > 1:
    if '-v' in (str(sys.argv).lower()):
        VERBOSE = 'True'

# Test each region (main loop)
reg_total = len(REGIONS)
reg_no = 0
while reg_total > 0:

    # Ask to test each region
    reg_name = REGIONS[reg_no]
    print("Test region", reg_name, "[yes]? (enter 'q' to quit) ", end = "")
    rsp = raw_input()
    rsp = rsp.lower()
    if rsp == "":
        rsp = "yes"

    if rsp in ( "q", "qu", "qui", "quit" ):
        reg_total = 0
        
    elif rsp not in ( "y", "ye", "yes" ):
        reg_no += 1
        reg_total -= 1

    else:
        # Do the work
        print("Region:", reg_name)
        myregion = boto.ec2.get_region(region_name=reg_name)
        conn = boto.vpc.VPCConnection(profile_name=PROFILE, region=myregion)

        # Create a test VPC
        test_vpc = conn.create_vpc(VPC_CIDR, instance_tenancy='default')

        # Get all available zones
        all_azs = conn.get_all_zones()
        az_total = len(all_azs)

        sub_list = [ ]
        sub_total = 0
        az_no = 0

        # Test each AZ by attempting to create a subnet
        while az_no < az_total:

            az_name = str(all_azs[az_no])
            az_name = az_name[5:]
            try:
                print("Attempting", az_name, end = "")
                sub = conn.create_subnet(test_vpc.id, SUBNETS[sub_total], availability_zone=az_name)
                print(" ..success!")
                sub_list.append(sub.id)
                sub_total += 1
                az_no += 1
            except Exception,e:
                print(" ..failed!")
                if VERBOSE == 'True':
                    print("\n--------------")
                    print("Error Message:")
                    print(e)
                    print("--------------\n")
                az_no += 1

        # Clean up the mess
        print("\nCleaning up", end = "")
        while sub_total != 0:

            sub_total -= 1
            conn.delete_subnet(sub_list[sub_total])

        conn.delete_vpc(test_vpc.id)
        print(" ..done!\n")

        reg_no += 1
        reg_total -= 1
#
# (end main loop)
