### Automated EBS Volume Snapshots

This BASH script will create a snapshot of EBS volumes mathcing
a specific TAG key/value pair. It will look for snapshots older than a retention
period/date and remove them.

Can be run from cron once a day, or from AWS Data Pipeline (ebs-snapshot-dp.sh)

**Requirements:**

* The awscli  `sudo pip install awscli`
* A valid profile in ~/.aws/config or ${AWS_CONFIG_FILE} with the appropriate API keys (ebs-snapshot.sh)
* MacOS `date` command/format (ebs-snapshot.sh)

**An EBS volume snapshot will be created if:**

* The EBS volume is assigned the TAG key/value pair; "Autosnap/True"

**A Snapshot will be removed only after meeting the following criteria:**

* The snapshot status equals "complete"
* Snapshot has the description, "Automated snapshot"
* The snapshot is older than the specified retention period/date (7 days by default)

**Usage:**

```
ebs-snapshot.sh --profile <profile_name> [ --region <region_name> ]
ebs-snapshot-dp.sh [ --region <region_name> ]
```

**Output:**

```
./ebs-snapshot.sh --profile eng --region us-west-2
```

```
Creating snapshot for EBS volume, vol-953dcf85...
{
    "Description": "Automated snapshot", 
    "Encrypted": false, 
    "VolumeId": "vol-953dcf85", 
    "State": "pending", 
    "VolumeSize": 10, 
    "Progress": null, 
    "StartTime": "2015-05-04T16:41:01.000Z", 
    "SnapshotId": "snap-e054ffa3", 
    "OwnerId": "XXXXXXXX5893"
}
snap-e29174a0 has been deleted.
snap-35097d70 has been deleted.
```

**To Do:**

- [ ] Modify to handle/use the `date` command from other linux flavors
- [ ] Add the necessary logic to run from either cmd-line (i.e. --profile) or Data Pipeline

**Notes:**

Data Pipeline Workflow
![EBS Snapshot Diagram](./ebs-autosnap-edp-flow.jpg)

AWS Linux Date

`date -d"$TODAY" +%s`
