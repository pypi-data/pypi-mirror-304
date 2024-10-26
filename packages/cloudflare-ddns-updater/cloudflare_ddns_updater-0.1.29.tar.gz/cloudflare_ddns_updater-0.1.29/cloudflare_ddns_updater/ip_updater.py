from requests import get, request
import os
import json
import logging
from cloudflare_ddns_updater.constants import *


CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE)

# Configure logging
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def counter(r):
    # TODO error handling what if: c is not  numeric, is empty, is more lines
    try:
        with open(COUNTER_PATH) as t:
            c = int(t.read().strip())
            if c <= 0:
                os.remove(CURRENT_IP_PATH)
                c = int(r)
                logging.info(f"Scheduled forced IP update. {CURRENT_IP_PATH} removed.")
            c -= 1
        with open(COUNTER_PATH, 'w') as t:
            t.write(str(c))
    except FileNotFoundError:
        with open(COUNTER_PATH, 'w') as t:
            t.write(r)
        logging.info(f"Created new counter file with {r} runs.")


def main():
    # Load the configuration from the JSON file
    try:
        with open(CONFIG_FILE_PATH) as config_file:
            config = json.load(config_file)
        zone_id = config['ZONE_ID']
        dns_record_id = config['DNS_RECORD_ID']
        api_token = config['API_TOKEN']
        runs = config['FORCE_IP']
    except Exception as e:
        print(f"Failed to load configuration.\nPlease run cloudflare-ddns-updater --setup")
        logging.error(f"Failed to load configuration: {e}")
        exit(1)

    # Try to read the current IP from the file
    try:
        with open(CURRENT_IP_PATH) as t:
            old_ip = t.read().strip()  # Strip any extra whitespace or newlines
    except FileNotFoundError:
        old_ip = "none"
        with open(CURRENT_IP_PATH, 'w') as t:
            t.write(old_ip)
        logging.info(f"Created new {CURRENT_IP_PATH} with placeholder IP 'none'.")

    # Try to get the current public IP
    try:
        ip = get('https://api.ipify.org').text.strip()
        logging.info(f"Successfully retrieved current IP: {ip}")
    except Exception as e:
        ip = "error"
        logging.error(f"Error occurred while fetching IP from ipify: {e}")

    # Compare old IP with current IP
    if ip == old_ip:
        counter(runs)
        logging.info("No IP change detected.")
    elif ip == "error":
        logging.error("Unable to retrieve the current IP")
    else:
        logging.info(f"New IP detected: {ip}")

        # Cloudflare DNS update payload
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}"
        payload = {
            "content": f"{ip}"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        }

        # Attempt to update Cloudflare
        try:
            response = request("PATCH", url, json=payload, headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors
            r = response.json()

            # Check if the update was successful
            if r['success']:
                cloudflare_ip = r['result']['content']
                logging.info(f"Cloudflare IP successfully updated to: {cloudflare_ip}")

                # If the IP matches, update the local file
                if cloudflare_ip == ip:
                    with open(CURRENT_IP_PATH, 'w') as t:
                        t.write(ip)
                    logging.info(f"Updated local IP file {CURRENT_IP_PATH} with IP: {ip}")
            else:
                logging.error(f"Error updating Cloudflare: {r['errors']}")

        except Exception as e:
            logging.error(f"Error occurred during Cloudflare update: {e}")


if __name__ == "__main__":
    main()


