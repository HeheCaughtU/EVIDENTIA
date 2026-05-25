# EVIDENTIA

## SIEM-Driven Automated Incident Response Framework

EVIDENTIA is an automated Digital Forensics and Incident Response (DFIR) framework that integrates Wazuh SIEM with a custom Python-based evidence collection engine.

It detects security incidents in real time and automatically initiates forensic evidence collection on Windows endpoints based on alert severity.

## Key Features

- Real-time SIEM alert monitoring
- Automated DFIR response workflows
- Severity-based evidence acquisition
- Windows forensic artifact collection
- HTTP-based cross-system automation
- Structured incident evidence storage

## Technology Stack

- Python
- Wazuh SIEM
- Kali Linux
- Windows
- JSON
- HTTP
- DFIR Tooling

## Architecture

(Add your architecture screenshot here)

## Workflow

1. Wazuh detects suspicious activity
2. Alert generated in alerts.json
3. Monitoring script processes alert
4. Trigger sent to Windows listener
5. Evidence collection initiated
6. Artifacts stored in structured incident folders

## Project Modules

- Collectors
- Core Engine
- Listener Service
- Utility Modules
- Evidence Vault

## Author

Aryan Patel  
Cybersecurity | DFIR | SIEM | SOC | Incident Response
