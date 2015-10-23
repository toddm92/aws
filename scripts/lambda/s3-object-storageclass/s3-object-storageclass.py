import json
import boto3

print('Loading function...')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # print("EVENT: ", event)

    # Get the object from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    prefix = event['Records'][0]['s3']['object']['key']
    source = bucket + '/' + prefix
    
    try:
        # Find the object storage class
        object = s3.list_objects(Bucket=bucket, Prefix=prefix)
        storage = object['Contents'][0]['StorageClass']
        
        # Change object to STANDARD_IA class storage
        if storage != 'STANDARD_IA':
            s3.copy_object(Bucket=bucket, CopySource=source, Key=prefix, StorageClass='STANDARD_IA')
            print('StorageClass for object ' + source + ' changed to STANDARD_IA')
        else:
            print('No change to object ' + source)
            
    except Exception as e:
        print(e)
        print('Error getting object ' + source)
