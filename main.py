import argparse
import os
import json
import ctypes
import sys
from datetime import datetime

from utils.privilege import is_admin

from collectors.system_collector import run_internal_collector
from collectors.filesystem_collector import filesystem_metadata_collector
from collectors.process_collector import process_collector
from collectors.eventlog_collector import event_log_collector
from collectors.user_activity_collector import user_activity_collector
from collectors.timeline_collector import timeline_builder
from core.monitoring_engine import monitoring_engine
from core.privilege_check import is_admin
from collectors.system_info_collector import system_info_collector
from collectors.services_collector import services_collector
from collectors.scheduled_tasks_collector import scheduled_tasks_collector
from collectors.software_collector import software_collector
from collectors.prefetch_collector import prefetch_collector
from collectors.open_files_collector import open_files_collector
from collectors.memory_collector import memory_collector
from collectors.browser_collector import browser_history_collector


def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("[INFO] Requesting admin privileges...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

def generate_incident_id():
    return "INCIDENT_" + datetime.now().strftime("%Y%m%d_%H%M%S")


def create_incident_folder(incident_id):
    path = os.path.join(os.getcwd(), "vault", incident_id)
    os.makedirs(path, exist_ok=True)
    return path


def log_event(event):
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    with open(os.path.join(log_dir, "activity.log"), "a") as f:
        f.write(json.dumps(event) + "\n")


def severity_decision(severity, incident_path):
    print(f"[DEBUG] severity_decision running with severity={severity}")

    # LOW SEVERITY (1–2)
    if severity <= 2:
        decision = "Low severity – basic context only"

        run_internal_collector(incident_path)
        user_activity_collector(incident_path)
        timeline_builder(incident_path)

    # MEDIUM SEVERITY (3–5)
    elif 3 <= severity <= 5:
        decision = "Medium severity – snapshot + monitoring"

        user_activity_collector(incident_path)
        system_info_collector(incident_path)
        filesystem_metadata_collector(incident_path)
        process_collector(incident_path)
        event_log_collector(incident_path)
        services_collector(incident_path)
        scheduled_tasks_collector(incident_path)
        software_collector(incident_path)
        prefetch_collector(incident_path)

        # 🔹 START 30-MINUTE MONITORING
        monitoring_engine(
            incident_path,
            severity,
            duration_minutes=1,
            interval_seconds=5
        )

    # HIGH / CRITICAL SEVERITY (6+)
    else:
        decision = "High severity – snapshot + extended monitoring"

        run_internal_collector(incident_path)
        user_activity_collector(incident_path)
        timeline_builder(incident_path)
        system_info_collector(incident_path)
        filesystem_metadata_collector(incident_path)
        process_collector(incident_path)
        event_log_collector(incident_path)
        services_collector(incident_path)
        scheduled_tasks_collector(incident_path)
        software_collector(incident_path)
        open_files_collector(incident_path)
        memory_collector(incident_path)
        browser_history_collector(incident_path)

        # 🔹 START 30-MINUTE MONITORING
        monitoring_engine(
            incident_path,
            severity,
            duration_minutes=1,
            interval_seconds=5
        )

    print(f"[DEBUG] decision taken: {decision}")
    return decision


def main():
    run_as_admin()
    parser = argparse.ArgumentParser(description="EVIDENTIA – Forensic Evidence Orchestrator")
    parser.add_argument("--trigger-source", required=True)
    parser.add_argument("--incident-type", required=True)
    parser.add_argument("--severity", type=int, required=True)
    args = parser.parse_args()

    incident_id = generate_incident_id()
    incident_path = create_incident_folder(incident_id)

    admin_status = is_admin()
    print(f"[INFO] Running with admin privileges: {admin_status}")

    decision = severity_decision(args.severity, incident_path)

    event = {
        "time": datetime.now().isoformat(),
        "incident_id": incident_id,
        "trigger_source": args.trigger_source,
        "incident_type": args.incident_type,
        "severity": args.severity,
        "decision": decision,
        "admin": admin_status,
        "status": "initialized"
    }

    log_event(event)

    print(f"[+] Incident created: {incident_id}")
    print(f"[+] Evidence directory: {incident_path}")


if __name__ == "__main__":
    main()
