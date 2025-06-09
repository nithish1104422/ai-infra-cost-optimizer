from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.monitor import MonitorClient
from datetime import datetime, timedelta
import os

def get_idle_vms(subscription_id, resource_group, threshold=10, days=14):
    credentials = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credentials, subscription_id)
    monitor_client = MonitorClient(credentials, subscription_id)

    idle_vms = []
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    for vm in compute_client.virtual_machines.list(resource_group):
        vm_name = vm.name
        vm_id = vm.id

        metrics_data = monitor_client.metrics.list(
            resource_uri=vm_id,
            timespan=f"{start_time.isoformat()}/{end_time.isoformat()}",
            interval='PT1H',
            metricnames='Percentage CPU',
            aggregation='Average'
        )

        datapoints = metrics_data.value[0].timeseries[0].data if metrics_data.value else []
        if datapoints:
            avg_cpu = sum((p.average or 0) for p in datapoints) / len(datapoints)
            if avg_cpu < threshold:
                idle_vms.append({
                    "VMName": vm_name,
                    "AverageCPU": round(avg_cpu, 2)
                })

    return idle_vms
