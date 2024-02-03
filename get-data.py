import subprocess
import requests
from datetime import datetime

def get_active_users():
    active_users_output = subprocess.check_output(['who']).decode().split('\n')
    active_users = []
    for line in active_users_output:
        if line:
            parts = line.split()
            username = parts[0]
            login_time = ' '.join(parts[2:5])
            ip_address = parts[-1].strip('()')
            active_users.append((username, login_time, ip_address))
    return active_users

def get_location(ip_address):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}?fields=city')
        if response.status_code == 200 and response.text.strip():  
            data = response.json()
            return data['city']
        else:
            return "Error: No data available"
    except requests.RequestException:
        return "Error: Unable to retrieve city"

def main():
    active_users = get_active_users()
    print("Active Users:")
    for username, login_time, ip_address in active_users:
        city = get_location(ip_address)
        print(f"Username: {username}, Login Time: {login_time}, IP: {ip_address}, City: {city}")

if __name__ == "__main__":
    main()
