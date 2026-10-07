"""
GraphOps Database Seed Script.

Creates realistic cybersecurity synthetic data in Neo4j.
Uses MERGE to be idempotent — safe to run multiple times.
"""

import os
import sys
from pathlib import Path

# Allow imports from backend/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load env from backend/.env
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

NEO4J_URI = os.getenv("NEO4J_URI", "")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


# ── Node Data ────────────────────────────────────────────────────────────────

USERS = [
    {"userId": "USR-001", "name": "Ateeq Khan", "role": "DevOps Engineer", "department": "Engineering", "privileged": True},
    {"userId": "USR-002", "name": "Priya Sharma", "role": "Software Engineer", "department": "Engineering", "privileged": False},
    {"userId": "USR-003", "name": "James Wilson", "role": "Senior Developer", "department": "Engineering", "privileged": False},
    {"userId": "USR-004", "name": "Neha Fathima", "role": "Security Analyst", "department": "Security", "privileged": True},
    {"userId": "USR-005", "name": "Carlos Rivera", "role": "Network Admin", "department": "IT", "privileged": True},
    {"userId": "USR-006", "name": "Aisha Patel", "role": "Database Admin", "department": "IT", "privileged": True},
    {"userId": "USR-007", "name": "David Chen", "role": "Finance Manager", "department": "Finance", "privileged": False},
    {"userId": "USR-008", "name": "Emily Johnson", "role": "HR Director", "department": "HR", "privileged": False},
    {"userId": "USR-009", "name": "Michael Brown", "role": "IT Support", "department": "IT", "privileged": False},
    {"userId": "USR-010", "name": "Sarah Lee", "role": "Data Analyst", "department": "Engineering", "privileged": False},
    {"userId": "USR-011", "name": "Robert Taylor", "role": "VP Engineering", "department": "Engineering", "privileged": True},
    {"userId": "USR-012", "name": "Lisa Martinez", "role": "SOC Analyst", "department": "Security", "privileged": True},
    {"userId": "USR-013", "name": "Thomas Anderson", "role": "Operations Lead", "department": "Operations", "privileged": False},
    {"userId": "USR-014", "name": "Jennifer White", "role": "Finance Analyst", "department": "Finance", "privileged": False},
    {"userId": "USR-015", "name": "Kevin Park", "role": "SRE Engineer", "department": "Engineering", "privileged": True},
    {"userId": "USR-016", "name": "Amanda Clark", "role": "HR Specialist", "department": "HR", "privileged": False},
    {"userId": "USR-017", "name": "Daniel Kim", "role": "Cloud Architect", "department": "Engineering", "privileged": True},
    {"userId": "USR-018", "name": "Rachel Green", "role": "Compliance Officer", "department": "Operations", "privileged": False},
    {"userId": "USR-019", "name": "Alex Turner", "role": "Helpdesk Analyst", "department": "IT", "privileged": False},
    {"userId": "USR-020", "name": "Maria Garcia", "role": "QA Engineer", "department": "Engineering", "privileged": False},
    {"userId": "USR-021", "name": "Chris Evans", "role": "Security Engineer", "department": "Security", "privileged": True},
    {"userId": "USR-022", "name": "Hannah Moore", "role": "Accountant", "department": "Finance", "privileged": False},
    {"userId": "USR-023", "name": "Ryan Adams", "role": "Sys Admin", "department": "IT", "privileged": True},
    {"userId": "USR-024", "name": "Olivia Scott", "role": "Product Manager", "department": "Operations", "privileged": False},
    {"userId": "USR-025", "name": "Ethan Hall", "role": "Intern", "department": "Engineering", "privileged": False},
]

DEVICES = [
    {"deviceId": "DEV-001", "hostname": "Laptop-01", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 15},
    {"deviceId": "DEV-002", "hostname": "Laptop-02", "os": "macOS 14", "deviceType": "Laptop", "status": "active", "riskScore": 10},
    {"deviceId": "DEV-003", "hostname": "Laptop-03", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 20},
    {"deviceId": "DEV-004", "hostname": "Laptop-04", "os": "Ubuntu 22.04", "deviceType": "Laptop", "status": "active", "riskScore": 12},
    {"deviceId": "DEV-005", "hostname": "Laptop-05", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 8},
    {"deviceId": "DEV-006", "hostname": "Laptop-06", "os": "macOS 14", "deviceType": "Laptop", "status": "active", "riskScore": 5},
    {"deviceId": "DEV-007", "hostname": "Laptop-07", "os": "Windows 10", "deviceType": "Laptop", "status": "compromised", "riskScore": 92},
    {"deviceId": "DEV-008", "hostname": "Laptop-08", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 18},
    {"deviceId": "DEV-009", "hostname": "Laptop-09", "os": "macOS 14", "deviceType": "Laptop", "status": "active", "riskScore": 7},
    {"deviceId": "DEV-010", "hostname": "Laptop-10", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 11},
    {"deviceId": "DEV-011", "hostname": "Desktop-01", "os": "Windows 11", "deviceType": "Desktop", "status": "active", "riskScore": 14},
    {"deviceId": "DEV-012", "hostname": "Desktop-02", "os": "Windows 11", "deviceType": "Desktop", "status": "active", "riskScore": 9},
    {"deviceId": "DEV-013", "hostname": "Desktop-03", "os": "Ubuntu 22.04", "deviceType": "Desktop", "status": "active", "riskScore": 6},
    {"deviceId": "DEV-014", "hostname": "Desktop-04", "os": "Windows 11", "deviceType": "Desktop", "status": "active", "riskScore": 13},
    {"deviceId": "DEV-015", "hostname": "Desktop-05", "os": "Windows 11", "deviceType": "Desktop", "status": "active", "riskScore": 10},
    {"deviceId": "DEV-016", "hostname": "Workstation-01", "os": "Ubuntu 22.04", "deviceType": "Workstation", "status": "active", "riskScore": 22},
    {"deviceId": "DEV-017", "hostname": "Workstation-02", "os": "Windows 11", "deviceType": "Workstation", "status": "active", "riskScore": 17},
    {"deviceId": "DEV-018", "hostname": "Workstation-03", "os": "macOS 14", "deviceType": "Workstation", "status": "active", "riskScore": 8},
    {"deviceId": "DEV-019", "hostname": "Laptop-11", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 25},
    {"deviceId": "DEV-020", "hostname": "Laptop-12", "os": "macOS 14", "deviceType": "Laptop", "status": "active", "riskScore": 6},
    {"deviceId": "DEV-021", "hostname": "Laptop-13", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 19},
    {"deviceId": "DEV-022", "hostname": "Laptop-14", "os": "Ubuntu 22.04", "deviceType": "Laptop", "status": "active", "riskScore": 11},
    {"deviceId": "DEV-023", "hostname": "Laptop-15", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 14},
    {"deviceId": "DEV-024", "hostname": "Desktop-06", "os": "Windows 11", "deviceType": "Desktop", "status": "active", "riskScore": 10},
    {"deviceId": "DEV-025", "hostname": "Desktop-07", "os": "macOS 14", "deviceType": "Desktop", "status": "active", "riskScore": 7},
    {"deviceId": "DEV-026", "hostname": "Laptop-16", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 16},
    {"deviceId": "DEV-027", "hostname": "Laptop-17", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 30},
    {"deviceId": "DEV-028", "hostname": "Workstation-04", "os": "Ubuntu 22.04", "deviceType": "Workstation", "status": "active", "riskScore": 12},
    {"deviceId": "DEV-029", "hostname": "Laptop-18", "os": "macOS 14", "deviceType": "Laptop", "status": "active", "riskScore": 9},
    {"deviceId": "DEV-030", "hostname": "Laptop-19", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 21},
    {"deviceId": "DEV-031", "hostname": "Desktop-08", "os": "Windows 11", "deviceType": "Desktop", "status": "active", "riskScore": 8},
    {"deviceId": "DEV-032", "hostname": "Desktop-09", "os": "Ubuntu 22.04", "deviceType": "Desktop", "status": "active", "riskScore": 13},
    {"deviceId": "DEV-033", "hostname": "Laptop-20", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 10},
    {"deviceId": "DEV-034", "hostname": "Laptop-21", "os": "macOS 14", "deviceType": "Laptop", "status": "active", "riskScore": 5},
    {"deviceId": "DEV-035", "hostname": "Workstation-05", "os": "Windows 11", "deviceType": "Workstation", "status": "active", "riskScore": 15},
    {"deviceId": "DEV-036", "hostname": "Laptop-22", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 28},
    {"deviceId": "DEV-037", "hostname": "Laptop-23", "os": "Windows 10", "deviceType": "Laptop", "status": "active", "riskScore": 35},
    {"deviceId": "DEV-038", "hostname": "Desktop-10", "os": "Windows 11", "deviceType": "Desktop", "status": "active", "riskScore": 7},
    {"deviceId": "DEV-039", "hostname": "Laptop-24", "os": "macOS 14", "deviceType": "Laptop", "status": "active", "riskScore": 9},
    {"deviceId": "DEV-040", "hostname": "Laptop-25", "os": "Windows 11", "deviceType": "Laptop", "status": "active", "riskScore": 11},
]

IPS = [
    {"address": "10.0.1.10", "type": "internal"},
    {"address": "10.0.1.11", "type": "internal"},
    {"address": "10.0.1.12", "type": "internal"},
    {"address": "10.0.1.20", "type": "internal"},
    {"address": "10.0.1.21", "type": "internal"},
    {"address": "10.0.2.10", "type": "internal"},
    {"address": "10.0.2.11", "type": "internal"},
    {"address": "10.0.2.12", "type": "internal"},
    {"address": "10.0.3.10", "type": "internal"},
    {"address": "10.0.3.11", "type": "internal"},
    {"address": "10.0.3.50", "type": "internal"},
    {"address": "10.0.4.10", "type": "internal"},
    {"address": "10.0.4.11", "type": "internal"},
    {"address": "192.168.1.100", "type": "internal"},
    {"address": "192.168.1.101", "type": "internal"},
    {"address": "172.16.0.10", "type": "dmz"},
    {"address": "172.16.0.11", "type": "dmz"},
    {"address": "203.0.113.50", "type": "external"},
    {"address": "203.0.113.51", "type": "external"},
    {"address": "198.51.100.10", "type": "external"},
]

SERVERS = [
    {"serverId": "SRV-001", "hostname": "web-prod-01", "serverType": "Web", "criticality": "high", "environment": "production"},
    {"serverId": "SRV-002", "hostname": "web-prod-02", "serverType": "Web", "criticality": "high", "environment": "production"},
    {"serverId": "SRV-003", "hostname": "app-prod-01", "serverType": "Application", "criticality": "high", "environment": "production"},
    {"serverId": "SRV-004", "hostname": "app-prod-02", "serverType": "Application", "criticality": "medium", "environment": "production"},
    {"serverId": "SRV-005", "hostname": "db-prod-01", "serverType": "Database", "criticality": "critical", "environment": "production"},
    {"serverId": "SRV-006", "hostname": "db-prod-02", "serverType": "Database", "criticality": "critical", "environment": "production"},
    {"serverId": "SRV-007", "hostname": "auth-prod-01", "serverType": "Authentication", "criticality": "critical", "environment": "production"},
    {"serverId": "SRV-008", "hostname": "file-srv-01", "serverType": "File", "criticality": "medium", "environment": "production"},
    {"serverId": "SRV-009", "hostname": "monitor-01", "serverType": "Monitoring", "criticality": "medium", "environment": "production"},
    {"serverId": "SRV-010", "hostname": "app-staging-01", "serverType": "Application", "criticality": "low", "environment": "staging"},
    {"serverId": "SRV-011", "hostname": "web-staging-01", "serverType": "Web", "criticality": "low", "environment": "staging"},
    {"serverId": "SRV-012", "hostname": "ci-cd-01", "serverType": "Application", "criticality": "high", "environment": "production"},
    {"serverId": "SRV-013", "hostname": "vpn-gateway-01", "serverType": "Web", "criticality": "high", "environment": "production"},
    {"serverId": "SRV-014", "hostname": "backup-srv-01", "serverType": "File", "criticality": "high", "environment": "production"},
    {"serverId": "SRV-015", "hostname": "log-aggregator-01", "serverType": "Monitoring", "criticality": "medium", "environment": "production"},
]

APPLICATIONS = [
    {"appId": "APP-001", "name": "GraphOps Portal", "version": "1.2.0", "criticality": "high"},
    {"appId": "APP-002", "name": "HR Management System", "version": "3.5.1", "criticality": "medium"},
    {"appId": "APP-003", "name": "Finance ERP", "version": "5.0.2", "criticality": "critical"},
    {"appId": "APP-004", "name": "Customer CRM", "version": "2.8.0", "criticality": "high"},
    {"appId": "APP-005", "name": "Internal Wiki", "version": "1.0.4", "criticality": "low"},
    {"appId": "APP-006", "name": "CI/CD Pipeline", "version": "4.1.0", "criticality": "high"},
    {"appId": "APP-007", "name": "Identity Provider", "version": "2.3.1", "criticality": "critical"},
    {"appId": "APP-008", "name": "Log Analytics", "version": "3.0.0", "criticality": "medium"},
    {"appId": "APP-009", "name": "Backup Manager", "version": "1.5.2", "criticality": "high"},
    {"appId": "APP-010", "name": "VPN Gateway App", "version": "2.0.1", "criticality": "high"},
]

DATABASES = [
    {"databaseId": "DB-001", "name": "Finance-DB", "dataType": "Finance", "criticality": "critical"},
    {"databaseId": "DB-002", "name": "Customer-DB", "dataType": "Customer", "criticality": "critical"},
    {"databaseId": "DB-003", "name": "Employee-DB", "dataType": "Employee", "criticality": "high"},
    {"databaseId": "DB-004", "name": "Logs-DB", "dataType": "Logs", "criticality": "medium"},
    {"databaseId": "DB-005", "name": "Analytics-DB", "dataType": "Analytics", "criticality": "medium"},
    {"databaseId": "DB-006", "name": "Auth-DB", "dataType": "Employee", "criticality": "critical"},
    {"databaseId": "DB-007", "name": "Backup-DB", "dataType": "Logs", "criticality": "high"},
    {"databaseId": "DB-008", "name": "Config-DB", "dataType": "Analytics", "criticality": "medium"},
]

VULNERABILITIES = [
    {"cveId": "CVE-2024-21351", "severity": "critical", "description": "Windows SmartScreen Security Feature Bypass Vulnerability"},
    {"cveId": "CVE-2024-21412", "severity": "high", "description": "Internet Shortcut Files Security Feature Bypass Vulnerability"},
    {"cveId": "CVE-2024-3400", "severity": "critical", "description": "PAN-OS Command Injection in GlobalProtect Gateway"},
    {"cveId": "CVE-2023-44228", "severity": "critical", "description": "Apache Log4j2 Remote Code Execution"},
    {"cveId": "CVE-2024-1709", "severity": "critical", "description": "ConnectWise ScreenConnect Authentication Bypass"},
    {"cveId": "CVE-2023-46805", "severity": "high", "description": "Ivanti Connect Secure Authentication Bypass"},
    {"cveId": "CVE-2024-27198", "severity": "critical", "description": "JetBrains TeamCity Authentication Bypass"},
    {"cveId": "CVE-2023-34362", "severity": "high", "description": "MOVEit Transfer SQL Injection Vulnerability"},
    {"cveId": "CVE-2024-0204", "severity": "high", "description": "GoAnywhere MFT Authentication Bypass"},
    {"cveId": "CVE-2023-20198", "severity": "critical", "description": "Cisco IOS XE Web UI Privilege Escalation"},
    {"cveId": "CVE-2024-21887", "severity": "high", "description": "Ivanti Connect Secure Command Injection"},
    {"cveId": "CVE-2023-42793", "severity": "medium", "description": "JetBrains TeamCity RCE via Authentication Bypass"},
    {"cveId": "CVE-2024-23897", "severity": "medium", "description": "Jenkins CLI Arbitrary File Read"},
    {"cveId": "CVE-2023-36884", "severity": "medium", "description": "Microsoft Office HTML Remote Code Execution"},
    {"cveId": "CVE-2024-20353", "severity": "high", "description": "Cisco ASA and FTD Denial of Service"},
]


# ── Relationships ────────────────────────────────────────────────────────────

# (userId, deviceId) — User USES Device
USER_USES_DEVICE = [
    ("USR-001", "DEV-007"),  # Ateeq → Laptop-07 (compromised — attack scenario)
    ("USR-001", "DEV-016"),  # Ateeq also uses a workstation
    ("USR-002", "DEV-002"),
    ("USR-003", "DEV-003"),
    ("USR-004", "DEV-004"),
    ("USR-005", "DEV-005"),
    ("USR-006", "DEV-006"),
    ("USR-007", "DEV-011"),
    ("USR-008", "DEV-012"),
    ("USR-009", "DEV-013"),
    ("USR-010", "DEV-001"),
    ("USR-011", "DEV-017"),
    ("USR-012", "DEV-008"),
    ("USR-013", "DEV-014"),
    ("USR-014", "DEV-015"),
    ("USR-015", "DEV-019"),
    ("USR-016", "DEV-020"),
    ("USR-017", "DEV-021"),
    ("USR-018", "DEV-022"),
    ("USR-019", "DEV-023"),
    ("USR-020", "DEV-024"),
    ("USR-021", "DEV-009"),
    ("USR-022", "DEV-025"),
    ("USR-023", "DEV-010"),
    ("USR-024", "DEV-026"),
    ("USR-025", "DEV-018"),
]

# (deviceId, address) — Device HAS_IP
DEVICE_HAS_IP = [
    ("DEV-007", "10.0.1.10"),   # Laptop-07 (compromised)
    ("DEV-001", "10.0.1.11"),
    ("DEV-002", "10.0.1.12"),
    ("DEV-003", "10.0.1.20"),
    ("DEV-004", "10.0.1.21"),
    ("DEV-005", "10.0.2.10"),
    ("DEV-006", "10.0.2.11"),
    ("DEV-011", "10.0.2.12"),
    ("DEV-012", "10.0.3.10"),
    ("DEV-013", "10.0.3.11"),
    ("DEV-016", "10.0.3.50"),
    ("DEV-017", "10.0.4.10"),
    ("DEV-014", "10.0.4.11"),
    ("DEV-019", "192.168.1.100"),
    ("DEV-021", "192.168.1.101"),
]

# (deviceId, serverId) — Device CONNECTED_TO Server
DEVICE_CONNECTED_TO_SERVER = [
    ("DEV-007", "SRV-003"),   # Laptop-07 → app-prod-01 (attack path)
    ("DEV-007", "SRV-011"),   # Laptop-07 → web-staging
    ("DEV-001", "SRV-001"),
    ("DEV-002", "SRV-001"),
    ("DEV-003", "SRV-003"),
    ("DEV-004", "SRV-009"),
    ("DEV-005", "SRV-013"),
    ("DEV-006", "SRV-005"),
    ("DEV-016", "SRV-003"),
    ("DEV-016", "SRV-012"),
    ("DEV-017", "SRV-001"),
    ("DEV-017", "SRV-012"),
    ("DEV-019", "SRV-010"),
    ("DEV-021", "SRV-002"),
    ("DEV-008", "SRV-009"),
    ("DEV-013", "SRV-008"),
    ("DEV-014", "SRV-004"),
    ("DEV-015", "SRV-001"),
    ("DEV-010", "SRV-007"),   # SysAdmin device → Auth server
]

# (serverId, appId) — Server RUNS Application
SERVER_RUNS_APP = [
    ("SRV-001", "APP-001"),   # web-prod-01 → GraphOps Portal
    ("SRV-002", "APP-004"),   # web-prod-02 → CRM
    ("SRV-003", "APP-003"),   # app-prod-01 → Finance ERP (attack path)
    ("SRV-004", "APP-002"),   # app-prod-02 → HR System
    ("SRV-007", "APP-007"),   # auth-prod-01 → Identity Provider
    ("SRV-009", "APP-008"),   # monitor-01 → Log Analytics
    ("SRV-012", "APP-006"),   # ci-cd-01 → CI/CD Pipeline
    ("SRV-013", "APP-010"),   # vpn-gateway → VPN App
    ("SRV-014", "APP-009"),   # backup-srv → Backup Manager
    ("SRV-011", "APP-005"),   # web-staging → Internal Wiki
    ("SRV-015", "APP-008"),   # log-aggregator → Log Analytics
]

# (appId, databaseId) — Application ACCESSES Database
APP_ACCESSES_DB = [
    ("APP-003", "DB-001"),   # Finance ERP → Finance-DB (attack path)
    ("APP-004", "DB-002"),   # CRM → Customer-DB
    ("APP-002", "DB-003"),   # HR System → Employee-DB
    ("APP-007", "DB-006"),   # Identity Provider → Auth-DB
    ("APP-008", "DB-004"),   # Log Analytics → Logs-DB
    ("APP-006", "DB-008"),   # CI/CD → Config-DB
    ("APP-009", "DB-007"),   # Backup Manager → Backup-DB
    ("APP-001", "DB-005"),   # GraphOps Portal → Analytics-DB
]

# (deviceId, cveId) — Device HAS_VULNERABILITY
DEVICE_HAS_VULN = [
    ("DEV-007", "CVE-2024-21351"),  # Laptop-07 (compromised)
    ("DEV-007", "CVE-2024-21412"),  # Laptop-07 (compromised)
    ("DEV-007", "CVE-2023-44228"),  # Laptop-07 (compromised) — Log4j!
    ("DEV-037", "CVE-2024-21351"),
    ("DEV-037", "CVE-2023-36884"),
    ("DEV-027", "CVE-2024-23897"),
    ("DEV-019", "CVE-2024-1709"),
    ("DEV-036", "CVE-2024-0204"),
    ("DEV-030", "CVE-2023-34362"),
    ("DEV-003", "CVE-2023-42793"),
]

# (userId, serverId) — User PRIVILEGED_ACCESS to Server
USER_PRIVILEGED_ACCESS = [
    ("USR-001", "SRV-003"),   # Ateeq → app-prod-01 (attack scenario)
    ("USR-001", "SRV-012"),   # Ateeq → CI/CD
    ("USR-005", "SRV-007"),   # Network Admin → Auth server
    ("USR-005", "SRV-013"),   # Network Admin → VPN gateway
    ("USR-006", "SRV-005"),   # DBA → db-prod-01
    ("USR-006", "SRV-006"),   # DBA → db-prod-02
    ("USR-011", "SRV-001"),   # VP Eng → web-prod-01
    ("USR-011", "SRV-003"),   # VP Eng → app-prod-01
    ("USR-015", "SRV-009"),   # SRE → monitoring
    ("USR-015", "SRV-015"),   # SRE → log-aggregator
    ("USR-023", "SRV-007"),   # SysAdmin → Auth server
    ("USR-023", "SRV-008"),   # SysAdmin → file-srv
    ("USR-023", "SRV-014"),   # SysAdmin → backup-srv
    ("USR-004", "SRV-009"),   # Security Analyst → monitoring
    ("USR-012", "SRV-009"),   # SOC Analyst → monitoring
    ("USR-017", "SRV-001"),   # Cloud Architect → web-prod-01
    ("USR-017", "SRV-002"),   # Cloud Architect → web-prod-02
    ("USR-021", "SRV-007"),   # Security Engineer → Auth server
]

# (serverId, databaseId) — Server ACCESSES Database
SERVER_ACCESSES_DB = [
    ("SRV-005", "DB-001"),   # db-prod-01 → Finance-DB (attack path)
    ("SRV-005", "DB-002"),   # db-prod-01 → Customer-DB
    ("SRV-006", "DB-003"),   # db-prod-02 → Employee-DB
    ("SRV-006", "DB-004"),   # db-prod-02 → Logs-DB
    ("SRV-007", "DB-006"),   # auth-prod-01 → Auth-DB
    ("SRV-014", "DB-007"),   # backup-srv → Backup-DB
    ("SRV-015", "DB-004"),   # log-aggregator → Logs-DB
    ("SRV-003", "DB-001"),   # app-prod-01 → Finance-DB (attack path shortcut)
]

# (serverId, serverId) — Server COMMUNICATES_WITH Server
SERVER_COMMUNICATES = [
    ("SRV-001", "SRV-003"),   # web-prod-01 → app-prod-01
    ("SRV-001", "SRV-007"),   # web-prod-01 → auth-prod-01
    ("SRV-002", "SRV-004"),   # web-prod-02 → app-prod-02
    ("SRV-002", "SRV-007"),   # web-prod-02 → auth-prod-01
    ("SRV-003", "SRV-005"),   # app-prod-01 → db-prod-01 (attack path)
    ("SRV-004", "SRV-006"),   # app-prod-02 → db-prod-02
    ("SRV-003", "SRV-007"),   # app-prod-01 → auth-prod-01
    ("SRV-009", "SRV-015"),   # monitor → log-aggregator
    ("SRV-012", "SRV-010"),   # ci-cd → staging
    ("SRV-012", "SRV-003"),   # ci-cd → app-prod-01
    ("SRV-013", "SRV-007"),   # vpn-gateway → auth-prod-01
    ("SRV-014", "SRV-005"),   # backup-srv → db-prod-01
    ("SRV-014", "SRV-006"),   # backup-srv → db-prod-02
]


# ── Seed Logic ───────────────────────────────────────────────────────────────

def create_constraints(session):
    """Create uniqueness constraints for node identifiers."""
    constraints = [
        ("user_id_unique",        "User",          "userId"),
        ("device_id_unique",      "Device",        "deviceId"),
        ("server_id_unique",      "Server",        "serverId"),
        ("app_id_unique",         "Application",   "appId"),
        ("database_id_unique",    "Database",       "databaseId"),
        ("vuln_cve_unique",       "Vulnerability", "cveId"),
        ("ip_address_unique",     "IP",            "address"),
    ]
    for name, label, prop in constraints:
        query = (
            f"CREATE CONSTRAINT {name} IF NOT EXISTS "
            f"FOR (n:{label}) REQUIRE n.{prop} IS UNIQUE"
        )
        session.run(query)
    print("  Constraints created.")


def seed_nodes(session):
    """Insert all node types using MERGE (idempotent)."""
    # Users
    for u in USERS:
        session.run(
            "MERGE (n:User {userId: $userId}) "
            "SET n.name = $name, n.role = $role, "
            "n.department = $department, n.privileged = $privileged",
            **u,
        )

    # Devices
    for d in DEVICES:
        session.run(
            "MERGE (n:Device {deviceId: $deviceId}) "
            "SET n.hostname = $hostname, n.os = $os, "
            "n.deviceType = $deviceType, n.status = $status, n.riskScore = $riskScore",
            **d,
        )

    # IPs
    for ip in IPS:
        session.run(
            "MERGE (n:IP {address: $address}) SET n.type = $type",
            **ip,
        )

    # Servers
    for s in SERVERS:
        session.run(
            "MERGE (n:Server {serverId: $serverId}) "
            "SET n.hostname = $hostname, n.serverType = $serverType, "
            "n.criticality = $criticality, n.environment = $environment",
            **s,
        )

    # Applications
    for a in APPLICATIONS:
        session.run(
            "MERGE (n:Application {appId: $appId}) "
            "SET n.name = $name, n.version = $version, n.criticality = $criticality",
            **a,
        )

    # Databases
    for db in DATABASES:
        session.run(
            "MERGE (n:Database {databaseId: $databaseId}) "
            "SET n.name = $name, n.dataType = $dataType, n.criticality = $criticality",
            **db,
        )

    # Vulnerabilities
    for v in VULNERABILITIES:
        session.run(
            "MERGE (n:Vulnerability {cveId: $cveId}) "
            "SET n.severity = $severity, n.description = $description",
            **v,
        )

    print("  Nodes created.")


def seed_relationships(session):
    """Insert all relationships using MERGE (idempotent)."""
    rel_count = 0

    for uid, did in USER_USES_DEVICE:
        session.run(
            "MATCH (u:User {userId: $uid}), (d:Device {deviceId: $did}) "
            "MERGE (u)-[:USES]->(d)",
            uid=uid, did=did,
        )
        rel_count += 1

    for did, addr in DEVICE_HAS_IP:
        session.run(
            "MATCH (d:Device {deviceId: $did}), (ip:IP {address: $addr}) "
            "MERGE (d)-[:HAS_IP]->(ip)",
            did=did, addr=addr,
        )
        rel_count += 1

    for did, sid in DEVICE_CONNECTED_TO_SERVER:
        session.run(
            "MATCH (d:Device {deviceId: $did}), (s:Server {serverId: $sid}) "
            "MERGE (d)-[:CONNECTED_TO]->(s)",
            did=did, sid=sid,
        )
        rel_count += 1

    for sid, aid in SERVER_RUNS_APP:
        session.run(
            "MATCH (s:Server {serverId: $sid}), (a:Application {appId: $aid}) "
            "MERGE (s)-[:RUNS]->(a)",
            sid=sid, aid=aid,
        )
        rel_count += 1

    for aid, dbid in APP_ACCESSES_DB:
        session.run(
            "MATCH (a:Application {appId: $aid}), (db:Database {databaseId: $dbid}) "
            "MERGE (a)-[:ACCESSES]->(db)",
            aid=aid, dbid=dbid,
        )
        rel_count += 1

    for did, cve in DEVICE_HAS_VULN:
        session.run(
            "MATCH (d:Device {deviceId: $did}), (v:Vulnerability {cveId: $cve}) "
            "MERGE (d)-[:HAS_VULNERABILITY]->(v)",
            did=did, cve=cve,
        )
        rel_count += 1

    for uid, sid in USER_PRIVILEGED_ACCESS:
        session.run(
            "MATCH (u:User {userId: $uid}), (s:Server {serverId: $sid}) "
            "MERGE (u)-[:PRIVILEGED_ACCESS]->(s)",
            uid=uid, sid=sid,
        )
        rel_count += 1

    for sid, dbid in SERVER_ACCESSES_DB:
        session.run(
            "MATCH (s:Server {serverId: $sid}), (db:Database {databaseId: $dbid}) "
            "MERGE (s)-[:ACCESSES]->(db)",
            sid=sid, dbid=dbid,
        )
        rel_count += 1

    for s1, s2 in SERVER_COMMUNICATES:
        session.run(
            "MATCH (a:Server {serverId: $s1}), (b:Server {serverId: $s2}) "
            "MERGE (a)-[:COMMUNICATES_WITH]->(b)",
            s1=s1, s2=s2,
        )
        rel_count += 1

    print(f"  Relationships created: {rel_count}")
    return rel_count


def print_stats(session):
    """Print node and relationship counts."""
    labels = ["User", "Device", "IP", "Server", "Application", "Database", "Vulnerability"]
    print("\n  === GraphOps Database Statistics ===\n")
    for label in labels:
        result = session.run(f"MATCH (n:{label}) RETURN count(n) AS c")
        count = result.single()["c"]
        print(f"  {label + 's:':<20} {count}")

    result = session.run("MATCH ()-[r]->() RETURN count(r) AS c")
    total_rels = result.single()["c"]
    print(f"\n  {'Relationships:':<20} {total_rels}")
    print()


def main():
    if not NEO4J_URI or not NEO4J_USERNAME or not NEO4J_PASSWORD:
        print("ERROR: Neo4j credentials not configured.")
        print("Copy backend/.env.example to backend/.env and fill in your credentials.")
        sys.exit(1)

    print(f"Connecting to Neo4j at {NEO4J_URI} ...")
    driver = GraphDatabase.driver(
        NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    try:
        driver.verify_connectivity()
        print("Connected.\n")

        with driver.session(database=NEO4J_DATABASE) as session:
            print("Creating constraints ...")
            create_constraints(session)

            print("Seeding nodes ...")
            seed_nodes(session)

            print("Seeding relationships ...")
            seed_relationships(session)

            print_stats(session)

        print("GraphOps database seeded successfully.")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
