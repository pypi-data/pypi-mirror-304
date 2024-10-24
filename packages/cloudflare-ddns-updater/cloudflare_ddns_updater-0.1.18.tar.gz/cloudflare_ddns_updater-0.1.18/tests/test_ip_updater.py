import json
import requests
import os
import sys
import subprocess
import shutil
import argparse


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


