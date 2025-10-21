import boto3
import json
import os

sns = boto3.client('sns')

def lambda_handler(event, context):
    key = event['key']
    bucket = event['bucket']
    labels = event.get('labels', [])

    lines = [
        f"Rekognition results for: s3://{bucket}/{key}\n",
        "Detected Labels:"
    ]

    for label in labels:
        lines.append(f"- {label['Name']} ({label['Confidence']:.2f}%)")

    message = "\n".join(lines)

    response = sns.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Subject='🧠 AWS Rekognition Analysis Result',
        Message=message
    )

    return {
        'status': 'email_sent',
        'messageId': response['MessageId']
    }
