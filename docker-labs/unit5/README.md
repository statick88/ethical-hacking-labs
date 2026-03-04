# Unit 5 - Pentesting Autónomo y Red Teaming Agéntico

## Objectives

1. Learn autonomous pentesting techniques
2. Understand AI-assisted red teaming
3. Master automated vulnerability scanning
4. Learn to create custom exploitation scripts
5. Understand CI/CD security testing

## Tools Included

- **Kali Linux**: Penetration testing distribution
- **Nmap**: Network scanner
- **OpenVAS**: Vulnerability scanner
- **Metasploit**: Exploitation framework
- **Wfuzz**: Web fuzzer
- **AI Scanner**: AI-powered vulnerability detection

## Lab Setup

### Build and Start Containers

```bash
cd docker-labs/unit5
docker-compose up -d
```

### Access the Lab

1. **Web Interface**: http://localhost:8084 (Kali Desktop via noVNC)
2. **SSH Access**:
   ```bash
   ssh root@localhost -p 2226
   Password: toor
   ```

### Stop and Cleanup

```bash
cd docker-labs/unit5
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v
```

## Lab Exercises

### Exercise 1: Automated Scanning with OpenVAS

1. Start OpenVAS services:
   ```bash
   gsad --listen=0.0.0.0 --port=9392
   gvmd --listen=0.0.0.0 --port=9390
   ospd-openvas --listen=0.0.0.0 --port=9391
   ```

2. Access OpenVAS web interface: http://localhost:9392

### Exercise 2: Metasploit Automation

1. Start Metasploit console:
   ```bash
   msfconsole
   ```

2. Run automated scan:
   ```bash
   db_nmap -sV 192.168.0.105
   ```

3. Run exploit suggestion:
   ```bash
   db_services
   db_autopwn -p -t -e
   ```

### Exercise 3: Custom Script Development

1. Create a Python exploit script:
   ```python
   import socket

   target_ip = "192.168.0.105"
   target_port = 80

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect((target_ip, target_port))
   s.sendall(b"GET /exploit HTTP/1.1\r\nHost: vulnerable\r\n\r\n")
   data = s.recv(1024)
   print(data.decode())
   ```

2. Run the script:
   ```bash
   python3 exploit.py
   ```

### Exercise 4: AI-Powered Vulnerability Detection

1. Run AI scanner on target:
   ```bash
   ai-scanner scan http://192.168.0.105 --output results.json
   ```

2. Analyze results:
   ```bash
   cat results.json | jq '.'
   ```

## Resources

- [Metasploit Documentation](https://docs.metasploit.com/)
- [OpenVAS Documentation](https://docs.greenbone.net/GSM-Manual/gos-22.04/index.html)
- [Nmap Documentation](https://nmap.org/book/index.html)
- [AI Security Resources](https://openai.com/research/security)

## Troubleshooting

### OpenVAS won't start

Check service status:
```bash
cd docker-labs/unit5
docker exec -it kali gsad --status
```

### Metasploit database connection failed

Reconnect to database:
```bash
cd docker-labs/unit5
docker exec -it kali msfdb reinit
```
