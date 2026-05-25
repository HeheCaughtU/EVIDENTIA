import os
import json
import winreg
from datetime import datetime


def read_registry_key(root, path):
    data = {}
    try:
        with winreg.OpenKey(root, path) as key:
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    data[name] = value
                    i += 1
                except OSError:
                    break
    except Exception:
        pass
    return data


def read_registry_subkeys(root, path, fields=None):
    results = {}
    try:
        with winreg.OpenKey(root, path) as base_key:
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(base_key, i)
                    i += 1

                    subkey_path = f"{path}\\{subkey_name}"
                    subkey_data = {}

                    with winreg.OpenKey(root, subkey_path) as subkey:
                        j = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(subkey, j)
                                if fields is None or name in fields:
                                    subkey_data[name] = value
                                j += 1
                            except OSError:
                                break

                    if subkey_data:
                        results[subkey_name] = subkey_data

                except OSError:
                    break
    except Exception:
        pass

    return results



def registry_collector(incident_path, tag="snapshot"):
    print("[DEBUG] registry_collector() started")

    reg_dir = os.path.join(incident_path, "registry")
    os.makedirs(reg_dir, exist_ok=True)

    registry_data = {
        "collection_time": datetime.now().isoformat(),
        "tag": tag,
        "autoruns": {},
        "installed_software": {},
        "services": {}
    }

    # --- Auto-run keys ---
    registry_data["autoruns"]["HKLM_Run"] = read_registry_key(
        winreg.HKEY_LOCAL_MACHINE,
        r"Software\Microsoft\Windows\CurrentVersion\Run"
    )

    registry_data["autoruns"]["HKCU_Run"] = read_registry_key(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run"
    )

    # --- Installed software ---
    registry_data["installed_software"] = read_registry_subkeys(
        winreg.HKEY_LOCAL_MACHINE,
        r"Software\Microsoft\Windows\CurrentVersion\Uninstall",
        fields=["DisplayName", "DisplayVersion", "Publisher", "InstallDate"]
    )


    # --- Services ---
    registry_data["services"] = read_registry_subkeys(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Services",
        fields=["ImagePath", "Start", "Type"]
    )


    output_file = os.path.join(reg_dir, f"registry_{tag}.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(registry_data, f, indent=4)

    print(f"[+] Registry data saved: {output_file}")

if __name__ == "__main__":
    test_path = "D:/cyber secrutiy/projects/test_registry"
    registry_collector(test_path, tag="snapshot")
