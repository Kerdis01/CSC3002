# power_monitor.py
import subprocess
import psutil
import time

def get_cpu_usage():
    """Returns the current CPU usage as a percentage."""
    return psutil.cpu_percent(interval=1)

def get_cpu_temperature():
    """Returns the current CPU temperature in Celsius."""
    result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
    temp_str = result.stdout
    try:
        return float(temp_str.split('=')[1].split("'")[0])
    except (IndexError, ValueError):
        return None

def get_core_voltage():
    """Returns the current core voltage in Volts."""
    result = subprocess.run(['vcgencmd', 'measure_volts', 'core'], capture_output=True, text=True)
    volt_str = result.stdout
    try:
        return float(volt_str.split('=')[1].split('V')[0])
    except (IndexError, ValueError):
        return None

def log_system_metrics_to_csv(start_time, frame_counter, csv_writer):
    """Logs system metrics and writes them to a CSV file."""
    cpu_usage = get_cpu_usage()
    cpu_temp = get_cpu_temperature()
    core_voltage = get_core_voltage()
    # Calculate elapsed time in seconds since start
    elapsed_time = time.time() - start_time
    print(f"Frame: {frame_counter}, CPU Usage: {cpu_usage}%, CPU Temperature: {cpu_temp}�C, Core Voltage: {core_voltage}V")
    # Write the metrics to the CSV file
    csv_writer.writerow([frame_counter, elapsed_time, cpu_usage, cpu_temp, core_voltage])