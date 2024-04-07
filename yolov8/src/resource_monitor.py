import subprocess
import psutil

def get_cpu_usage():
    """Returns the current CPU usage as a percentage, formatted to two decimal places."""
    usage = psutil.cpu_percent(interval=1)
    return f"{usage:.2f}"

def get_cpu_temperature():
    """Returns the current CPU temperature in Celsius, formatted to two decimal places."""
    result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
    temp_str = result.stdout
    try:
        temp = float(temp_str.split('=')[1].split("'")[0])
        return f"{temp:.2f}"
    except (IndexError, ValueError):
        return None

def get_core_voltage():
    """Returns the current core voltage in Volts, formatted to two decimal places."""
    result = subprocess.run(['vcgencmd', 'measure_volts', 'core'], capture_output=True, text=True)
    volt_str = result.stdout
    try:
        voltage = float(volt_str.split('=')[1].split('V')[0])
        return f"{voltage:.2f}"
    except (IndexError, ValueError):
        return None
