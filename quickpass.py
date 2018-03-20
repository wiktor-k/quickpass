#!/usr/bin/env python

import struct
import sys
import subprocess
import json
import base64
import glob
from os.path import expanduser

root = expanduser("~") + "/.password-store/"

def read():
    rawlen = sys.stdin.read(4)
    if len(rawlen) == 0:
        sys.exit(0)
    msglen = struct.unpack('@I', rawlen)[0]
    msg = sys.stdin.read(msglen)
    return json.loads(msg)

def write(msg):
    encmsg = json.dumps(msg)
    sys.stdout.write(struct.pack('@I', len(encmsg)))
    sys.stdout.write(encmsg)
    sys.stdout.flush()

while True:
    body = read()
    if body['action'] == 'search' or body['action'] == 'match_domain':
        domain = body['domain']
        if domain.startswith('www.'):
            domain = domain[4:]
        credentials = glob.glob(root + "**/*.gpg") + glob.glob(root + "*.gpg")
        credentials = map(lambda x: x[len(root):-4].replace("\\", "/"), credentials)
        credentials = filter(lambda x: domain in x, credentials)
        write(credentials)
    elif body['action'] == 'get':
        pipe = subprocess.Popen(["gpg", "--decrypt", root + body['entry'] + '.gpg'], stdout=subprocess.PIPE)
        stdout, stderr = pipe.communicate()
        if pipe.returncode == 0:
            lines = stdout.split("\n")
            password = lines[0]
            properties = { }
            for line in lines[1:]:
                parts = line.split(": ", 1)
                properties[parts[0]] = parts[1] if len(parts) > 1 else ''
            write({
                'p': password,
                'u': properties.get('login') or properties.get('user') or properties.get('username') or body['entry'].split('/')[-1]
            })
        else:
            write({
                'error': 'could not retrieve password'
            })
