### Lambda: Change S3 Object StorageClass

An S3 'put object' triggers this function. It checks the storage class of the new S3 object (by default STANDARD) and converts the object to STANDARD_IA.

**Requirements:**

* Tested w/ python version 2.7
* The s3-object-role.json policy/IAM Role

![Lambda Flow Diagram](https://s3-us-west-2.amazonaws.com/toddm92/public/diagrams/sclass-flow.jpg)
