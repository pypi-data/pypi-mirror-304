"""
script.py

This script fetches the current IP address of the machine by 
parsing the HTML content of the page http://checkip.dyndns.org/.
Author: Phillip Bridgeman
Date: 2024-10-14
Last Modified: 2024-10-21
Version: 5.3
"""

import urllib.request
from html.parser import HTMLParser
import logging
import argparse

class MyHTMLParser(HTMLParser):
    """
    Custom HTML parser to extract the IP address from the HTML content.
    """
    def __init__(self) -> None:
        super().__init__()
        self.ip: str | None = None

    def handle_data(self, data: str) -> None:
        """Handle the data within the HTML content."""
        if "Current IP Address:" in data:
            parts = data.split(": ")
            if len(parts) > 1:
                self.ip = parts[1].strip()

    def get_ip(self) -> str | None:
        """Return the extracted IP address."""
        return self.ip

def fetch_html(url: str) -> str:
    """Fetch HTML content from the given URL."""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print("Failed to fetch IP address.")
        return ""

def get_ip_address(url: str = 'http://checkip.dyndns.org/') -> str | None:
    """Fetch and return the public IP address."""
    html = fetch_html(url)
    if html:
        parser = MyHTMLParser()
        parser.feed(html)
        return parser.get_ip()
    return None

def log_ip_address(ip: str | None, logger: logging.Logger) -> None:
    """Optional logging function to log the IP address."""
    if ip:
        logger.info("IP Address: %s", ip)
    else:
        logger.info("IP address not found.")

def main():
    """
    Main function to fetch and display the public IP address.
    """
    # Argument parsing for debug flag
    parser = argparse.ArgumentParser(description="Fetch and display the public IP address.")
    parser.add_argument('--debug', action='store_true', help="Enable logging of the IP address.")
    args = parser.parse_args()

    # Fetch the IP address
    ip_address = get_ip_address()

    if ip_address:
        print(f"IP Address: {ip_address}")
    else:
        print("IP address not found.")

    # If --debug flag is passed, configure logging
    if args.debug:
        logger = logging.getLogger(__name__)
        if not logger.hasHandlers():  # Only configure logging if it hasn't been configured
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        log_ip_address(ip_address, logger)

if __name__ == "__main__":
    main()
