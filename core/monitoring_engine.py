import time
from datetime import datetime

from collectors.process_collector import process_collector
from collectors.filesystem_collector import filesystem_metadata_collector
from collectors.registry_collector import registry_collector
from collectors.network_collector import network_collector
from collectors.eventlog_collector import event_log_collector
from collectors.timeline_collector import timeline_builder
from collectors.system_info_collector import system_info_collector
from collectors.services_collector import services_collector
from collectors.scheduled_tasks_collector import scheduled_tasks_collector
from collectors.software_collector import software_collector
from collectors.prefetch_collector import prefetch_collector
from collectors.open_files_collector import open_files_collector

def monitoring_engine(incident_path, severity, duration_minutes=1, interval_seconds=5):
    print("[DEBUG] Monitoring engine started")

    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    iteration = 1

    try:
        while time.time() < end_time:
            tag = f"monitor_{iteration}"
            current_time = datetime.now().isoformat()
            print(f"[DEBUG] Monitoring iteration {iteration} at {current_time}")

            # 🔹 Core collectors
            process_collector(incident_path, tag=tag)
            filesystem_metadata_collector(incident_path, tag=tag)
            registry_collector(incident_path, tag=tag)
            network_collector(incident_path, tag=tag)
            system_info_collector(incident_path, tag=tag)
            # 🔹 Event logs (with severity handling + Security log support)
            event_log_collector(incident_path, severity=severity)
            services_collector(incident_path, tag=tag)
            scheduled_tasks_collector(incident_path, tag=tag)
            software_collector(incident_path, tag=tag)
            prefetch_collector(incident_path)
            open_files_collector(incident_path, tag=tag)
            # 🔹 Timeline update
            timeline_builder(
                incident_path,
                message=f"Monitoring iteration {iteration}"
            )

            iteration += 1
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("[INFO] Monitoring stopped by user")

    finally:
        # 🔐 GUARANTEED final network snapshot
        print("[INFO] Finalizing network evidence")
        network_collector(incident_path, tag="final")

        timeline_builder(
            incident_path,
            message="Monitoring stopped and evidence finalized"
        )

        print("[INFO] Monitoring engine finished safely")