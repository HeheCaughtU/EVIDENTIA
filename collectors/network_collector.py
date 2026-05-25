import os
import json
import psutil
import subprocess
import socket
from datetime import datetime


def resolve_ip(ip):
    try:
        socket.setdefaulttimeout(1)  # ⏱ prevent delay
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None

def network_collector(incident_path, tag="snapshot"):
    print("[DEBUG] network_collector() started")

    net_dir = os.path.join(incident_path, "network")
    os.makedirs(net_dir, exist_ok=True)

    data = {
        "collection_time": datetime.now().isoformat(),
        "tag": tag,
        "connections": [],
        "arp_cache": [],
        "routing_table": []
    }

    # 🔹 Active network connections
    for conn in psutil.net_connections(kind="inet"):
        try:
            data["connections"].append({
                "pid": conn.pid,
                "laddr": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                "raddr": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                "rhost": resolve_ip(conn.raddr.ip) if conn.raddr else None,
                "status": conn.status,
                "protocol": "TCP" if conn.type == 1 else "UDP"
            })
        except Exception:
            continue

    # 🔹 ARP cache
    try:
        arp = subprocess.check_output("arp -a", shell=True, text=True)
        data["arp_cache"] = arp.splitlines()
    except Exception:
        data["arp_cache"] = ["Failed to collect ARP cache"]

    # 🔹 Routing table
    try:
        route = subprocess.check_output("route print", shell=True, text=True)
        data["routing_table"] = route.splitlines()
    except Exception:
        data["routing_table"] = ["Failed to collect routing table"]

    output_file = os.path.join(net_dir, f"network_{tag}.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"[+] Network evidence saved: {output_file}")
