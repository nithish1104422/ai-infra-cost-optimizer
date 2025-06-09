
import streamlit as st
import requests

st.set_page_config(page_title="AI Infra Cost Optimizer", layout="wide")

st.title("📊 AI Infrastructure Cost Optimization Dashboard")

st.markdown("Use the form below to generate AI-based cost optimization summaries.")

with st.form("summary_form"):
    resource_name = st.text_input("Resource Name", "staging-ec2-01")
    resource_type = st.selectbox("Resource Type", ["EC2", "RDS", "S3", "EBS", "GCE", "VM"])
    usage_data = st.text_area("Usage Data", "Average CPU usage: 5% over last 14 days")
    recommendation = st.text_area("Recommendation", "Consider downsizing to t3.small to reduce cost.")
    submitted = st.form_submit_button("Generate Summary")

    if submitted:
        response = requests.post(
            "http://localhost:8000/recommendation",
            json={
                "resource_name": resource_name,
                "resource_type": resource_type,
                "usage_data": usage_data,
                "recommendation": recommendation,
            }
        )
        if response.status_code == 200:
            st.success("✅ Summary Generated:")
            st.write(response.json()["summary"])
        else:
            st.error("❌ Failed to generate summary. Check backend service.")
