import streamlit as st
import pandas as pd

# Load AWS pricing data
csv_file = "aws_pricing_filtered.csv"  # Ensure this file is in the same directory
df = pd.read_csv(csv_file)

# Data Cleaning
df["vcpu"] = pd.to_numeric(df["vcpu"], errors="coerce")  # Convert vCPU column to numeric
df["memory"] = df["memory"].str.replace(" GiB", "").astype(float)  # Remove " GiB" and convert to numeric

# Streamlit UI settings
st.set_page_config(page_title="AWS Instance Recommendation", layout="wide")

# Header Update
st.markdown(
    """
    <style>
    .header-title {
        font-size: 2.5em;
        font-weight: bold;
        color: black;
        text-align: center;
    }
    .gradient-blue {
        color: #007BFF;
    }
    .container {
        background-color: #F8F9FA;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .filter-label {
        font-weight: bold;
        font-size: 1.2em;
        color: black;
    }
    .table-header {
        font-size: 1.3em;
        font-weight: bold;
        color: black;
    }
    </style>
    <h1 class="header-title">
        AWS Instance Recommendation
    </h1>
    """,
    unsafe_allow_html=True
)

# Filter section
st.markdown('<div class="container">', unsafe_allow_html=True)
st.subheader("Filter Options")

# Dropdown for Cloud Provider
selected_provider = st.selectbox("Cloud Provider", ["AWS"], index=0)

# Dropdown for Location (filter dynamically)
location_options = df["regionCode"].dropna().unique().tolist()
selected_location = st.selectbox("Location", ["Any"] + location_options)

# Filter dynamically based on user selection
filtered_df = df.copy()

if selected_location != "Any":
    filtered_df = filtered_df[filtered_df["regionCode"] == selected_location]

os_options = filtered_df["operatingSystem"].dropna().unique().tolist()
selected_os = st.selectbox("Operating System", ["Any"] + os_options)

if selected_os != "Any":
    filtered_df = filtered_df[filtered_df["operatingSystem"] == selected_os]

vcpu_options = sorted(filtered_df["vcpu"].unique())
selected_vcpu = st.selectbox("Scale CPU Cores (vCPU)", ["Any"] + vcpu_options)

if selected_vcpu != "Any":
    filtered_df = filtered_df[filtered_df["vcpu"] >= int(selected_vcpu)]

ram_options = sorted(filtered_df["memory"].unique())
selected_ram = st.selectbox("Scale RAM (GiB)", ["Any"] + ram_options)

if selected_ram != "Any":
    filtered_df = filtered_df[filtered_df["memory"] >= float(selected_ram)]

st.markdown("</div>", unsafe_allow_html=True)

# Filter instances based on user input
filtered_instances = filtered_df[filtered_df["marketoption"] == "OnDemand"]  # Filter for "OnDemand" pricing

# Display results in a table
if not filtered_instances.empty:
    st.write(f"### Matching Instances: {len(filtered_instances)} Found")
    st.dataframe(
        filtered_instances[["instanceType", "vcpu", "memory", "storage", "operatingSystem", "regionCode", "marketoption"]].rename(
            columns={
                "instanceType": "Instance Type",
                "vcpu": "vCPU",
                "memory": "Memory (GiB)",
                "storage": "Storage",
                "operatingSystem": "Operating System",
                "regionCode": "Location",
                "marketoption": "Market Option (Pricing)"
            }
        ),
        use_container_width=True
    )
else:
    st.warning("⚠️ No instances match your criteria. Try adjusting your filters.")