# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 23:54:41 2024

@author: Gourab Ghosh
"""

import nmap
import requests
import re

# Function to scan open ports on a target
def scan_open_ports(target):
    scanner = nmap.PortScanner()
    scanner.scan(target, '1-1024')  # Scanning the first 1024 ports
    open_ports = []

    for host in scanner.all_hosts():
        for proto in scanner[host].all_protocols():
            lport = scanner[host][proto].keys()
            for port in lport:
                if scanner[host][proto][port]['state'] == 'open':
                    open_ports.append(port)
    return open_ports

# Function to check for outdated software versions on a website
def check_outdated_software(url):
    response = requests.get(url)
    headers = response.headers
    software_info = {}

    # Common headers to check for software versions
    server = headers.get('Server', '')
    x_powered_by = headers.get('X-Powered-By', '')

    # Simple regex to extract version numbers
    version_pattern = re.compile(r'\d+(\.\d+)+')

    if server:
        version = version_pattern.search(server)
        if version:
            software_info['Server'] = server

    if x_powered_by:
        version = version_pattern.search(x_powered_by)
        if version:
            software_info['X-Powered-By'] = x_powered_by

    return software_info

# Function to perform the vulnerability scan
def vulnerability_scan(target):
    print(f"Scanning {target} for open ports...")
    open_ports = scan_open_ports(target)
    print(f"Open ports: {open_ports}")

    if target.startswith('http'):
        print(f"Checking {target} for outdated software versions...")
        outdated_software = check_outdated_software(target)
        print(f"Outdated software: {outdated_software}")

# Running the scan from a script
target = input("Enter the target (IP or URL): ")
vulnerability_scan(target)
