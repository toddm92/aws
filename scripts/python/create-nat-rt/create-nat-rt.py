#!/usr/bin/env python
#
# Python Version: 2.7
# Boto Version 2.38
#
# Build VPC NAT route tables
# Used for sending specified traffic thru a NAT gateway
#

# Must be the first line
from __future__ import print_function

import sys
import boto.vpc

#  Modify variables as needed
PROFILE = 'eng'       # (from your ~/.boto)
REGION = 'us-west-2'

myregion = boto.ec2.get_region(region_name=REGION)
conn = boto.vpc.VPCConnection(profile_name=PROFILE, region=myregion)

def usage():
  """ Usage statement """

  print("""
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
    """)

def create_rtb(vpc, igw = "None", instance = "None"):
  """ Create VPC route-table """

  try:
    route_list = open('routes.txt', 'r')
  except Exception as e:
    print(e)
    exit(1)
  else:
    newrt = conn.create_route_table(vpc)

  print('Populating routes..')
  for route in route_list:
    route = route.replace('\n', '')
    conn.create_route(newrt.id, route, gateway_id=None, instance_id=instance, interface_id=None)

  print('Creating default route..')
  conn.create_route(newrt.id, '0.0.0.0/0', gateway_id=igw, instance_id=None, interface_id=None)
  route_list.close()

  return newrt.id

def get_nat():
  """ Get NAT Instance Id """

  nat_id = ''
  while 'i-' not in nat_id:
    nat_id = raw_input('Enter the NAT instance id for this route table: '); nat_id = nat_id.lower()

  try:
    conn.get_all_instances(instance_ids=nat_id, filters=None, max_results=None)
  except Exception as e:
    print(e.message)
    exit(1)
  else:
    return nat_id

def tag_it(resource):
  """ Tag our route-tables """

  name = ''
  while len(name) == 0:
    name = raw_input('Route Table name? '); name = name.lower()

  conn.create_tags(resource, { 'Name' : name })

  return name

def main():
  """ Do the work """

  # Print usage and instructions
  usage()

  # Get the VPC Id
  vpc_id = ''
  while 'vpc-' not in vpc_id:
    vpc_id = raw_input('\nEnter your vpc-id: '); vpc_id = vpc_id.lower()

  try:
    conn.get_all_vpcs(vpc_ids=vpc_id, filters=None)
  except Exception as e:
    print(e.message)
    exit(1)

  # Get the igw Id
  try:
    igw = conn.get_all_internet_gateways(filters={'attachment.vpc-id': vpc_id})
  except Exception as e:
    print(e.message)
    exit(1)
  else:
    igw = str(igw[0])
    igw_id = igw[16:]

  # Create the first route table
  instance_id = get_nat()
  newrt_id = create_rtb(vpc_id, igw_id, instance_id)
  tag = tag_it(newrt_id)
  print('New Route Table Id for', tag, ':', newrt_id)

  # Ask to create additional route tables
  reply = 'yes'
  while reply not in ('n', 'no'):
    reply = raw_input('\nCreate another Route Table? '); reply = reply.lower()
    if reply in ( 'y', 'ye', 'yes' ):
      instance_id = get_nat()
      newrt_id = create_rtb(vpc_id, igw_id, instance_id)
      tag = tag_it(newrt_id)
      print('New Route Table Id for', tag, ':', newrt_id)

if __name__ == "__main__":

  main()
