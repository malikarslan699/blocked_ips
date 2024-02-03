##Python3
import subprocess
import requests

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

def get_asname_and_city(ip_address):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}?fields=asname,city')
        if response.status_code == 200 and response.text.strip():  # Check if response is valid
            data = response.json()
            asname = data.get('asname', 'Error: No AS name')
            city = data.get('city', 'Error: No city')
            return asname, city
        else:
            return "Error: No data available", "Error: No data available"
    except requests.RequestException:
        return "Error: Unable to retrieve AS name", "Error: Unable to retrieve city"

def main():
    active_users = get_active_users()
    network_counts = {}
    print("Active Users:")
    for username, login_time, ip_address in active_users:
        asname, city = get_asname_and_city(ip_address)
        if asname == "EMIRATES-INTERNET":
            asname = "\033[1m\033[32mETISALAT\033[0m"  # Bold and capitalized
            color = '\033[32m'  # Dark Green
        elif asname == "DU-AS1":
            asname = "\033[1m\033[35mDU\033[0m"  # Bold and capitalized
            color = '\033[35m'  # Dark Magenta
        else:
            color = '\033[0m'  # Reset color
        # print(f"Username: {username}, {login_time}, IP: {ip_address}, City: {city}, Network: {color}{asname}\033[0m")
        print(f"{username[:8].ljust(8)} | {login_time.ljust(19)} | {ip_address.ljust(15)} | {city.ljust(15)} | {color}{asname}\033[0m")
        network_counts[asname] = network_counts.get(asname, 0) + 1

    print("\nSummary:")
    total_users = len(active_users)
    print(f"Total Connected users: {total_users}")
    for network, count in network_counts.items():
        print(f"{network} Network: {count}")

  # Include the date command after printing the summary
    subprocess.run(['date'])

if __name__ == "__main__":
    main()
