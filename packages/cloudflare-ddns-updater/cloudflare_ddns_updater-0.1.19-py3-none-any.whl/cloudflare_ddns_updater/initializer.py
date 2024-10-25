import argparse
import json
import os
import shutil
import sys
import requests
from crontab import CronTab

# TODO Use crontab library


# If you change the following settings, config_file_path in ip_updater.py must also be updated
config_dir = '/etc/ip_updater'
config_file = 'cloudflare_config.json'
config_file_path = os.path.join(config_dir, config_file)
cron_comment = "# Cloudflare DDNS ip-updater"

# Define the log file path
log_file_path = '/var/log/ip_update.log'


def delete_cron_job():
    # Access the user's crontab
    cron = CronTab(user=True)
    # Remove the found jobs
    for job in cron:
        if job.comment == cron_comment:
            print(f"Removed cron job: {job}")
            cron.remove(job)
            cron.write()
            return
    print("No cron jobs to remove")
    return


def cleanup():
    shutil.rmtree('/etc/ip_updater', ignore_errors=True)
    try:
        os.remove('/var/log/ip_update.log')
    except:
        pass
    try:
        os.remove('/tmp/counter.txt')
    except:
        pass
    try:
        os.remove('/tmp/current_ip.txt')
    except:
        pass
    delete_cron_job()
    print('Now uninstall package using "pip (or pipx) uninstall cloudflare-ddns-updater"')
    return


def create_log_file():
    # Check if the log file exists
    if not os.path.exists(log_file_path):
        print(f"Creating log file {log_file_path}.")
        # Create the log file
        try:
            with open(log_file_path, 'w') as log_file:
                log_file.write("IP update log initiated.\n")
            # Set file permissions to ensure it's writeable (if needed)
            # os.chmod(log_file_path, 0o644)  # rw-r--r--
            print(f"Log file {log_file_path} created successfully.")
        except PermissionError:
            print(f"Permission denied. Cannot create {log_file_path}. Please run with appropriate privileges.")
            sys.exit()
    else:
        print(f"Log file is {log_file_path}.")


def find_ip_updater():
    # Find the full path of 'ip-updater' command
    ip_updater_path = shutil.which('ip-updater')
    if not ip_updater_path:
        print("ip-updater command not found. Try a fresh installation.")
        sys.exit(1)
    return ip_updater_path


def update_json_with_force_ip(fi):
    # Check if the file exists
    if os.path.exists(config_file_path):
        # Load existing JSON data
        with open(config_file_path, 'r') as json_file:
            config_data = json.load(json_file)

        # Update the dictionary with the new key-value pair
        config_data["FORCE_IP"] = fi

        # Write the updated dictionary back to the JSON file
        with open(config_file_path, 'w') as json_file:
            json.dump(config_data, json_file)
        print("Updated JSON file with FORCE_IP value.")
    else:
        print("JSON file not found. Please ensure the configuration file is created.")


def manage_cron_job():
    # Check if the config file exists, otherwise you haven't run --setup yet
    if not os.path.exists(config_file_path):
        print(f"Please run 'cloudflare-ddns-updater --setup'")
        sys.exit()
    # Ask for and validate cron interval
    valid = False
    while not valid:
        cron_interval = input("How often in minutes do you want to check your IP address? (Default is 2, max 59): ")
        if cron_interval == "":
            cron_interval = "2"
        if cron_interval.isnumeric() and int(cron_interval) in range(1, 59):
            # print(f"script will run every {cron_interval} minutes")
            valid = True
        else:
            print("\nNo, seriously...")

    # Ask for and validate Force update interval
    valid = False
    while not valid:
        force_interval = input("After how many days would you like to force an IP update? (default is 1) ")
        if force_interval == "":
            force_interval = "1"
        if force_interval.isnumeric() and int(force_interval) in range(1, 366):
            print(f"IP address will be forced every {force_interval} days.")
            # Calculate force interval in runs
            force_after_runs = int(int(force_interval) * 1440 / int(cron_interval))  # / creates a float. we want an int
            force_after_runs = str(force_after_runs)
            update_json_with_force_ip(force_after_runs)
            valid = True
        else:
            print("\nNo, seriously...")

    # Get the full path of ip-updater
    ip_updater_path = find_ip_updater()
    # Delete old cron job
    delete_cron_job()
    # Create new cron job
    cron = CronTab(user=True)
    job = cron.new(command=f"{ip_updater_path} >> /var/log/ip_update.log 2>&1", comment=cron_comment)
    job.minute.every(cron_interval)
    print("Cron job added/updated successfully.")


def run_setup():
    print("\nThis script fetches the Zone ID and the dns record ID from yor Cloudflare account.\n"
          "\nBefore running this script you must login to Cloudflare\n"
          "and create a Token with the following Permissions:\n"
          "Zone - Zone - Read\nZone - DNS - Edit\n"
          "and the following Zone Resources:\nInclude - Specific zone - yourdomain.xx")
    print("You must also create an A record (whatever.yourdomain.xx)")
    print("\nThis script only needs to be run once.\n"
          "After running it, you can run ip_updater (using crontab, if you wish)")
    if input("Do you have your token? y or n: ").lower() != "y":
        print("Once you have the token run this script again. see you later!")
        sys.exit()

    api_token = input("Input your Cloudflare token\n")
    dns_record = input("For what record do you want to manage dns? (for example vpn.yourdomain.com)\n")

    # Create directory for config file
    try:
        os.makedirs(config_dir, exist_ok=True)  # Create the directory if it doesn't exist
    except Exception as e:
        print(f"Something went wrong! {e}")
        sys.exit()

    # Get zone id
    url = "https://api.cloudflare.com/client/v4/zones"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    try:
        response = requests.request("GET", url, headers=headers)
        r = response.json()
        zone_id = r['result'][0]['id']
        print(f"zone id is: {zone_id}")
    except Exception as e:
        print(f"Error occurred during retrieval of zone id.\n"
              f"Make sure that your token is correct\n"
              f"and that it has the correct permissions.\n{e}")
        sys.exit()

    # Get dns record id
    try:
        dns_records = f"{url}/{zone_id}/dns_records"
        response = requests.request("GET", dns_records, headers=headers)
        d = response.json()["result"]
        dns_record_id = "none"
        for i in range(len(d)):
            if d[i]["name"] == dns_record:
                dns_record_id = d[i]["id"]
                print(f'dns record id is: {dns_record_id}')
        if dns_record_id == "none":
            print(f"I could not find {dns_record} in your Zone")
            print("The A records in your Zone are:")
            for i in range(len(d)):
                if d[i]["type"] == "A":
                    print(f'  {d[i]["name"]}')
            print("Please run this script again with an existing record.")
            sys.exit()
    except Exception as e:
        print(f"Something went wrong: {e}")
        sys.exit()

    # Create dictionary with data
    data = {
        "ZONE_ID": zone_id,
        "DNS_RECORD_ID": dns_record_id,
        "API_TOKEN": api_token,
    }

    # Write the data to a JSON file
    with open(config_file_path, 'w') as cf:
        json.dump(data, cf)

    create_log_file()
    manage_cron_job()


def main():
    parser = argparse.ArgumentParser(description="Cloudflare DDNS Updater")
    parser.add_argument('--setup', action='store_true', help="Run the setup process.")
    parser.add_argument('--cron', action='store_true', help="Update the cron job.")
    parser.add_argument('--cleanup', action='store_true', help="Cleanup files before uninstalling")

    args = parser.parse_args()

    if args.setup:
        run_setup()  # Replace this with the actual setup function
    elif args.cron:
        manage_cron_job()  # This will just update the cron job
    elif args.cleanup:
        cleanup()  # This will cancel the cron job
    else:
        print("Please provide either --setup, --cron or --cleanup.")


# The following ensures that when the user runs `cloudflare-ddns-updater`, the main function will be called.
if __name__ == "__main__":
    main()
