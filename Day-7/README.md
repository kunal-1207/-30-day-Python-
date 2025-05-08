# CPU Usage Monitoring Script

## Description

This script monitors CPU usage and provides an alert when CPU usage exceeds 80%. It leverages the `psutil` library, which provides an interface for retrieving information about system utilization, such as CPU, memory, disks, network, and more.

## Prerequisites

* Python 3.x installed
* `psutil` library installed (Install using `pip install psutil`)

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install the `psutil` library by running:

   ```bash
   pip install psutil
   ```

## Usage

To run the script, execute the following command:

```bash
python cpu_monitor.py
```

## Code Breakdown

```python
# Import the psutil library
import psutil
```

* This line imports the `psutil` library, which provides access to system-level information like CPU, memory, and disk usage.

```python
# Get the CPU usage percentage over a 1-second interval
cpu = psutil.cpu_percent(interval=1)
```

* `psutil.cpu_percent(interval=1)` measures the CPU usage over a 1-second interval and stores it in the `cpu` variable.

```python
# Check if CPU usage is greater than 80%
if cpu > 80:
    print(f"ALERT! High CPU usage: {cpu}%")
```

* This conditional statement checks if the CPU usage exceeds 80%.
* If it does, it prints an alert message showing the current CPU usage percentage.

```python
else:
    print(f"CPU OK: {cpu}%")
```

* If CPU usage is 80% or below, a confirmation message is printed indicating that the CPU usage is normal.

## Example Output

```
ALERT! High CPU usage: 85.3%
```

or

```
CPU OK: 42.7%
```

## Future Enhancements

* Implement logging to record CPU usage over time.
* Send alerts via email or SMS.
* Integrate with system monitoring tools for advanced tracking.

## Author

Created as part of Day 7 challenge focusing on the `psutil` library.
