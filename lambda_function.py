import boto3
import json

sfn = boto3.client('stepfunctions')

def lambda_handler(event, context):
    print("Received S3 event:", json.dumps(event))

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Check if bucket is correct
    if bucket != "imageuploadpipeline":
        print("Skipping - wrong bucket")
        return {'statusCode': 400}

    response = sfn.start_execution(
        stateMachineArn='arn:aws:states:region:Accountid:stateMachine:MediaProcessingWorkflow',
        input=json.dumps({'bucket': bucket, 'key': key})
    )

    print("Step Function triggered:", response['executionArn'])

    return {'statusCode': 200}
