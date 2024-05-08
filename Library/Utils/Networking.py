# Coded by Eric Chen / D1172271
# ISTM Purdue
#
# Date: 2023/11/25
# CopyRight: GNU GPLv3
# DESC: RollColling FLASK Server

import socket


def get_local_ip():
    try:
        # Create a socket to connect to an external site
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Use Google's DNS server as the destination, but don't actually establish a connection
            s.connect(("8.8.8.8", 80))

            # Get the socket's own address
            return s.getsockname()[0]
    
    except Exception:
        return "127.0.0.1"  # Fallback to localhost