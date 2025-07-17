import boto3
import botocore.exceptions

class CloudWatch_Helper:
    def __init__(self, region_name="eu-central-1"):
        self.client = boto3.client("cloudwatch", region_name=region_name)
        self.logs_client = boto3.client("logs", region_name=region_name)

    def list_metrics(self, namespace=None):
        if namespace:
            return self.client.list_metrics(Namespace=namespace)
        return self.client.list_metrics()

    def get_metric_statistics(self, namespace, metric_name, dimensions, start_time, end_time, period, statistics):
        return self.client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=statistics
        )

    def create_log_group(self, log_group_name):
        try:
            self.logs_client.create_log_group(logGroupName=log_group_name)
            print(f"Log group '{log_group_name}' created successfully.")
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                print(f"Log group '{log_group_name}' already exists.")
            else:
                print(f"Unexpected error: {e}")

    def print_recent_logs(self, log_group_name, limit=5):
        streams = self.logs_client.describe_log_streams(
            logGroupName=log_group_name,
            orderBy='LastEventTime',
            descending=True,
            limit=1
        )

        if not streams['logStreams']:
            print("No log streams found.")
            return

        log_stream_name = streams['logStreams'][0]['logStreamName']

        events = self.logs_client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            limit=limit,
            startFromHead=False
        )

        for event in events['events']:
            print(event['message'])
