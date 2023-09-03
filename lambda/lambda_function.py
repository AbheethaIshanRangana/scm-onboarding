import boto3
import csv
import json

def lambda_handler(event, context):
    # AWS Services
    ec2_client = boto3.client('ec2')
    sns_client = boto3.client('sns')

    # Get all EC2 instances
    instances_response = ec2_client.describe_instances()

    # Prepare data for the report
    report_data = []

    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_name = ''
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']

            # Get security groups for the instance
            security_group_ids = [sg['GroupId'] for sg in instance['SecurityGroups']]
            security_groups_response = ec2_client.describe_security_groups(GroupIds=security_group_ids)

            for security_group in security_groups_response['SecurityGroups']:
                for ip_permission in security_group['IpPermissions']:
                    port = ip_permission['FromPort']
                    source = ip_permission['IpRanges'][0]['CidrIp']

                    report_data.append((instance_name, instance_id, port, source))

    # Create the report in CSV format
    report_csv = 'Instance Name, Instance ID, Port/Port range, Source\n'
    for item in report_data:
        report_csv += f'{item[0]}, {item[1]}, {item[2]}, {item[3]}\n'

    # Optional: Send the report via SNS
    topic_arn = 'arn:aws:sns:us-east-1:XXXXXXXXXXXXX:ec2-sg'

    sns_client.publish(
        TopicArn=topic_arn,
        Subject='EC2 Security Group Report',
        Message=report_csv,
    )

    print(report_csv)

    return {
        'statusCode': 200,
        'body': 'Report generated successfully and sent via SNS'
    }
