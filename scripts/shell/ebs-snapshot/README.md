### Automated EBS Volume Snapshots

This BASH script will create a snapshot of AWS EBS volumes mathcing
a specific TAG key/value pair. It will look for snapshots older than a retention
period/date and remove them.

This script has moved into its own repo:

https://github.com/toddm92/ebs-snapshot
