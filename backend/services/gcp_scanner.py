
# GCP resource scanner

from google.cloud import monitoring_v3
from google.auth import default
from datetime import datetime, timedelta, timezone

def get_idle_gce_instances(project_id, zone, threshold=10, days=14):
    credentials, _ = default()
    client = monitoring_v3.MetricServiceClient(credentials=credentials)

    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    start_time = now - timedelta(days=days)

    interval = monitoring_v3.TimeInterval({
        "start_time": start_time,
        "end_time": now,
    })

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 86400},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    )

    results = client.list_time_series(
        request={
            "name": f"projects/{project_id}",
            "filter": 'metric.type="compute.googleapis.com/instance/cpu/utilization"',
            "interval": interval,
            "aggregation": aggregation,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    idle_instances = []

    for ts in results:
        instance_id = ts.resource.labels.get("instance_id")
        avg_cpu = sum(point.value.double_value for point in ts.points) / len(ts.points)
        if avg_cpu * 100 < threshold:
            idle_instances.append({
                "InstanceID": instance_id,
                "AverageCPU": round(avg_cpu * 100, 2)
            })

    return idle_instances
