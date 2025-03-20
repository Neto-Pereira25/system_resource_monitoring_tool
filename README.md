# Resource Watchdog

A Streamlit application for monitoring system resources (CPU, memory, disk) in real-time.

## Features

- Real-time monitoring of CPU usage (overall and per-core)
- Memory usage tracking with detailed metrics
- Disk usage analysis across all partitions
- Historical data visualization with interactive charts
- Customizable update interval and history length

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run app.py
```

## Usage

1. Open the application in your web browser (typically at http://localhost:8501)
2. Use the sidebar to adjust settings:
   - Update interval: How frequently the data refreshes (in seconds)
   - History length: How many data points to keep in the historical charts

3. View real-time metrics:
   - Main dashboard shows current CPU, memory and disk usage with gauges
   - Detailed tabs provide historical trends and additional metrics
   - CPU tab shows per-core usage
   - Memory tab displays detailed memory statistics
   - Disk tab provides usage breakdown by partition

## Requirements

- Python 3.7+
- Streamlit
- psutil
- plotly
- pandas

## License

This project is open source and available under the MIT License.