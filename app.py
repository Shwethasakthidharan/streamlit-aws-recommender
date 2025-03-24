import streamlit as st
import pandas as pd

# Load AWS pricing data
csv_file = "aws_pricing_filtered.csv"  # Ensure this file is in the same directory
df = pd.read_csv(csv_file)

# Data Cleaning
df["vcpu"] = pd.to_numeric(df["vcpu"], errors="coerce")  # Convert vCPU column to numeric
df["memory"] = df["memory"].str.replace(" GiB", "").astype(float)  # Remove " GiB" and convert to numeric

# Streamlit UI settings
st.set_page_config(page_title="AWS Instance Filter", layout="wide")

# App Header
st.title("AWS Instance Recommendation")

# Input section
st.subheader("Configure Your Requirements")

# Dropdown for Cloud Provider
cloud_provider = st.selectbox(
    "Cloud", 
    options=["AWS"],  # Options for cloud providers
    index=0  # Default is "AWS"
)

# Radio buttons for Operating System
selected_os = st.radio(
    "Operating System", 
    options=["Linux", "Windows"], 
    index=0  # Default is "Linux"
)

# Dropdown for CPU cores (vCPU)
selected_vcpu = st.selectbox(
    "Scale CPU Cores (vCPU)", 
    options=[i for i in range(1, 65)],  # Range from 1 to 64 vCPUs
    index=0  # Default is 1 vCPU
)

# Dropdown for RAM (GiB)
selected_ram = st.selectbox(
    "Scale RAM (GiB)", 
    options=[i * 0.5 for i in range(1, 513)],  # Range from 0.5 to 256 GiB in 0.5 increments
    index=0  # Default is 0.5 GiB
)

# Filter instances based on selections
filtered_instances = df[
    (df["vcpu"] == selected_vcpu) &  # Filter for exact vCPU match
    (df["memory"] == selected_ram) &  # Filter for exact memory match
    (df["operatingSystem"] == selected_os)  # Filter for selected OS
]

# Display results
if not filtered_instances.empty:
    st.write(f"### Matching Instance Types: {len(filtered_instances)} Found")
    st.dataframe(
        filtered_instances[["instanceType", "vcpu", "memory", "storage", "operatingSystem"]].rename(
            columns={
                "instanceType": "Instance Type",
                "vcpu": "vCPU",
                "memory": "Memory (GiB)",
                "storage": "Storage",
                "operatingSystem": "Operating System"
            }
        ),
        use_container_width=True
    )
else:
    st.warning("⚠️ No matching instance types found for the specified criteria.")
