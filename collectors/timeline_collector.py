import os
from datetime import datetime

def timeline_builder(incident_path, message=""):
    output_file = os.path.join(incident_path, "timeline.txt")

    with open(output_file, "a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {message}\n")

    print(f"[+] Timeline updated: {output_file}")
