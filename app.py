%%writefile app.py
import streamlit as st
import pandas as pd

# Load AWS pricing data
csv_file = "aws_pricing_filtered.csv"  # Ensure this file is in the same directory
df = pd.read_csv(csv_file)

# Data Cleaning
df["vcpu"] = pd.to_numeric(df["vcpu"], errors="coerce")  # Convert vCPU column to numeric
df["memory"] = df["memory"].str.replace(" GiB", "").astype(float)  # Remove " GiB" and convert to numeric

# Filter for Malaysia region (ap-southeast-5)
filtered_df = df[df["regionCode"] == "ap-southeast-5"]

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

# Extract unique operating systems dynamically and add "Any" option
available_os = ["Any"] + filtered_df["operatingSystem"].dropna().unique().tolist()

# Radio buttons for OS (Dynamic based on dataset)
selected_os = st.radio("Operating System", available_os)

# Dropdown for scaling CPU cores, with "Any" as an option
selected_vcpu = st.selectbox(
    "Scale CPU Cores (vCPU)", 
    options=["Any"] + [i for i in range(1, 65)]  # Add "Any" option
)

# Dropdown for scaling RAM, with "Any" as an option
selected_ram = st.selectbox(
    "Scale RAM (GiB)", 
    options=["Any"] + [i * 0.5 for i in range(1, 513)]  # Add "Any" option
)

# Location selection
location = st.text_input("Location", "AP Southeast")

st.markdown("</div>", unsafe_allow_html=True)

# Filter instances based on user input
if selected_vcpu == "Any":
    vcpu_filter = filtered_df["vcpu"] >= 0  # Select all vCPU values
else:
    vcpu_filter = filtered_df["vcpu"] >= int(selected_vcpu)

if selected_ram == "Any":
    ram_filter = filtered_df["memory"] >= 0  # Select all memory values
else:
    ram_filter = filtered_df["memory"] >= float(selected_ram)

if selected_os == "Any":
    os_filter = filtered_df["operatingSystem"].notnull()  # Include all OS
else:
    os_filter = filtered_df["operatingSystem"] == selected_os

filtered_instances = filtered_df[
    vcpu_filter & 
    ram_filter & 
    os_filter & 
    (filtered_df["marketoption"] == "OnDemand")  # Filter for "OnDemand" pricing
]

# Display results in a table
if not filtered_instances.empty:
    st.write(f"### Matching Instances: {len(filtered_instances)} Found")
    st.dataframe(
        filtered_instances[["instanceType", "vcpu", "memory", "storage", "operatingSystem", "marketoption"]].rename(
            columns={
                "instanceType": "Instance Type",
                "vcpu": "vCPU",
                "memory": "Memory (GiB)",
                "storage": "Storage",
                "operatingSystem": "Operating System",
                "marketoption": "Market Option (Pricing)"
            }
        ),
        use_container_width=True
    )
else:
    st.warning("⚠️ No instances match your criteria. Try adjusting your filters.")