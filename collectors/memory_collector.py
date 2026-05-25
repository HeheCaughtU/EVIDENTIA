import os
import subprocess

def memory_collector(incident_path):
    print("[DEBUG] memory_collector() started")

    output_dir = os.path.join(incident_path, "memory")
    os.makedirs(output_dir, exist_ok=True)

    dump_file = os.path.join(output_dir, "memory_dump.raw")
    tool_path = os.path.join("tools", "winpmem.exe")

    if not os.path.exists(tool_path):
        print("[ERROR] Memory module missing")
        return

    try:
        print("[INFO] Starting full memory dump (this may take time...)")

        subprocess.run(
            [tool_path, "acquire", dump_file],
            check=True
        )

        print(f"[+] Memory dump saved: {dump_file}")

    except Exception as e:
        print(f"[ERROR] Memory dump failed: {e}")