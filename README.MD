# Challenge: AWS Three-Tier Architecture, CloudFormation, Lambda, CodeBuild and CI/CD 
## AWS Three-Tier Architecture 💥 [Infrastructure provisioning]

A 3-Tier architecture provides a general framework for deploying traditional client/server applications into three logical tiers; the Web, Application, and Database tier. End users interact with the Web tier which provides them with a user interface they can use to view, modify, or submit information. The Application tier is responsible for handling the requests made by the user. The Application or Middle tier is the brains behind the operation. It assists in translating users actions into business logic that allow for data processing by programs. Lastly, the Database or Data tier is where the information processed by the application is stored and managed.

### Design

![Design](./assets/design.png)

In case you wonder why we will use availability zones?

1. High Availability
2. Disaster Recovery
3. Data Sovereignty
4. Scalability
5. Fault Tolerance

#### Web Tier [Frontend]

In this layer, we will create a public load balancer and an auto-scaling group. The load balancer will be used to distribute traffic across the instances.

**Resources:**

- 2 public subnets
- Public route table
- Internet Gateway & NAT Gateway
- Internet facing Application Load Balancer with a Security Group allowing inbound permission from the Internet.
- Minimum of 2 EC2 instances in an Auto Scaling Group.
- EC2 Security Group allowing inbound permission from the the Web Tier Application Load Balancer
- Create a public route table and associate the 2 public subnets.

#### Application Tier [Backend]

In this layer, we will create an internal load balancer and an auto-scaling group. The load balancer will be used to distribute traffic across the application servers. The auto-scaling group will be used to scale the number of application servers up or down based on the demand.

**Resources:**

- 2 private subnets
- Private route table
- Internal Application Load Balancer with a Security Group allowing inbound permission from EC2 instances in the Web Tier.
- Minimum of 2 EC2 instances in an Auto Scaling Group
- EC2 Security Group allowing inbound permission from the Application Tier Application Load Balancer
- Image host on docker hub 
- Associate with private route table

#### Database Tier [Data]

In this layer, we will create a Multi AZ RDS MySQL database. The database will be used to store the data for the application.

**Resources:**

- 2 private subnets
- Public route table
- MySql RDS Database with Multi AZ standby instance
- The Database Security Group allowing inbound traffic for MySQL from the Application Server Security Group

#### Admin Tier [Ops]

In this layer, we will create a bastion host. The bastion host will be used to access compute services in private networks for administration purposes.

**Resources:**

- 2 private subnets
- Public route table
- MySql RDS Database with Multi AZ standby instance
- The Database Security Group allowing inbound traffic for MySQL from the Application Server Security Group

## Let's do it 🚀

### Prerequisites

- AWS Account
- AWS CLI, for installation in linux operative system follow the next steps:

    ```sh
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    ```

- Configuring AWS CLI you need **access key and secret key**, you can create it in IAM service.

    ```sh
    aws configure
    ```

1. Creat an EC2 Key Pair used to SSH into the bastion host

```bash
aws ec2 create-key-pair --key-name aws-tree-tier-app-varela --query 'KeyMaterial' --output text > aws-tree-tier-app-varela.pem
```

2. Infrastructure as Code with CloudFormation

- Parameters: Are a way to provide input values to a CloudFormation stack at the time of stack creation or update. Parameters allow you to customize the behavior and configuration of your stack templates without modifying the template itself.

    1. KeyPair: The name of an existing EC2 KeyPair to enable SSH access to the instances
    2. DatabaseUser
    3. DatabasePassword

- Mappings: Are a way to provide conditional parameters to your CloudFormation template based on region or environment. Mappings are a great way to keep your CloudFormation templates DRY.

- Conditions: Are a way to control whether certain resources are created or whether certain resource properties are assigned a value during stack creation or update. Conditions are declared in the Conditions section of a CloudFormation template.

- Resources: Are the core of your CloudFormation template. Resources are the AWS components that you want to deploy as part of your infrastructure such as EC2 instances, RDS databases, VPCs, and more. In our we will create the following resources.

    1. VPC
    2. Internet Gateway
    3. NAT Gateway
    4. Public Subnets [3]
    5. Private Subnets [4]
    6. Public Route Table
    7. Private Route Table
    8. Web Tier Security Group
    9. Application Tier Security Group
    10. Database Tier Security Group
    11. Bastion Host Security Group
    12. Web Tier Application Load Balancer
    13. Application Tier Application Load Balancer
    14. Web Tier Auto Scaling Group
    15. Application Tier Auto Scaling Group
    16. Database Tier RDS MySQL

- Outputs: Are a way to return information about your AWS infrastructure stack after it has been created or updated. Outputs are declared in the Outputs section of a CloudFormation template.

- Transform: Is a macro that processes your template in two phases. In the first phase, the macro processes all intrinsic functions except for Fn::Transform. In the second phase, the macro recursively expands macros. The following example shows a template that uses the AWS::Include transform to include a snippet of YAML-formatted template code from an Amazon S3 bucket.

- Metadata: Is a section in a CloudFormation template that contains additional information for AWS CloudFormation to process but that is not strictly part of the template's AWS resources. Metadata is optional.

3. Create a CloudFormation Stack

```bash
aws cloudformation create-stack --stack-name aws-tree-tier-app-varela --template-body file://./iac/main.yml --parameters file://./iac/parameters.json
```

4. Check the status of the stack

```bash
aws cloudformation describe-stacks --stack-name aws-tree-tier-app-varela --query 'Stacks[0].StackStatus'
```

5. Check the outputs of the stack

    - Bastion Host Public IP
    - Web Tier Application Load Balancer URL
    - Application Tier Application Load Balancer URL
    - Endpoint URL address for our RDS MySQL Database
    - RDS MySQL Database TCP Port used

    ```bash
    aws cloudformation describe-stacks --stack-name aws-tree-tier-app-varela --query 'Stacks[0].Outputs'
    ``` 

6. Delete the stack

```bash
aws cloudformation delete-stack --stack-name aws-tree-tier-app-varela
```

# Lambda AWS

## What is Lambda?

Is a serverless computing service provided by AWS, it runs your code in response to events and automatically manages the underlying compute resources for you. You can use AWS Lambda to extend other AWS services with custom logic, or create your own back-end services that operate at AWS scale, performance, and security.

**Requirements:**

- Create an IAM role for the AWS Lambda function and assign the necessary permissions to perform the task.

    IAM Role creation:

    ```bash
    aws iam create-role --role-name LambdaRole --assume-role-policy-document file://../serverless/trust-policy.json
    ```
    Attach Policy to Role:

    ```bash
    aws iam attach-role-policy --role-name LambdaRole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
    ```

    Create source-bucket and upload a local image file

    ```bash
    aws s3api create-bucket --bucket source-bucket --region us-east-1
    aws s3 cp ./assets/design.png s3://source-bucket/src/design.png
    ```
    ```

- Use the AWS CLI to create an AWS Lambda function that performs a simple task, such as copying a file from one Amazon S3 bucket to another bucket.

    ```bash
    aws lambda create-function --function-name S3Lambda --runtime python3.8 --role arn:aws:iam::163740413966:role/LambdaRole --handler lambda-function.lambda_handler --code fileb://../serverless/s3-basic-operations.py
    ```

    Invoke the AWS Lambda function to verify that it works correctly.

    ```bash
    aws lambda invoke --function-name S3Lambda --payload file://event.json output.txt
    ```

# CodeBuild AWS

**Requirements:**

Use CodeBuild to build the CloudFormation deployment artifact from the CloudFormation template.

# CI/CD AWS

**Requirements:**
Create a gtihub workflow with two jobs, one to set up the environment and simulate running automated unit tests, and another that only runs if tests pass to deploy to an EC2 instance, over SSH using a file deployment. sh

# Monitoring AWS

**Requirements:**
Add a CloudWatch alert that sends an email notification when the RDS database exceeds 80% capacity

1. Create a IAM policy for allow CloudWatch to send email notifications

```bash
aws iam create-policy --policy-name CloudWatchEmailNotification --policy-document file://../monitoring/cloudwatch-email-notification-policy.json
```

2. Get ARN of the policy

```bash
aws iam list-policies --query 'Policies[?PolicyName==`CloudWatchEmailNotification`].Arn' --output text
```

3. Create a SES verified email address

```bash
aws ses verify-email-identity --email-address alejo8677@gmail.com
```

4. Configure CloudWatch to send email notifications

```bash
aws cloudwatch put-metric-alarm --alarm-name RDS-Storage-Usage --alarm-description "RDS Storage Usage" --metric-name FreeStorageSpace --namespace AWS/RDS --statistic Average --period 300 --threshold 80 --comparison-operator GreaterThanThreshold --dimensions Name=DBInstanceIdentifier,Value=aws-tree-tier-app-varela-db --evaluation-periods 1 --alarm-actions arn:aws:iam::163740413966:policy/CloudWatchEmailNotification --unit Bytes
```





