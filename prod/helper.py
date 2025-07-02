import subprocess
import re
from datetime import datetime


"""
Function: `helper_wan_ping(ip_address)`
Utility: Pings a given IP address and returns the round-trip time in milliseconds as a string.
Input: IP Address in the format XX.XX.XX.XX
Output: `XX ms` or `-1 ms`, Target variable: null
"""
def helper_wan_ping(ip_address):
    try:
        result = subprocess.run(
            ["ping", "-c", "2", ip_address],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            match = re.search(r'time[=<]([\d\.]+)\s*ms', result.stdout)
            if match:
                return [match.group(1)]
            else:
                return ["-1"]
        else:
            return ["-1"]
    except Exception as e:
        return ["-1"]

# TEST
#print(helper_wan_ping("1.1.1.1"))


"""
Function: `get_lines()`
Utility: Reads WAN speed test results from a CSV file and returns them as a set of lines.
Input: null
Output: `Set`, Target variable: `last_seen_lines`
"""

def helper_wan_speed_periodic(target_csv):
    try:
        with open(target_csv, "r") as f:
            return set(f.readlines())
    except FileNotFoundError:
        return set()

# TEST
#print(helper_wan_speed_periodic("wan_speed.csv"))


"""
Function: `helper_wan_speed_ondemand(server_id="")`
Utility: Runs a speed test using the specified server ID (if provided) and returns the latency, upload, and download speeds as a formatted string with date and time.
Input: Optional server ID as a string.
Output: [date, time, latency, upload, download] or failure["meta"]
"""
def helper_wan_speed_ondemand(server_id):
    try:
        result = subprocess.run(
            ["speedtest", "--server", server_id, "--simple"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        date = datetime.now().strftime("%d.%m.%Y")
        time_str = datetime.now().strftime("%H:%M")
        if result.returncode == 0:
            # Extracting latency, download, and upload speeds using regex
            latency_match = re.search(r'Ping:\s*([\d\.]+)\s*ms', result.stdout)
            upload_match = re.search(r'Upload:\s*([\d\.]+)\s*Mbit/s', result.stdout)
            download_match = re.search(r'Download:\s*([\d\.]+)\s*Mbit/s', result.stdout)
            # Formatting the output
            out_latency = f"{latency_match.group(1)} ms" if latency_match else -1
            out_upload = f"{upload_match.group(1)} Mbit/s" if upload_match else -1
            out_download = f"{download_match.group(1)} Mbit/s" if download_match else -1
            # Returning the formatted string
            return [date, time_str, out_latency, out_upload, out_download]
        else:
            return ["-1", "-1", "-1", "-1", "-1"]
    except Exception:
        return ["-1", "-1", "-1", "-1", "-1"]

# TEST
#print(helper_wan_speed_ondemand("12221"))