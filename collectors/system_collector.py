import os
import getpass
from datetime import datetime





def run_internal_collector(incident_path):
    """
    First internal collector (safe).
    Collects system basic info without external tools.
    """
    output_file = os.path.join(incident_path, "system_info.txt")

    info = []
    info.append(f"OS Name: {os.name}")
    info.append(f"Current Directory: {os.getcwd()}")
    info.append(f"User: {os.getlogin()}")

    with open(output_file, "w") as f:
        for line in info:
            f.write(line + "\n")