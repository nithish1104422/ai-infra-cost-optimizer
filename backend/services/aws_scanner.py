import boto3
import os
from datetime import datetime, timedelta

def get_idle_ec2_instances(region_name="us-east-1", cpu_threshold=10, days=14):
    client = boto3.client("cloudwatch", region_name=region_name)
    ec2 = boto3.client("ec2", region_name=region_name)

    # Get all running EC2 instances
    instances = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )

    idle_instances = []

    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]

            # Get CPU utilization over the past `days` days
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)

            metrics = client.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,
                Statistics=["Average"],
            )

            datapoints = metrics.get("Datapoints", [])
            if datapoints:
                avg_cpu = sum(d["Average"] for d in datapoints) / len(datapoints)
                if avg_cpu < cpu_threshold:
                    idle_instances.append({
                        "InstanceId": instance_id,
                        "AverageCPU": round(avg_cpu, 2)
                    })

    return idle_instances
