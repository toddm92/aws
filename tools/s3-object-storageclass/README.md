### Change S3 Object StorageClass

<p>
An S3 'put object' triggers this function. It checks the storage class of the new S3 object (by default STANDARD) and converts the object to STANDARD_IA.

<b>Requirements:</b>
<ul>
 <li> Tested w/ python version 2.7
 <li> The s3-object-role.json policy/IAM Role
</ul>

![Lambda Flow Diagram](https://s3-us-west-2.amazonaws.com/toddm92/public/diagrams/sclass-flow.jpg)
