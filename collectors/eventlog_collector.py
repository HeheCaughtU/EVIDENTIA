import os
import subprocess
from core.privilege_check import is_admin


def event_log_collector(incident_path, severity=1):
    print("[DEBUG] event_log_collector() started")

    logs_dir = os.path.join(incident_path, "event_logs")
    os.makedirs(logs_dir, exist_ok=True)

    # 🧠 Define logs based on severity
    logs = {
        "Application": "Application.evtx",
        "System": "System.evtx"
    }

    # 🔥 Add Security log only for high severity
    if severity >= 7:
        logs["Security"] = "Security.evtx"

    # 🟡 Check admin only if Security log needed
    if "Security" in logs and not is_admin():
        print("[WARNING] Security log requires admin privileges!")
        print("[INFO] Please run tool as Administrator for full evidence collection")

        # Remove Security if no admin (fallback)
        logs.pop("Security")

    elif not is_admin():
        print("[INFO] Event log collection skipped (requires admin)")
        print("[INFO] Please run tool as Administrator for full evidence collection")
        return

    # 🔄 Export logs
    for log_name, file_name in logs.items():
        output_path = os.path.join(logs_dir, file_name)

        # ✅ Forensic-safe (no overwrite)
        if os.path.exists(output_path):
            print(f"[!] {log_name} log already exists, skipping export")
            continue

        command = ["wevtutil", "epl", log_name, output_path]

        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=False
        )

        if result.returncode == 0:
            print(f"[+] {log_name} event log exported: {output_path}")
        else:
            print(f"[!] {log_name} log export failed")