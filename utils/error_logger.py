import os
from datetime import datetime

def log_collection_error(incident_path, collector, reason, permission):
    error_file = os.path.join(incident_path, "collection_errors.txt")
    timestamp = datetime.now().isoformat()

    line = f"{timestamp} | {collector} | {reason} | {permission}\n"

    with open(error_file, "a") as f:
        f.write(line)
