import boto3

rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    bucket = event['bucket']
    key = event['key']

    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': key}},
        MaxLabels=10,
        MinConfidence=70
    )

    return {
        'bucket': bucket,
        'key': key,
        'labels': response['Labels']
    }
