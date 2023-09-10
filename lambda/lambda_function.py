import boto3
from collections import defaultdict
from datetime import datetime

sg_rules = defaultdict(list)

def get_instance_name(instance):
    for tag in instance.get('Tags', []):
        if tag['Key'] == 'Name':
            return tag['Value']
    return "N/A"
    
def lambda_handler(event, context):

    ec2_client = boto3.client('ec2', region_name='us-east-1')
    ec2_instances = ec2_client.describe_instances()
    ses_client = boto3.client('ses')

    #print(ec2_instances)

    for reservation in ec2_instances['Reservations']:
        #print(reservation)
        for instance in reservation['Instances']:
            #print(instance)
            instance_name = get_instance_name(instance)
            instance_id = instance['InstanceId']
            #print(f"Instance ID: {instance_id}")
            security_groups = instance['SecurityGroups']
            #print(f"Security Groups: {security_groups}")

            for sg in security_groups:
                sg_id = sg['GroupId']
                sg_name = sg['GroupName']
                #print(f"Security Group Name/ID: {sg_name}/{sg_id}")

                sg_info = ec2_client.describe_security_groups(GroupIds=[sg_id])
                #print(f"Security Group Info: {sg_info}")
                inbound_rules = sg_info['SecurityGroups'][0]['IpPermissions']
                #print(f"Inbound Rules: {inbound_rules}")

                for rule in inbound_rules:
                    from_port = rule.get('FromPort','All')
                    #print(f"From Ports: {from_port}")
                    to_port = rule.get('ToPort','All')
                    #print(f"To Ports: {to_port}")
                    ip_ranges = [ip_range['CidrIp'] for ip_range in rule.get('IpRanges', [])]
                    #print(f"IP Ranges: {ip_ranges}")

                    sg_rules[instance_name].append((instance_id, from_port, to_port, ip_ranges))

                    print(sg_rules)

    # Create an HTML table
    html_table_report = '<h2>EC2 Security Group Report</h2>'
    html_table_report += '<table border="1">\n'
    html_table_report += '<tr><th>Instance Name</th><th>Instance ID</th><th>From Port</th><th>To Port</th><th>IP Ranges</th></tr>\n'

    for instance_name, instances in sg_rules.items():
        for instance in instances:
            instance_id, from_port, to_port, ip_ranges = instance
            ip_ranges_str = ', '.join(ip_ranges)
            html_table_report += f'<tr><td>{instance_name}</td><td>{instance_id}</td><td>{from_port}</td><td>{to_port}</td><td>{ip_ranges_str}</td></tr>\n'

    html_table_report += '</table>'

    # Save the HTML table to a file or print it
    print(html_table_report)

    # send email via SES
    sender_email = 'sender@gmail.com'
    recipient_email = 'receiver@gmail.com'
    subject = f"EC2 Security Group Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    try:
        response = ses_client.send_email(
                Source = sender_email,
                Destination = {'ToAddresses': [recipient_email]},
                Message = {
                    'Subject': {'Data': subject},
                    'Body': {'Html': {'Data': html_table_report}},
                }
        )
    
        print("Email sent successfully")

    except Exception as e:
        print(f"Error sending email: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': 'Report generated successfully and sent via SES'
    }
