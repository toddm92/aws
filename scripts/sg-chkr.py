#!/usr/bin/env python
#
# Python Version: 2.7
#
# Scan for "open" security groups 

# Must be the first line
from __future__ import print_function

import boto.vpc
import boto.ec2
import sys

# ** Modify these variables as needed **
REGIONS = ( 'us-east-1',  'eu-west-1',  'ap-northeast-1',
            'us-west-1', 'us-west-2', 'ap-southeast-1',
            'ap-southeast-2', 'sa-east-1' )
# **

# Make our text pretty
class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def usage():
    """Usage Statement"""

    print("""

  Security group checker..
    """)

    print("\t* use: --profile <profile_name>")
    print("\t" + bcolors.GREEN + "profile_name " + bcolors.ENDC + "from your ~/.boto (~/.aws/config)\n\n")

    exit()

# Check for arguments
args = len(sys.argv)
if args != 3:
    usage()

if '--profile' in (str(sys.argv[1]).lower()):
    profile = str(sys.argv[2]).lower()
else:
    usage()

reg_total = len(REGIONS)
reg_no = 0

# Test in each region (main loop)
while reg_total > 0:

    # Do the work
    sg_no = 0
    reg_name = REGIONS[reg_no]
    myregion = boto.ec2.get_region(region_name=reg_name)
    try:
        conn = boto.vpc.VPCConnection(profile_name=profile, region=myregion)
    except Exception,e:
        print("\nCheck your profile_name in ~/.boto and try again.")
        print(e)
        usage()

    print("\nRegion:", reg_name)

    # Get all security groups
    all_sgs = conn.get_all_security_groups()
    sg_total = len(all_sgs)
    print("Number of SGs:", sg_total, "\n")

    # Scan the rules in each security group 
    # Look for 0.0.0.0/0 as the source - ports 80 and 443 probably ok, but print them anyway
    while sg_no < sg_total:

        sg = all_sgs[sg_no]
        for rule in sg.rules:
            if str(rule.from_port) == "80" or str(rule.from_port) == "443":
                textc = bcolors.WARNING
            else:
                textc = bcolors.FAIL
            for grant in rule.grants:
                if str(grant) in ("0.0.0.0/0"):
                    print(textc + "WARNING: Open security group >>>", sg.name, "(", sg.id, ")")
                    textc = bcolors.ENDC
                    print(textc + "Proto:", rule.ip_protocol, "\tPorts:", rule.from_port, "\t", rule.to_port, "\tSource:", rule.grants, "\n")

        sg_no += 1

    reg_no += 1
    reg_total -= 1
#
# (end main loop)
