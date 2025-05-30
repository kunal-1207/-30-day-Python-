# cloud_manager/ec2.py
import click
from botocore.exceptions import ClientError
from .utils.logging import get_logger
from .utils.exceptions import handle_aws_error

logger = get_logger(__name__)

@click.group()
def ec2_commands():
    """EC2 instance management commands"""
    pass

@ec2_commands.command()
@click.option('--state', type=click.Choice(['running', 'stopped', 'all']), 
              default='all', help='Filter instances by state')
@click.pass_context
def list_instances(ctx, state):
    """List EC2 instances using the configured AWS manager"""
    try:
        # Access through the config's aws_manager
        ec2 = ctx.obj['CONFIG'].aws_manager.get_client('ec2')
        response = ec2.describe_instances()
        
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if state == 'all' or instance['State']['Name'] == state:
                    instances.append({
                        'id': instance['InstanceId'],
                        'type': instance['InstanceType'],
                        'state': instance['State']['Name'],
                        'public_ip': instance.get('PublicIpAddress', 'N/A')
                    })
        
        if not instances:
            click.echo("No instances found matching criteria")
            return
            
        for instance in instances:
            click.echo(f"ID: {instance['id']}, Type: {instance['type']}, "
                      f"State: {instance['state']}, IP: {instance['public_ip']}")
    
    except ClientError as e:
        handle_aws_error(e, "Failed to list instances")

@ec2_commands.command()
@click.pass_context
def show_account(ctx):
    """Display current AWS account information"""
    try:
        config = ctx.obj['CONFIG']
        click.echo(f"AWS Account ID: {config.account_id}")
        click.echo(f"Region: {config.current_region}")
        click.echo(f"Profile: {config.current_profile}")
    except Exception as e:
        handle_aws_error(e, "Failed to get account information")
