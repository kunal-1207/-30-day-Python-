# s3.py
import os
import click
import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm
from .utils.logging import get_logger
from .utils.exceptions import handle_aws_error

logger = get_logger(__name__)

@click.group()
def s3_commands():
    """S3 bucket management commands"""
    pass

@s3_commands.command()
@click.option('--prefix', default='', help='Filter buckets with prefix')
@click.pass_context
def list_buckets(ctx, prefix):
    """List S3 buckets"""
    try:
        s3 = ctx.obj['CONFIG'].s3_client
        response = s3.list_buckets()
        
        buckets = [b['Name'] for b in response['Buckets'] if b['Name'].startswith(prefix)]
        
        if not buckets:
            click.echo("No buckets found matching criteria")
            return
            
        click.echo("Available buckets:")
        for bucket in buckets:
            click.echo(f"- {bucket}")
    
    except ClientError as e:
        handle_aws_error(e, "Failed to list buckets")

@s3_commands.command()
@click.argument('bucket_name')
@click.argument('local_path', type=click.Path(exists=True))
@click.option('--key', help='S3 object key (defaults to filename)')
@click.pass_context
def upload_file(ctx, bucket_name, local_path, key=None):
    """Upload file to S3 bucket with progress bar"""
    try:
        s3 = ctx.obj['CONFIG'].s3_client
        
        if not key:
            key = os.path.basename(local_path)
        
        file_size = os.path.getsize(local_path)
        
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=key) as pbar:
            def upload_progress(chunk):
                pbar.update(chunk)
            
            s3.upload_file(
                local_path,
                bucket_name,
                key,
                Callback=upload_progress
            )
        
        click.echo(f"Successfully uploaded {local_path} to s3://{bucket_name}/{key}")
    
    except ClientError as e:
        handle_aws_error(e, f"Failed to upload file to {bucket_name}")
    except Exception as e:
        logger.error(f"Unexpected error during upload: {str(e)}")
        raise click.ClickException("Upload failed")
