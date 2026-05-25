# EVIDENTIA

SIEM-Driven Automated Incident Response Framework

## Overview
EVIDENTIA is a SIEM-driven DFIR automation framework that integrates Wazuh with a custom Python-based incident response system.

It detects alerts in real time and automatically triggers forensic evidence collection on Windows systems.

## Features
- Real-time Wazuh alert monitoring
- Automated DFIR workflow
- Severity-based response execution
- Windows evidence collection
- Incident artifact storage
- Modular collector architecture

## Project Structure
```bash
collectors/   -> Evidence collection modules
core/         -> Core execution logic
docs/         -> Architecture and documentation
tools/        -> External forensic tools
utils/        -> Helper functions
listener.py   -> Windows listener
main.py       -> Main DFIR engine
```

## Technologies
- Python
- Wazuh SIEM
- Kali Linux
- Windows
- DFIR
- HTTP Automation

## Author
Aryan Patel
Cybersecurity | DFIR | SOC | SIEM