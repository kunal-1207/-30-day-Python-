# cli.py
import click
from .ec2 import ec2_commands
from .s3 import s3_commands
from .monitoring import monitoring_commands
from .config import load_config

@click.group()
@click.option('--profile', default='default', help='AWS profile to use')
@click.option('--region', default='us-east-1', help='AWS region')
@click.option('--verbose', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, profile, region, verbose):
    """Cloud Resource Management CLI"""
    ctx.ensure_object(dict)
    ctx.obj['CONFIG'] = load_config(profile, region, verbose)

cli.add_command(ec2_commands, name='ec2')
cli.add_command(s3_commands, name='s3')
cli.add_command(monitoring_commands, name='monitor')

if __name__ == '__main__':
    cli(obj={})
