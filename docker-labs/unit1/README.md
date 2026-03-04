# Unit 1 - Fundamentos y Reconocimiento Agéntico

## Objectives

1. Understand ethical hacking fundamentals
2. Learn agentic reconnaissance techniques
3. Master passive and active information gathering
4. Understand OSINT (Open Source Intelligence) methods
5. Learn to use automated reconnaissance tools

## Tools Included

- **Kali Linux**: Penetration testing distribution
- **Nmap**: Network scanner
- **Wireshark**: Network analyzer
- **Sublist3r**: Subdomain enumeration
- **Dirb**: Web directory enumeration
- **Recon-ng**: Web reconnaissance framework

## Lab Setup

### Build and Start Containers

```bash
cd docker-labs/unit1
docker-compose up -d
```

### Access the Lab

1. **Web Interface**: http://localhost:8080 (Kali Desktop via noVNC)
2. **SSH Access**:
   ```bash
   ssh root@localhost -p 2222
   Password: toor
   ```

### Stop and Cleanup

```bash
cd docker-labs/unit1
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v
```

## Lab Exercises

### Exercise 1: Network Scanning with Nmap

1. Scan a target network:
   ```bash
   nmap -sP 192.168.0.0/24
   ```

2. Perform a detailed scan:
   ```bash
   nmap -sV -sC -p- 192.168.0.100
   ```

3. Save scan results:
   ```bash
   nmap -oN scan_results.txt -oX scan_results.xml 192.168.0.100
   ```

### Exercise 2: Web Reconnaissance with Recon-ng

1. Start Recon-ng:
   ```bash
   recon-ng
   ```

2. Add a domain:
   ```bash
   [recon-ng] > use recon/domains-hosts/baidu_site
   [recon-ng] > set SOURCE example.com
   [recon-ng] > run
   ```

3. Export results:
   ```bash
   [recon-ng] > use report/csv
   [recon-ng] > set FILENAME results.csv
   [recon-ng] > run
   ```

### Exercise 3: Subdomain Enumeration

1. Use Sublist3r:
   ```bash
   sublist3r -d example.com -o subdomains.txt
   ```

2. Use dirb to find hidden directories:
   ```bash
   dirb http://example.com
   ```

### Exercise 4: Packet Analysis with Wireshark

1. Capture network traffic:
   ```bash
   tcpdump -i eth0 -w capture.pcap
   ```

2. Analyze captured packets:
   ```bash
   wireshark capture.pcap
   ```

### Exercise 5: OSINT Gathering

1. Search for information about a target:
   ```bash
   python3 -m pip install google
   python3 google-search.py "target company"
   ```

2. Check social media:
   ```bash
   python3 social-scan.py "target_username"
   ```

## Resources

- [Nmap Documentation](https://nmap.org/book/man.html)
- [Wireshark Documentation](https://www.wireshark.org/docs/)
- [Recon-ng Wiki](https://github.com/lanmaster53/recon-ng/wiki)
- [Sublist3r](https://github.com/aboul3la/Sublist3r)
- [OSINT Framework](https://osintframework.com/)

## Troubleshooting

### Cannot connect to Kali desktop

Check container status:
```bash
cd docker-labs/unit1
docker-compose ps
```

### VNC connection fails

Check if the container is running and port is exposed:
```bash
netstat -tuln | grep 8080
```

### Permission denied when running Nmap

Run Nmap as root:
```bash
sudo nmap -sP 192.168.0.0/24
```
