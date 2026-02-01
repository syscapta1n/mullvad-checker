Mullvad Account Checker

A lightweight Python script for checking Mullvad VPN account IDs using the official Mullvad CLI.
The tool validates account IDs, detects active, expired, and invalid accounts, and calculates the remaining subscription days.

It includes timeout handling and small delays between checks to avoid excessive requests.

Requirements

Python 3

Mullvad VPN CLI installed and available in PATH

Usage

Put account IDs (16 digits) into list.txt, then run:

python3 checker.py


Valid accounts will be saved to valid.txt.
