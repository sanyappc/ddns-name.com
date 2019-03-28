#!/usr/bin/python3

"""DDNS

DDNS (name.com)
"""

import argparse
import signal
import requests
import time
import sys

__author__ = "Alexander Mokrov"
__email__ = "sanyappc.io@gmail.com"
__version__ = "1.0.0"
__status__ = "Development"

base_url = 'https://api.name.com'

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('username', help='username')
parser.add_argument('token', help='token')
parser.add_argument('domain', help='the zone that the record belongs to')
parser.add_argument('host', help='host relative to the zone')
parser.add_argument('-i', '--interval', type=int, default=3600,
                    help='wait interval seconds between requests')

args = parser.parse_args()

signal.signal(signal.SIGINT, signal.default_int_handler)

while True:
    try:
        response = requests.get(
            requests.compat.urljoin(
                base_url, '/'.join(['v4', 'domains', args.domain, 'records'])),
            auth=(args.username, args.token))
        response.raise_for_status()

        for record in response.json()['records']:
            if record['type'] == 'A' and record['host'] == args.host:
                ip = requests.get('https://api.ipify.org').text
                if record['answer'] != ip:
                    print("old IP: %s" % record['answer'])
                    print("new IP: %s" % ip)
                    record['answer'] = ip
                    response = requests.put(
                        requests.compat.urljoin(
                            base_url, '/'.join(['v4', 'domains', args.domain, 'records', str(record['id'])])),
                        auth=(args.username, args.token),
                        json=record)
                    response.raise_for_status()
                break
    except Exception as e:
        print(e, file=sys.stderr)

    if args.interval:
        time.sleep(args.interval)
