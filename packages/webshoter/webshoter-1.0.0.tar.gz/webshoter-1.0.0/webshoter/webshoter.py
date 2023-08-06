import argparse
import sys
import os
from utils import get_host_by_url, get_bgp_toolkit, download_screenshot, banner, generate_html_report
from huepy import *

def main():
    print('\033c')
    print(banner())
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output directory", required=True)
    urls = []

    # Check if there is data piped into the script
    if not sys.stdin.isatty():
        urls = sys.stdin.read().splitlines()
    else:
        # Read cli arguments
        parser.add_argument("-u", "--url", help="URL to take screenshot of")
        args = parser.parse_args()

        # Filter out the url
        urls.append(args.url)

    # Check if output directory exists
    if not os.path.exists(parser.parse_args().output):
        os.makedirs(parser.parse_args().output)

    # Take screenshot for each URL
    for url in urls:
        try:
            # Get url host
            host = get_host_by_url(url)

            # Request BGP toolkit
            get_bgp_toolkit(host)

            # Download a Screenshot
            download_screenshot(host, parser.parse_args().output)

            print(f"[{green('SUCCESS')}] {url}")
        except Exception as e:
            print(f"[{red('FAILED')}] {url}")

    generate_html_report(parser.parse_args().output)
    print("\nReport saved to " + parser.parse_args().output + "/report.html")