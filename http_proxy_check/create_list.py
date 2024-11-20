import os
import requests
import json
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from retrying import retry
import re


# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
FULL_PROXY_LIST = 'full_proxy_list'
READY_LIST = f'ready_list-{datetime.now().strftime("%Y-%m-%d")}'
READY_LIST_BRACK = f'{READY_LIST}-brack'
VALIDATION_URL = 'https://ifconfig.io'
CONNECTION_TIMEOUT = 5  # seconds
MAX_RETRIES = 3
NUM_WORKERS = 10  # For both retrieval and validation
PROXY_SOURCES = [
    'https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt',
    'https://raw.githubusercontent.com/arunsakthivel96/proxyBEE/master/proxy.list',
    'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt',
    'https://raw.githubusercontent.com/Eloco/free-proxy-raw/main/proxy/http_1721038733_iw4p_C171.txt',
    'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt',
    'https://raw.githubusercontent.com/lalifeier/proxy-scraper/main/proxies/http.txt',
    'https://raw.githubusercontent.com/themiralay/Proxy-List-World/master/data.txt',
    'https://raw.githubusercontent.com/Vadim287/free-proxy/main/proxies/http.txt',
    'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt',
    'https://raw.githubusercontent.com/ObcbO/getproxy/master/file/http.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
    'https://raw.githubusercontent.com/TuanMinPay/live-proxy/master/http.txt',
    'https://raw.githubusercontent.com/Vann-Dev/proxy-list/main/proxies/http.txt',
    'https://raw.githubusercontent.com/Siva2webdev/Alive_Proxies/tat/alive_proxies.txt',
    'https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt',
    'https://raw.githubusercontent.com/claude89757/free_https_proxies/main/free_https_proxies.txt',
    'https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/http.txt'
    # Add additional URLs here as needed
]

# Functions
def fetch_proxies_from_url(url):
    """Fetch proxies from a single URL."""
    logging.info(f"Fetching proxies from {url}")
    try:
        response = requests.get(url, timeout=CONNECTION_TIMEOUT)
        response.raise_for_status()
        return response.text.splitlines()
    except Exception as e:
        logging.error(f"Failed to fetch proxies from {url}: {e}")
        return []

def process_proxy_data(data, source_type='plain'):
    """Process raw proxy data into a consistent IP:PORT format."""
    valid_proxies = set()
    invalid_entries = []

    # Regex for matching valid IP:PORT format
    ip_port_pattern = re.compile(r"^\d{1,3}(\.\d{1,3}){3}:\d+$")

    try:
        if source_type == 'plain':
            for line in data:
                stripped_line = line.strip()
                # Extract IP:PORT from lines with extra data
                if ':' in stripped_line:
                    parts = stripped_line.split(':')
                    if len(parts) >= 2 and parts[0].count('.') == 3:  # Ensure the first part is an IP
                        ip_port = f"{parts[0]}:{parts[1]}"
                        valid_proxies.add(ip_port)
                    else:
                        invalid_entries.append(stripped_line)
                else:
                    invalid_entries.append(stripped_line)
        elif source_type == 'json':
            for proxy_data in data:
                try:
                    proxy = json.loads(proxy_data)
                    host_ip = proxy["host"]
                    port = proxy["port"]
                    valid_proxies.add(f"{host_ip}:{port}")
                except Exception:
                    invalid_entries.append(proxy_data)
    except Exception as e:
        logging.error(f"Failed to process proxy data: {e}")

    # Log invalid entries for review
    if invalid_entries:
        logging.warning(f"Found {len(invalid_entries)} invalid entries. Saving to 'invalid_proxies.log'.")
        with open('invalid_proxies.log', 'w') as invalid_file:
            invalid_file.write('\n'.join(invalid_entries))

    return valid_proxies


def fetch_all_proxies():
    """Fetch and consolidate proxies from all sources."""
    consolidated_proxies = set()
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        future_to_url = {executor.submit(fetch_proxies_from_url, url): url for url in PROXY_SOURCES}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                source_type = 'json' if 'proxyBEE' in url else 'plain'
                proxies = process_proxy_data(data, source_type)
                consolidated_proxies.update(proxies)
            except Exception as e:
                logging.error(f"Error processing proxies from {url}: {e}")
    return consolidated_proxies

@retry(stop_max_attempt_number=MAX_RETRIES, wait_fixed=1000)
def validate_proxy(proxy):
    """Validate a single proxy with retry mechanism."""
    try:
        response = requests.get(VALIDATION_URL, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=CONNECTION_TIMEOUT)
        if response.status_code == 200:
            logging.info(f"Valid proxy: {proxy}")
            return True
    except Exception:
        logging.debug(f"Invalid proxy: {proxy}")
    return False

def validate_all_proxies(proxies):
    """Validate proxies concurrently and write results to files."""
    with open(READY_LIST, 'w') as ready_file, open(READY_LIST_BRACK, 'w') as brack_file:
        with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
            future_to_proxy = {executor.submit(validate_proxy, proxy): proxy for proxy in proxies}
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    if future.result():
                        ready_file.write(f"http://{proxy}\n")
                        brack_file.write(f"\"http://{proxy}\",\n")
                except Exception as e:
                    logging.error(f"Error validating proxy {proxy}: {e}")

def main():
    # Step 1: Remove old files
    for file in [FULL_PROXY_LIST, READY_LIST, READY_LIST_BRACK]:
        if os.path.exists(file):
            os.remove(file)

    # Step 2: Fetch and consolidate unique proxies
    proxies = fetch_all_proxies()
    logging.info(f"Fetched {len(proxies)} unique proxies.")
    with open(FULL_PROXY_LIST, 'w') as file:
        file.write('\n'.join(proxies))

    # Step 3: Validate proxies and save results
    logging.info("Starting proxy validation...")
    validate_all_proxies(proxies)
    logging.info("Proxy validation completed.")

if __name__ == "__main__":
    main()
