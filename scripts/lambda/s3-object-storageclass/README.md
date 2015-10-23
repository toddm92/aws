### Change S3 Object StorageClass

<p>
A S3 Put object triggers this function. It checks the storage class of the new object (by default STANDARD) and converts the object to STANDARD_IA.

<b>Requirements:</b>
<ul>
 <li> Tested w/ python version 2.7
 <li> The s3-object-role.json policy/IAM Role
</ul>
