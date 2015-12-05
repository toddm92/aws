#!/usr/bin/env python
#
# Python Version: 2.7
# Boto Version 2.38
#
# Remove those pesky default VPCs
#
# Warning: Deleting the default VPC is a permanent action.
#          You must contact AWS Support if you want to create a new default VPC.
#

# Must be the first line
from __future__ import print_function

import sys
import boto.vpc
import boto.ec2

VERBOSE = 1

def get_regions():
  """ Build a region list """

  reg_list = []
  for reg in boto.vpc.regions():
    if reg.name == 'us-gov-west-1' or reg.name == 'cn-north-1':
      continue
    reg_list.append(reg)

  return reg_list

def del_igw(conn, vpcid):
  """ Detach and delete the internet-gateway """
      
  igw = conn.get_all_internet_gateways(filters={'attachment.vpc-id': vpcid})
  if igw:
    try:
      print("Removing igw-id: ", igw[0].id) if (VERBOSE == 1) else ""
      conn.detach_internet_gateway(igw[0].id, vpcid)
      status = conn.delete_internet_gateway(igw[0].id)
    except boto.exception.EC2ResponseError as e:
      print(e.message)

def del_sub(conn, vpcid):
  """ Delete the subnets """
      
  subs = conn.get_all_subnets(filters={'vpcId': [vpcid]})
  if subs:
    try:
      for sub in subs: 
        print("Removing sub-id: ", sub.id) if (VERBOSE == 1) else ""
        status = conn.delete_subnet(sub.id)
    except boto.exception.EC2ResponseError as e:
      print(e.message)

def del_rtb(conn, vpcid):
  """ Delete the route-tables """
      
  rtbs = conn.get_all_route_tables(filters={'vpc-id': vpcid})
  if rtbs:
    try:
      for tbl in rtbs:
        for assoc in tbl.associations:
          main = 'true' if (assoc.main == True) else 'false'
        if main == 'true':
          continue
        print("Removing rtb-id: ", tbl.id) if (VERBOSE == 1) else ""
        status = conn.delete_route_table(tbl.id)
    except boto.exception.EC2ResponseError as e:
      print(e.message)

def del_acl(conn, vpcid):
  """ Delete the network-access-lists """
      
  acls = conn.get_all_network_acls(filters={'vpc-id': vpcid})
  if acls:
    try:
      for acl in acls: 
        if acl.default == 'true':
          continue
        print("Removing acl-id: ", acl.id) if (VERBOSE == 1) else ""
        status = conn.delete_network_acl(acl.id)
    except boto.exception.EC2ResponseError as e:
      print(e.message)

def del_sgp(conn, vpcid):
  """ Delete any security-groups """
      
  sgps = conn.get_all_security_groups(filters={'vpc-id': vpcid})
  if sgps:
    try:
      for sg in sgps: 
        if sg.name == 'default':
          continue
        print("Removing sgp-id: ", sg.id) if (VERBOSE == 1) else ""
        status = conn.delete_security_group(group_id=sg.id)
    except boto.exception.EC2ResponseError as e:
      print(e.message)

def del_vpc(conn, vpcid):
  """ Delete the VPC """
      
  try:
    print("Removing vpc-id: ", vpcid)
    status = conn.delete_vpc(vpcid)
  except boto.exception.EC2ResponseError as e:
      print(e.message)
      print("Please remove dependencies and delete VPC manually.")
  #finally:
  #  return status

def main(keyid, secret):
  """
  Do the work - order of operation

  1.) Delete the internet-gateway
  2.) Delete subnets
  3.) Delete route-tables
  4.) Delete network access-lists
  5.) Delete security-groups
  6.) Delete the VPC 
  """

  regions = get_regions()

  for region in regions:
    try:
      conn = boto.vpc.VPCConnection(aws_access_key_id=keyid, aws_secret_access_key=secret, region=region)
      attributes = conn.describe_account_attributes(attribute_names='default-vpc')
    except boto.exception.EC2ResponseError as e:
      print(e.message)
      exit(1)
    else:
      print("\n" + region.name.upper())

      for attribute in attributes:
        default = attribute.attribute_values[0]
        print("Default  vpc-id: ", default)

      if default != 'none':
        del_igw(conn, default)
        del_sub(conn, default)
        del_rtb(conn, default)
        del_acl(conn, default)
        del_sgp(conn, default)
        del_vpc(conn, default)

if __name__ == "__main__":

  main(keyid = 'XXXX', secret = 'XXXX')
