import os
import json
import subprocess
from datetime import datetime


def services_collector(incident_path, tag="snapshot"):
    print("[DEBUG] services_collector() started")

    output_dir = os.path.join(incident_path, "services")
    os.makedirs(output_dir, exist_ok=True)

    try:
        result = subprocess.check_output(
            ["sc", "query", "state=", "all"],
            text=True
        )
        services = result.splitlines()
    except Exception:
        services = ["Failed to collect services"]

    data = {
        "collection_time": datetime.now().isoformat(),
        "tag": tag,
        "services": services
    }

    output_file = os.path.join(output_dir, f"services_{tag}.json")

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[+] Services saved: {output_file}")