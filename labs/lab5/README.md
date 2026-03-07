# Lab 5: Automated Pentesting

## Overview

Lab 5 teaches automated penetration testing techniques using industry-standard tools. Students will learn to automate reconnaissance, vulnerability scanning, and exploitation workflows using Metasploit Framework, AutoRecon, and other automated tools against vulnerable applications.

## Requirements

- Docker Engine 24.0+
- Docker Compose 2.0+
- 4GB RAM minimum (6GB recommended)
- 8GB free disk space

## Architecture

```
┌──────────────────────────────────────────┐
│     Docker Network (172.18.5.0/24)       │
├──────────────────────────────────────────┤
│  Kali Linux (172.18.5.10)                │
│  ├── Metasploit Framework                │
│  ├── AutoRecon                           │
│  ├── Nmap, Nikto, testssl.sh            │
│  └── Automated Testing Scripts           │
│                                          │
│  OWASP Juice Shop (172.18.5.20)         │
│  ├── Intentionally Vulnerable App       │
│  ├── Port 3000 (Web)                    │
│  └── Multiple Vulnerabilities            │
└──────────────────────────────────────────┘
```

## Quick Start

### 1. Start the Lab

```bash
cd lab5
docker-compose up -d
```

### 2. Wait for target to be ready

```bash
docker-compose logs -f target

# Wait for "Listening on port 3000" message
```

### 3. Access target application

Open browser: `http://localhost:3000`

### 4. Connect to Kali

```bash
docker-compose exec kali /bin/bash
```

## Learning Objectives

By the end of this lab, students will be able to:

- ✓ Use Metasploit Framework for automation
- ✓ Perform automated reconnaissance with AutoRecon
- ✓ Conduct vulnerability scanning at scale
- ✓ Automate exploitation workflows
- ✓ Generate professional penetration test reports
- ✓ Use Nmap, Nikto, and testssl.sh
- ✓ Integrate multiple tools into workflows

## Exercises

### Exercise 1: Automated Network Reconnaissance

**Objective**: Perform comprehensive automated scanning

From Kali container:

```bash
# 1. Basic Nmap scan with all ports
nmap -p- -sV -O 172.18.5.20 -oA lab5_scan

# 2. Run AutoRecon (comprehensive automated scanning)
autorecon 172.18.5.20 --single-host

# 3. Aggressive scan with NSE scripts
nmap -A -sC -sV --script=http-* 172.18.5.20

# 4. Save results in multiple formats
nmap -sV -p- 172.18.5.20 -oX report.xml -oG report.gnmap -oN report.nmap
```

### Exercise 2: Web Application Scanning

**Objective**: Scan for web vulnerabilities using automated tools

```bash
# 1. Nikto - Web server vulnerability scanning
nikto -h 172.18.5.20:3000

# 2. SSL/TLS scanning (if HTTPS available)
testssl.sh --full 172.18.5.20:3000

# 3. HTTP header analysis
curl -I http://172.18.5.20:3000

# 4. Vulnerability scanning with Nmap NSE
nmap -p 3000 --script=http-vulnerabilities 172.18.5.20
```

### Exercise 3: Metasploit Automation

**Objective**: Use Metasploit for automated exploitation

```bash
# Start Metasploit console
msfconsole

# In msfconsole:
> search juice-shop
> use auxiliary/scanner/http/http_version
> set RHOSTS 172.18.5.20
> set RPORT 3000
> run

# Set up workspace
> workspace -a lab5_pentest
> db_status

# Run resource script
> resource scripts/juice_shop_scan.rc
```

### Exercise 4: Create Automated Scanning Script

**Objective**: Combine tools into automated workflow

Create file `automated_scan.sh`:

```bash
#!/bin/bash

TARGET="172.18.5.20"
OUTPUT_DIR="./scan_results"

mkdir -p $OUTPUT_DIR

echo "[*] Starting automated penetration test..."

# Step 1: Port scanning
echo "[*] Running Nmap scan..."
nmap -p- -sV -O $TARGET -oA $OUTPUT_DIR/nmap_full

# Step 2: Web vulnerability scanning
echo "[*] Running Nikto web scan..."
nikto -h $TARGET:3000 -o $OUTPUT_DIR/nikto_report.txt

# Step 3: Service enumeration
echo "[*] Enumerating services..."
nmap -sV -sC -p 3000 $TARGET --script=http-* -oX $OUTPUT_DIR/web_scripts.xml

# Step 4: Generate report summary
echo "[*] Generating report..."
cat > $OUTPUT_DIR/REPORT.txt << EOF
AUTOMATED PENETRATION TEST REPORT
==================================

Target: $TARGET
Date: $(date)

FINDINGS SUMMARY:
- Open Ports: $(grep "^3000" $OUTPUT_DIR/nmap_full.gnmap | wc -l)
- Vulnerabilities Found: Check nikto_report.txt

Next Steps:
1. Manual verification of findings
2. Exploitation of discovered vulnerabilities
3. Documentation of all findings
EOF

echo "[+] Scan complete! Results in $OUTPUT_DIR/"
```

Run the script:

```bash
chmod +x automated_scan.sh
./automated_scan.sh
```

### Exercise 5: Vulnerability Assessment Report

**Objective**: Create structured vulnerability report

Create file `vuln_assessment.md`:

```markdown
# Vulnerability Assessment Report
## Target: 172.18.5.20 (OWASP Juice Shop)

### Executive Summary
- Assessment Date: [Date]
- Duration: [Duration]
- Tools Used: Nmap, Nikto, Metasploit, testssl.sh
- Risk Level: High

### Findings by Severity

#### CRITICAL (0)
- None found

#### HIGH (3)
1. SQL Injection vulnerability
2. Unencrypted sensitive data transmission
3. Default credentials exposure

#### MEDIUM (5)
1. Missing security headers
2. Weak password policy
3. Information disclosure
4. Insecure direct object reference
5. Inadequate error handling

#### LOW (2)
1. Outdated software versions
2. Unnecessary services running

### Remediation Recommendations
[List specific fixes for each vulnerability]

### Proof of Concepts
[Document how each vulnerability was discovered]
```

## Tools Reference

### Nmap Scanning Profiles

```bash
# Quick scan (fastest)
nmap -T4 -F 172.18.5.20

# Comprehensive scan (slowest, most thorough)
nmap -T2 -p- -sV -sC -A -O 172.18.5.20

# UDP scanning
nmap -sU -p- 172.18.5.20

# Service fingerprinting
nmap -sV -p- 172.18.5.20

# OS detection
nmap -O 172.18.5.20

# Script scanning
nmap --script=vuln -p- 172.18.5.20
```

### AutoRecon Usage

```bash
# Basic scan
autorecon 172.18.5.20

# Single host mode
autorecon 172.18.5.20 --single-host

# CIDR range
autorecon 172.18.5.0/24

# Custom ports
autorecon 172.18.5.20 --ports 80,443,3000

# Output to specific directory
autorecon 172.18.5.20 -o ./results/
```

### Metasploit Automation

```bash
# Run resource script
msfconsole -r script.rc

# Output results
msfconsole -r script.rc -o output.txt

# Batch mode
msfconsole -b -r script.rc
```

## OWASP Juice Shop Target

### Known Vulnerabilities

The target application contains 20+ intentional vulnerabilities:

1. **Broken Authentication**
2. **Sensitive Data Exposure**
3. **XML External Entities (XXE)**
4. **Broken Access Control**
5. **Security Misconfiguration**
6. **Cross-Site Scripting (XSS)**
7. **SQL Injection**
8. **Insecure Deserialization**
9. **Using Components with Known Vulnerabilities**
10. **Insufficient Logging & Monitoring**

### Challenge Scoring

Access challenge list:
```
http://localhost:3000/#/score-board
```

Complete challenges to verify successful exploitation.

## Troubleshooting

### Target not starting

```bash
docker-compose logs target

# Restart target
docker-compose restart target
```

### Nmap shows no open ports

```bash
# Verify network connectivity
docker-compose exec kali ping -c 3 172.18.5.20

# Check target is running
docker-compose ps

# Wait for target to fully start
docker-compose logs -f target
```

### Metasploit database errors

```bash
# Inside Kali, initialize database
msfdb init

# Check database status
msfdb status

# Reinitialize if corrupted
msfdb delete
msfdb init
```

### Disk space full during scans

```bash
# Check available space
df -h

# Clean up old scan results
rm -rf scan_results/*

# Reduce verbosity to use less disk
```

## Performance Tips

1. **Run scans in background**:
   ```bash
   naut scan.sh &
   ```

2. **Limit Nmap timing**:
   - `-T0`: Paranoid (slowest)
   - `-T1`: Sneaky
   - `-T2`: Polite (default)
   - `-T3`: Normal
   - `-T4`: Aggressive
   - `-T5`: Insane (fastest, unreliable)

3. **Use parallel scanning**:
   ```bash
   nmap -p- -sV --host-timeout 5m 172.18.5.0/24
   ```

## Cleanup

### Stop containers

```bash
docker-compose stop
```

### Remove containers

```bash
docker-compose down
```

### Complete cleanup

```bash
docker-compose down -v
```

## Resources

- [Metasploit Documentation](https://docs.metasploit.com/)
- [Nmap Manual](https://nmap.org/book/)
- [AutoRecon GitHub](https://github.com/Tib3rius/AutoRecon)
- [Nikto Scanner](https://cirt.net/Nikto2)
- [testssl.sh](https://github.com/drwetter/testssl.sh)
- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)

## Success Criteria

You have completed Lab 5 when you can:

- ✓ Perform automated network reconnaissance
- ✓ Run comprehensive vulnerability scans
- ✓ Execute automated exploits with Metasploit
- ✓ Generate professional assessment reports
- ✓ Identify 15+ vulnerabilities in target
- ✓ Document remediation for each finding

## Next Steps

After completing Lab 5, you should:

1. Study penetration testing methodologies
2. Create standardized scanning templates
3. Move to Lab 6: Undetectable Payloads
4. Practice evasion techniques

---

**Lab Created**: March 2026  
**Last Updated**: March 2026  
**Status**: Ready for Student Use
