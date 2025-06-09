# Predict cost trends

import boto3
from datetime import datetime, timedelta

def get_cost_forecast(service='AmazonEC2', region='us-east-1', period='DAILY', duration_days=30):
    client = boto3.client('ce', region_name=region)

    end = datetime.utcnow()
    start = end - timedelta(days=duration_days)

    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start.strftime('%Y-%m-%d'),
                'End': end.strftime('%Y-%m-%d')
            },
            Granularity=period,
            Metrics=["UnblendedCost"],
            Filter={
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": [service]
                }
            },
            GroupBy=[
                {
                    "Type": "DIMENSION",
                    "Key": "SERVICE"
                }
            ]
        )

        cost_data = response['ResultsByTime']
        total_cost = sum(float(day['Total']['UnblendedCost']['Amount']) for day in cost_data)
        average_daily_cost = total_cost / len(cost_data)

        forecast = {
            "Service": service,
            "AverageDailyCost": round(average_daily_cost, 2),
            "EstimatedMonthlyCost": round(average_daily_cost * 30, 2)
        }

        return forecast
    except Exception as e:
        return {"error": str(e)}
