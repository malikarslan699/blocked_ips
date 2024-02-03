###Python3
import subprocess
import json
import requests
from datetime import datetime

def get_active_users():
    active_users_output = subprocess.check_output(['who']).decode().split('\n')
    active_users = []
    for line in active_users_output:
        if line:
            parts = line.split()
            username = parts[0]
            login_time = ' '.join(parts[2:4])  # Modify to use only the third and fourth fields
            ip_address = parts[-1].strip('()')
            active_users.append((username, login_time, ip_address))
    return active_users

def get_asname(ip_address):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}?fields=asname')
        if response.status_code == 200 and response.text.strip():  # Check if response is valid
            data = response.json()
            return data['asname']
        else:
            return "Error: No data available"
    except requests.RequestException:
        return "Error: Unable to retrieve AS name"

def main():
    active_users = get_active_users()
    network_counts = {}
    print("Active Users:")
    for username, login_time, ip_address in active_users:
        asname = get_asname(ip_address)
        if asname == "EMIRATES-INTERNET":
            asname = "ETISALAT"
        elif asname == "DU-AS1":
            asname = "DU"
        color = '\033[32m' if asname == "ETISALAT" else '\033[35m' if asname == "DU" else '\033[0m'
        network = "ETISALAT Network" if asname == "ETISALAT" else "DU Network" if asname == "DU" else "Unknown Network"
        print(f"Username: {username}, {login_time}, IP: {ip_address}, Network: {color}{network}\033[0m")
        network_counts[network] = network_counts.get(network, 0) + 1

    print("\nSummary:")
    total_users = len(active_users)
    print(f"Total Connected users: {total_users}")
    for network, count in network_counts.items():
        print(f"{network}: {count}")

if __name__ == "__main__":
    main()
