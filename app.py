import streamlit as st
import psutil
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os

# Set page configuration
st.set_page_config(
    page_title="System Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for history data
if 'cpu_history' not in st.session_state:
    st.session_state.cpu_history = []
if 'memory_history' not in st.session_state:
    st.session_state.memory_history = []
if 'disk_history' not in st.session_state:
    st.session_state.disk_history = []
if 'timestamps' not in st.session_state:
    st.session_state.timestamps = []

# Maximum history points to store
MAX_HISTORY_POINTS = 60

# Function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=0.5)

# Function to get memory usage
def get_memory_usage():
    memory = psutil.virtual_memory()
    return {
        'total': memory.total / (1024 ** 3),  # GB
        'used': memory.used / (1024 ** 3),    # GB
        'percent': memory.percent
    }

# Function to get disk usage
def get_disk_usage():
    partitions = []
    for partition in psutil.disk_partitions():
        if os.name == 'nt' and ('cdrom' in partition.opts or partition.fstype == ''):
            # Skip CD-ROM drives on Windows
            continue
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            partitions.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'total': usage.total / (1024 ** 3),  # GB
                'used': usage.used / (1024 ** 3),    # GB
                'percent': usage.percent
            })
        except PermissionError:
            # This can happen if the disk isn't ready
            continue
    return partitions

# Title and description
st.title("🖥️ System Resource Monitor")
st.markdown("""
This dashboard monitors your system's CPU, memory, and disk usage in real-time.
""")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["Overview", "History", "Details"])

# Overview tab
with tab1:
    # Create three columns for CPU, Memory, and Disk
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("CPU Usage")
        cpu_usage = get_cpu_usage()
        st.session_state.cpu_history.append(cpu_usage)
        cpu_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=cpu_usage,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "CPU %"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgreen"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ]
            }
        ))
        st.plotly_chart(cpu_gauge, use_container_width=True)
    
    with col2:
        st.subheader("Memory Usage")
        memory_usage = get_memory_usage()
        st.session_state.memory_history.append(memory_usage['percent'])
        memory_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=memory_usage['percent'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Memory % (Used: {memory_usage['used']:.2f} GB / Total: {memory_usage['total']:.2f} GB)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgreen"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ]
            }
        ))
        st.plotly_chart(memory_gauge, use_container_width=True)
    
    with col3:
        st.subheader("Disk Usage")
        disk_usages = get_disk_usage()
        total_disk_percent = sum(disk['percent'] for disk in disk_usages) / len(disk_usages) if disk_usages else 0
        st.session_state.disk_history.append(total_disk_percent)
        
        disk_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total_disk_percent,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Avg Disk %"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgreen"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ]
            }
        ))
        st.plotly_chart(disk_gauge, use_container_width=True)
        
        # Display disk details in a table
        st.write("Disk Details:")
        disk_data = []
        for disk in disk_usages:
            disk_data.append({
                "Device": disk['device'],
                "Mount Point": disk['mountpoint'],
                "Total (GB)": f"{disk['total']:.2f}",
                "Used (GB)": f"{disk['used']:.2f}",
                "Usage %": f"{disk['percent']:.2f}%"
            })
        st.dataframe(pd.DataFrame(disk_data), use_container_width=True)

# Add current timestamp
st.session_state.timestamps.append(datetime.now().strftime("%H:%M:%S"))

# Keep only the most recent MAX_HISTORY_POINTS
if len(st.session_state.cpu_history) > MAX_HISTORY_POINTS:
    st.session_state.cpu_history = st.session_state.cpu_history[-MAX_HISTORY_POINTS:]
    st.session_state.memory_history = st.session_state.memory_history[-MAX_HISTORY_POINTS:]
    st.session_state.disk_history = st.session_state.disk_history[-MAX_HISTORY_POINTS:]
    st.session_state.timestamps = st.session_state.timestamps[-MAX_HISTORY_POINTS:]

# History tab
with tab2:
    st.subheader("Resource Usage History")
    
    # Prepare data for plotting
    df = pd.DataFrame({
        'Timestamp': st.session_state.timestamps,
        'CPU (%)': st.session_state.cpu_history,
        'Memory (%)': st.session_state.memory_history,
        'Disk (%)': st.session_state.disk_history
    })
    
    # Create a line chart for history
    fig = px.line(
        df, 
        x='Timestamp', 
        y=['CPU (%)', 'Memory (%)', 'Disk (%)'],
        labels={'value': 'Usage (%)', 'variable': 'Resource'},
        title='System Resource Usage Over Time'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Show the raw data
    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)

# Details tab
with tab3:
    st.subheader("Process Information")
    
    # Get process information
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
        try:
            processes.append({
                'PID': proc.info['pid'],
                'Name': proc.info['name'],
                'User': proc.info['username'],
                'Memory %': proc.info['memory_percent'],
                'CPU %': proc.info['cpu_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Convert to DataFrame and sort by CPU usage
    processes_df = pd.DataFrame(processes)
    if not processes_df.empty:
        processes_df = processes_df.sort_values(by='CPU %', ascending=False)
        
        # Add search functionality
        search_term = st.text_input("Search processes by name:")
        if search_term:
            filtered_df = processes_df[processes_df['Name'].str.contains(search_term, case=False)]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.dataframe(processes_df, use_container_width=True)
    else:
        st.info("Unable to retrieve process information.")

# Add auto-refresh button
refresh_interval = st.sidebar.slider(
    "Auto-refresh interval (seconds)", 
    min_value=1, 
    max_value=60, 
    value=5
)

st.sidebar.write(f"Dashboard will refresh every {refresh_interval} seconds")

# System information in sidebar
st.sidebar.title("System Information")
st.sidebar.info(f"""
- **OS**: {os.name.upper()}
- **CPU Cores**: {psutil.cpu_count(logical=False)} (Physical), {psutil.cpu_count(logical=True)} (Logical)
- **Total Memory**: {psutil.virtual_memory().total / (1024**3):.2f} GB
- **Boot Time**: {datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")}
""")

# Add refresh button
if st.sidebar.button("Refresh Now"):
    st.rerun()

# Create auto-refresh
time.sleep(refresh_interval)
st.rerun()  # Use st.rerun() instead of st.experimental_rerun()