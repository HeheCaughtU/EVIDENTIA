import os
import getpass
import socket
from datetime import datetime

def user_activity_collector(incident_path):
    output_file = os.path.join(incident_path, "user_activity.txt")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("User Activity Evidence\n")
        f.write("======================\n")
        f.write(f"Username: {getpass.getuser()}\n")
        f.write(f"Hostname: {socket.gethostname()}\n")
        f.write(f"Collected at: {datetime.now().isoformat()}\n")

    print(f"[+] User activity collected: {output_file}")
