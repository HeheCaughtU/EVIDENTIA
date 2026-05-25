import os
import json
import platform
from datetime import datetime


def system_info_collector(incident_path, tag="snapshot"):
    print("[DEBUG] system_info_collector() started")

    data = {
        "collection_time": datetime.now().isoformat(),
        "tag": tag,
        "system": {
            "os": platform.system(),
            "os_version": platform.version(),
            "release": platform.release(),
            "hostname": platform.node(),
            "architecture": platform.machine(),
            "processor": platform.processor()
        }
    }

    output_dir = os.path.join(incident_path, "system_info")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"system_info_{tag}.json")

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[+] System info saved: {output_file}")