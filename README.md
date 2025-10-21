# media-analysis-pipeline-on-AWS
A fully automated serverless pipeline built on AWS for processing and analyzing media (images/videos) uploaded to an S3 bucket, orchestrating analysis with AWS Step Functions, and sending final status notifications.

# 🖼️ Serverless Media Processing Workflow (S3 → Step Functions → Rekognition)

This project implements a fully serverless, event-driven workflow on AWS for automated media (image/video) analysis. When a file is uploaded to an S3 bucket, it automatically triggers an analysis pipeline using AWS Step Functions to orchestrate AWS Lambda and Amazon Rekognition, and finally notifies a user via email using Amazon SNS.

## ✨ Key Features

* **Event-Driven Architecture: The workflow starts instantly upon a file upload to S3.
* **Serverless Orchestration: AWS Step Functions manages the sequential flow of tasks.
* **AI/ML Integration: Amazon Rekognition is used for content analysis and label detection.
* **Decoupled Notifications: Amazon SNS handles the email delivery of the analysis results.
* **Scalable and Cost-Effective: Uses purely serverless components (Lambda, S3, SNS, Rekognition, Step Functions).

## 📐 Architecture



The workflow is fully serverless from the client to the back-end.

1.  S3 (Static Website): The client-side application is hosted here, providing the file upload interface.
2.  S3 (`imageuploadpipeline`): The media file is uploaded directly to this bucket via the website's JavaScript. This upload is the event trigger.
3.  `TriggerHandler` Lambda: Activated by the S3 upload. It extracts the S3 bucket and key and starts the Step Function execution.
4.  Step Function (`MediaProcessingWorkflow`): Orchestrates the core logic:
    `AnalyzeMedia` Task (Lambda): Calls Amazon Rekognition to detect labels in the uploaded media.
    `StoreResults` Task (Lambda): Formats the analysis results and publishes them to an SNS Topic.
5.  SNS (`RekognitionResultsTopic`): Sends the final analysis results as an email notification to the configured subscriber.

## ⚙️ Deployment and Setup

This project uses seven AWS services. Follow these steps to deploy the infrastructure and logic.

### Prerequisites

* An active AWS account.
* AWS CLI configured (optional, but recommended).

### 1. Create S3 Bucket

The bucket is the project's trigger.
Name: `imageuploadpipeline`

### 2. Create IAM Role (`LambdaExecutionRole`)

This single role is used by all Lambda functions. It requires the following managed policies:
* `AmazonS3ReadOnlyAccess`
* `AmazonRekognitionFullAccess`
* `AmazonSNSFullAccess`
* `CloudWatchLogsFullAccess`

### 3. Create SNS Topic

* Name:`RekognitionResultsTopic`
* Subscription: Create an Email subscription with your address and confirm the subscription.

### 4. Deploy Lambda Functions

Create three Python 3.x Lambda functions using the code provided in the respective files below. All functions must use the `LambdaExecutionRole`.

| Function Name  | Code File                            | Purpose                                                 |
| :---           | :---                                 | :---                                                    |
| `TriggerHandler| `trigger_handler/lambda_function.py` | Starts the Step Function. Requires ARN replacement.     |
| `AnalyzeMedia` | `analyze_media/lambda_function.py`   | Detects labels using Rekognition.                       |
| `StoreResults` | `store_results/lambda_function.py`   | Publishes results to SNS. **Requires ENV variable.      |

Note for `TriggerHandler`:Replace the placeholder ARN:
`stateMachineArn='arn:aws:states:YOUR_REGION:YOUR_ACCOUNT_ID:stateMachine:MediaProcessingWorkflow'`

Note for `StoreResults`:Set an Environment Variable :
  Key: `SNS_TOPIC_ARN`
  Value:`arn:aws:sns:YOUR_REGION:YOUR_ACCOUNT_ID:RekognitionResultsTopic`

### 5. Create Step Function State Machine

Create a Standard state machine named `MediaProcessingWorkflow`. Use the ASL JSON definition from `workflow/state_machine_definition.json`.

Important: You must replace `REGION` and `ACCOUNT_ID` placeholders in the `Resource` fields with your actual AWS values.

### 6. Connect S3 Trigger

Configure an Event Notification on the `imageuploadpipeline` S3 bucket:
* Event Type: `s3:ObjectCreated:Put`
* Destination: Lambda Function**
* Function:`TriggerHandler`
* Optional Filter: Suffixes for common media types (`.jpg`, `.png`, `.mp4`).

## 🚀 Testing the Workflow

1.  Upload a test image (e.g., `test.jpg`) to the `imageuploadpipeline` S3 bucket.
2.  Go to the Step Functions Console and observe a new execution of `MediaProcessingWorkflow`.
3.  Check your email inbox for a subject line like "AWS Rekognition Analysis Result" containing the detected labels.

## 📄 Code Files

The core logic is contained in these files:

* [`trigger_handler/lambda_function.py`](trigger_handler/lambda_function.py)
* [`analyze_media/lambda_function.py`](analyze_media/lambda_function.py)
* [`store_results/lambda_function.py`](store_results/lambda_function.py)
* [`workflow/state_machine_definition.json`](workflow/state_machine_definition.json)
