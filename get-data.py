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
    # Sort the active users by login time
    active_users.sort(key=lambda x: x[1])  # Sort based on the second element (login_time)
    return active_users

def get_organization_and_city(ip_address):
    try:
        response = requests.get(f'https://get.geojs.io/v1/ip/geo/{ip_address}.json')
        if response.status_code == 200:
            data = response.json()
            organization = data.get('organization', 'Error: No organization name')
            organization_name = data.get('organization_name', 'Error: No organization name')
            city = data.get('city', 'Error: No city')
            return organization, organization_name, city
        else:
            return "Error: No data available", "Error: No data available", "Error: No data available"
    except requests.RequestException:
        return "Error: Unable to retrieve organization name", "Error: Unable to retrieve organization name", "Error: Unable to retrieve city"

def main():
    active_users = get_active_users()
    network_counts = {}
    for username, login_time, ip_address in active_users:
        organization, organization_name, city = get_organization_and_city(ip_address)
        if "Emirates Telecommunications Group Company (Etisalat) Pjsc" in organization_name or "AS5384 Emirates Telecommunications Group Company (Etisalat Group) Pjsc" in organization:
            organization = "\033[1m\033[32mETISALAT\033[0m"  # Bold and Dark Green
            color = '\033[32m'  # Dark Green
        elif "Emirates Integrated Telecommunications Company PJSC" in organization_name or "AS15802 Emirates Integrated Telecommunications Company PJSC" in organization:
            organization = "\033[1m\033[35mDU\033[0m"  # Bold and Magenta
            color = '\033[35m'  # Magenta
        else:
            color = '\033[0m'  # Reset color
        print(f"{username[:8].ljust(8)} | {login_time.ljust(19)} | {ip_address.ljust(15)} | {city.ljust(15)} | {color}{organization}\033[0m")
        network_counts[organization] = network_counts.get(organization, 0) + 1

    print("\nSummary:")
    total_users = len(active_users)
    print(f"Total Connected users: {total_users}")
    for network, count in network_counts.items():
        if network == "\033[1m\033[32mETISALAT\033[0m":
            network_name = "ETISALAT"
        elif network == "\033[1m\033[35mDU\033[0m":
            network_name = "DU"
        else:
            network_name = network
        print(f"{network_name} Network: {count}")

    subprocess.run(['date'])

if __name__ == "__main__":
    main()
