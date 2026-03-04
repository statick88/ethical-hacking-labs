# Unit 7 - Ciberseguridad Industrial

## Objectives

1. Understand industrial control systems (ICS) and SCADA
2. Learn Modbus, DNP3, and other industrial protocols
3. Master ICS vulnerability assessment
4. Learn SCADA system exploitation
5. Understand ICS security best practices

## Tools Included

- **Kali Linux**: Penetration testing distribution
- **Modbus Tools**: Modbus protocol testing
- **DNP3 Tools**: DNP3 protocol testing
- **Wireshark**: Network analyzer
- **ICS Simulator**: SCADA/ICS simulation

## Lab Setup

### Build and Start Containers

```bash
cd docker-labs/unit7
docker-compose up -d
```

### Access the Lab

1. **Web Interface**: http://localhost:8086 (Kali Desktop via noVNC)
2. **SSH Access**:
   ```bash
   ssh root@localhost -p 2228
   Password: toor
   ```

### Stop and Cleanup

```bash
cd docker-labs/unit7
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v
```

## Lab Exercises

### Exercise 1: Modbus Protocol Analysis

1. Capture Modbus traffic:
   ```bash
   tcpdump -i eth0 port 502 -w modbus.pcap
   ```

2. Analyze with Wireshark:
   ```bash
   wireshark modbus.pcap
   ```

### Exercise 2: Modbus Exploitation

1. Read Modbus registers:
   ```bash
   modbusclient -m tcp -a 1 -r 1 -c 10 192.168.0.107:502
   ```

2. Write to Modbus coil:
   ```bash
   modbusclient -m tcp -a 1 -w 1 192.168.0.107:502
   ```

### Exercise 3: DNP3 Protocol Testing

1. Test DNP3 connection:
   ```bash
   dnp3test -a 192.168.0.107 -p 20000 -m master -c 1
   ```

2. Analyze DNP3 traffic:
   ```bash
   tcpdump -i eth0 port 20000 -w dnp3.pcap
   ```

### Exercise 4: ICS Vulnerability Scanning

1. Scan for ICS vulnerabilities:
   ```bash
   nmap -sV -p 502,20000,44818 192.168.0.107 --script="nse/*modbus* and nse/*dnp3*"
   ```

2. Check for outdated firmware:
   ```bash
   python3 ics_scanner.py -t 192.168.0.107 --check-firmware
   ```

## Resources

- [Modbus Protocol Documentation](https://www.modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf)
- [DNP3 Protocol Documentation](https://www.dnp.org/TechnicalResources/DNP3/DNP3_Standards.aspx)
- [ICS Security Resources](https://www.us-cert.gov/ics)
- [Wireshark ICS Protocol Support](https://wiki.wireshark.org/IndustrialProtocols)

## Troubleshooting

### Cannot connect to ICS device

Check physical connections and network settings

### Protocol errors in Wireshark

Verify protocol version and port settings in Wireshark preferences
