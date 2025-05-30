# monitoring.py
import click
from datetime import datetime, timedelta
from .utils.logging import get_logger
from .utils.exceptions import handle_aws_error

logger = get_logger(__name__)

@click.group()
def monitoring_commands():
    """Cloud monitoring commands"""
    pass

@monitoring_commands.command()
@click.argument('instance_id')
@click.option('--period', default=300, help='Metric period in seconds')
@click.option('--hours', default=24, help='Time range in hours')
@click.pass_context
def instance_metrics(ctx, instance_id, period, hours):
    """Get CloudWatch metrics for an EC2 instance"""
    try:
        cloudwatch = ctx.obj['CONFIG'].cloudwatch_client
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        metrics = {
            'CPUUtilization': {
                'namespace': 'AWS/EC2',
                'statistics': ['Average', 'Maximum'],
                'unit': 'Percent'
            },
            'NetworkIn': {
                'namespace': 'AWS/EC2',
                'statistics': ['Sum'],
                'unit': 'Bytes'
            },
            'NetworkOut': {
                'namespace': 'AWS/EC2',
                'statistics': ['Sum'],
                'unit': 'Bytes'
            },
            'DiskReadOps': {
                'namespace': 'AWS/EC2',
                'statistics': ['Sum'],
                'unit': 'Count'
            }
        }
        
        for metric_name, config in metrics.items():
            response = cloudwatch.get_metric_statistics(
                Namespace=config['namespace'],
                MetricName=metric_name,
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=period,
                Statistics=config['statistics'],
                Unit=config['unit']
            )
            
            click.echo(f"\nMetric: {metric_name}")
            if not response['Datapoints']:
                click.echo("No data available")
                continue
                
            for stat in config['statistics']:
                values = [dp[stat] for dp in response['Datapoints']]
                if values:
                    click.echo(f"{stat}: {sum(values)/len(values):.2f} {config['unit']}")
    
    except Exception as e:
        handle_aws_error(e, f"Failed to get metrics for instance {instance_id}")

@monitoring_commands.command()
@click.argument('alarm_name')
@click.argument('instance_id')
@click.option('--threshold', default=80.0, help='CPU utilization threshold')
@click.pass_context
def create_cpu_alarm(ctx, alarm_name, instance_id, threshold):
    """Create CPU utilization alarm for EC2 instance"""
    try:
        cloudwatch = ctx.obj['CONFIG'].cloudwatch_client
        
        cloudwatch.put_metric_alarm(
            AlarmName=alarm_name,
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=1,
            MetricName='CPUUtilization',
            Namespace='AWS/EC2',
            Period=300,
            Statistic='Average',
            Threshold=threshold,
            ActionsEnabled=False,
            AlarmDescription=f'Alarm when CPU exceeds {threshold}%',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                },
            ],
            Unit='Percent'
        )
        
        click.echo(f"Created CPU alarm '{alarm_name}' for instance {instance_id} at {threshold}%")
    
    except Exception as e:
        handle_aws_error(e, "Failed to create alarm")
