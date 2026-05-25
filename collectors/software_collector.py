import os
import json
import winreg
from datetime import datetime


def get_installed_software():
    software = []

    paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for path in paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)

                try:
                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    software.append(name)
                except:
                    continue
        except:
            continue

    return software


def software_collector(incident_path, tag="snapshot"):
    print("[DEBUG] software_collector() started")

    output_dir = os.path.join(incident_path, "software")
    os.makedirs(output_dir, exist_ok=True)

    data = {
        "collection_time": datetime.now().isoformat(),
        "tag": tag,
        "installed_software": get_installed_software()
    }

    output_file = os.path.join(output_dir, f"software_{tag}.json")

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[+] Software list saved: {output_file}")