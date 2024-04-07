import pulumi
import pulumi_aws as aws



# Step 2: Set Up IAM Role for Lambda Function
# Create an IAM role that will be assumed by the Lambda Function.
iam_lambda_role = aws.iam.Role(
    "amish-lambdaRole",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            }
        }]
    }"""
)

# Attach the AWS Lambda Basic Execution Role policy to the role.
lambda_exec_policy_attachment = aws.iam.RolePolicyAttachment("lambdaExecPolicyAttachment",
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    role=iam_lambda_role.name
)

my_lambda_function = aws.lambda_.Function(
    "amish-pulumi-lambda",
    code=pulumi.AssetArchive({
        '.': pulumi.FileArchive('lambda')   #read lambda.zip
    }),
    role=iam_lambda_role.arn,
    handler="lambda.lambda_handler",  #read lambda.py file from lambda zip folder
    runtime="python3.10",
    tags={
       
        "Name": "Amish-pulumi-lambda",
        "Creator": "amishthapa@gmail.com",
        "Project": "Intern",
        "Deletable": "yes"
    
    }
)

# create lambda function URL

lambda_function_url = aws.lambda_.FunctionUrl(
    "amish-lambda-url",
    function_name=my_lambda_function.name,
    authorization_type="NONE"
)

pulumi.export('lambda_function_arn', my_lambda_function.arn)
pulumi.export('lambda_function_url', lambda_function_url.function_url)



# size = "t2.micro"

# ami = aws.ec2.get_ami(
#     most_recent=True,
#     owners=["amazon"],
#     filters=[aws.ec2.GetAmiFilterArgs(name="name", values=["amzn2-ami-hvm-*"])],
# )

# group = aws.ec2.SecurityGroup(
#     "web-secgrp",
#     description="Enable HTTP access",
#     ingress=[
#         aws.ec2.SecurityGroupIngressArgs(
#             protocol="tcp",
#             from_port=80,
#             to_port=80,
#             cidr_blocks=["0.0.0.0/0"],
#         )
#     ],
# )

# user_data = """
# #!/bin/bash
# echo "Hello, World!" > index.html
# nohup python -m SimpleHTTPServer 80 &
# """

# server = aws.ec2.Instance(
#     "web-server-www",
#     instance_type=size,
#     vpc_security_group_ids=[group.id],
#     user_data=user_data,
#     ami=ami.id,
# )


# pulumi.export("public_ip", server.public_ip)
# pulumi.export("public_dns", server.public_dns)

# lambda_ = archive.get_file(type="zip",
#     source_file="./lamda/lambda.py",
#     output_path="./lambda/lambda_function_payload.zip")
#  source_code_hash=lambda_.output_base64sha256,