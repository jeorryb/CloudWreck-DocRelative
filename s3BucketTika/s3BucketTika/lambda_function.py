import json
import urllib.parse
import boto3
import tika.tika
from tika import parser

print('Loading function')

s3 = boto3.client('s3')

def getObjectURL(region, bucket, key):
    
    objectURL = "https://s3." + region + ".amazonaws.com/" + bucket + "/" + key
    return objectURL

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    region = event['Records'][0]['awsRegion']
    
    print("URL is: ", getObjectURL(region, bucket, key))
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        parsed = parser.from_file(getObjectURL(region, bucket, key))
        
        return parsed["metadata"]
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
