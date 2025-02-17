import psutil
import subprocess
import re


# Store previous values to detect changes
previous_values = {
    "CPU_Scheduler_Limit": None,
    "CPU_Available_CPUs": None,
    "CPU_Speed_Limit": None
}

def get_cpu_usage():
    """ Get usage of each CPU core """
    return psutil.cpu_percent(interval=1, percpu=True)

def get_ram_usage():
    """ Get total and used RAM in GB """
    ram = psutil.virtual_memory()
    total_ram = round(ram.total / (1024 ** 3), 2)  # Convert bytes to GB
    used_ram = round(ram.used / (1024 ** 3), 2)    # Convert bytes to GB
    return f"{used_ram} GB / {total_ram} GB"


def thermal_throttling():
    """ Fetch CPU throttling status from macOS `pmset -g therm` """
    try:
        # Run pmset command
        therm_cmd = subprocess.run(["pmset", "-g", "therm"], capture_output=True, text=True)
        output = therm_cmd.stdout.strip()

        # Extract key values using regex
        scheduler_match = re.search(r'CPU_Scheduler_Limit\s+=\s+(\d+)', output)
        available_cpus_match = re.search(r'CPU_Available_CPUs\s+=\s+(\d+)', output)
        speed_limit_match = re.search(r'CPU_Speed_Limit\s+=\s+(\d+)', output)

        scheduler_limit = int(scheduler_match.group(1)) if scheduler_match else "N/A"
        available_cpus = int(available_cpus_match.group(1)) if available_cpus_match else "N/A"
        speed_limit = int(speed_limit_match.group(1)) if speed_limit_match else "N/A"

        # Check if any value changed
        changes = []
        for key, new_value in [("CPU_Scheduler_Limit", scheduler_limit),
                               ("CPU_Available_CPUs", available_cpus),
                               ("CPU_Speed_Limit", speed_limit)]:
            if previous_values[key] is not None and previous_values[key] != new_value:
                changes.append(f"⚠️ {key} changed: {previous_values[key]} → {new_value}")
            previous_values[key] = new_value  # Update stored value

        # Format the response
        response = {
            "CPU_Scheduler_Limit": scheduler_limit,
            "CPU_Available_CPUs": available_cpus,
            "CPU_Speed_Limit": speed_limit,
            "Changes": changes if changes else "No changes detected"
        }

        return response

    except Exception as e:
        return {"error": str(e)}

def get_fan_speed():
    """ Get fan speed in RPM and percentage of max speed """
    try:
        fan_cmd = subprocess.run(["pmset", "-g", "therm"], capture_output=True, text=True)
        fan_speed_match = re.search(r'Fan: (\d+) rpm', fan_cmd.stdout)
        if fan_speed_match:
            fan_speed_rpm = int(fan_speed_match.group(1))
            max_fan_speed = 6000  # Assuming 6000 RPM is max speed
            fan_percentage = round((fan_speed_rpm / max_fan_speed) * 100, 1)
            return f"{fan_speed_rpm} RPM ({fan_percentage}%)"
        return "N/A"
    except:
        return "N/A"

def get_system_stats():
    """ Fetch system resource stats """
    try:
        return {
            "cpu_usage": get_cpu_usage(),
            "ram_usage": get_ram_usage(),
            "cpu_temp": thermal_throttling(),
            "fan_speed": "Function not available"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(get_system_stats())  # Test script