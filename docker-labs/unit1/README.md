# 🦸 Unit 1: Reconocimiento y Enumeración - LAB PRÁCTICO

## 📋 Requisitos Previos

Antes de comenzar este laboratorio, asegúrate de tener:

### Software Requerido
- **Docker** instalado y funcionando
- **Docker Compose** instalado
- **Cliente SSH** (OpenSSH en Linux/Mac, PuTTY o Wingit en Windows)
- **Navegador web** para acceder a la interfaz VNC de Kali

### Conocimientos Previos (Recomendados)
- Conceptos básicos de redes (TCP/IP, puertos, protocolos)
- Familiaridad con la línea de comandos
- Qué es una dirección IP y una red local

### Recursos Adicionales
- [Guía de Nmap](https://nmap.org/book/man.html)
- [Documentación de Kali Linux](https://www.kali.org/docs/)

---

## 🎯 Objetivos de Aprendizaje

Al completar este laboratorio serás capaz de:

1. ✅ **Identificar hosts activos** en una red local usando técnicas de descubrimiento
2. ✅ **Enumerar puertos abiertos** y determinar qué servicios están funcionando
3. ✅ **Identificar versiones de servicios** y tecnologías web
4. ✅ **Recopilar información** para planificar un ataque
5. ✅ **Documentar hallazgos** de manera profesional

---

## 🏗️ Arquitectura del Laboratorio

```
┌──────────────────────────────────────────────────────────────────┐
│                      LABORATORIO 1                                │
│                   RECONOCIMIENTO Y ENUMERACIÓN                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────────┐                            ┌─────────────┐    │
│   │    KALI    │        ATAQUE               │   OBJETIVOS │    │
│   │   LINUX    │  ──────────────────────→     │   VULNES   │    │
│   │ (Atacante) │                            │             │    │
│   │ 192.168.56 │                            │             │    │
│   └─────────────┘                            └─────────────┘    │
│        │                                            │            │
│        │  • Nmap                                    │            │
│        │  • Netdiscover                            │            │
│        │  • Enum4linux                            │            │
│        │  • Nikto                                 │            │
│        │  • WhatWeb                              │            │
│        │                                          │            │
│        │        ┌─────────────┐  ┌────────────┐  │            │
│        │        │ Metasploita │  │ ColdFusion│  │            │
│        │        │    ble 2    │  │    10     │  │            │
│        │        │ :80,21,22  │  │   :80     │  │            │
│        │        │ 3306,2121  │  │            │  │            │
│        │        └─────────────┘  └────────────┘  │            │
│        │                                          │            │
│        │            RED: 192.168.56.0/24          │            │
└────────┼──────────────────────────────────────────┼────────────┘
         │
     SSH:2222
     VNC:6080
```

### Direcciones IP Asignadas (Ejemplo)
| Máquina | IP Asignada | Servicios |
|---------|-------------|-----------|
| Kali Linux | 192.168.56.2 | SSH, VNC |
| Metasploitable2 | 192.168.56.3 | FTP, SSH, HTTP, MySQL, etc. |

**Nota**: Las IPs pueden variar. Usa `docker network inspect` para verificar las IPs reales.

---

## 🚀 INSTRUCCIONES DETALLADAS DE INSTALACIÓN

### Paso 1: Verificar Docker

```bash
# Verificar que Docker esté instalado
docker --version

# Verificar que Docker Compose esté instalado
docker-compose --version

# Verificar que el servicio esté corriendo
docker ps
```

Si Docker no está instalado, sigue las instrucciones en: https://docs.docker.com/engine/install/

### Paso 2: Iniciar el Laboratorio

```bash
# Navegar al directorio del laboratorio
cd docker-labs/unit1

# Iniciar los contenedores
docker-compose up -d
```

### Paso 3: Verificar que los Contenedores estén Corriendo

```bash
# Ver todos los contenedores activos
docker ps

# Ver la red del laboratorio
docker network ls | grep lab-network

# Inspeccionar la red para ver las IPs
docker network inspect docker-labs_lab-network
```

**Deberías ver:**
- `ethical-hacking-kali` - Contenedor de Kali Linux
- `target-metasploitable` - Objetivo vulnerable Metasploitable2

### Paso 4: Acceder a Kali Linux

Tienes DOS opciones para acceder a Kali:

#### Opción A: SSH (Recomendado)
```bash
# Conectar por SSH
ssh root@localhost -p 2222

# Password: toor
```

#### Opción B: VNC (Interfaz Gráfica)
```bash
# Abrir en navegador
http://localhost:6080

# No requiere password (en modo desarrollo)
```

### Paso 5: Verificar Conectividad desde Kali

Una vez dentro de Kali:
```bash
# Verificar IP asignada
ip addr show eth0

# Hacer ping al objetivo
ping -c 3 192.168.56.3

# Escaneo inicial para descubrir hosts
nmap -sn 192.168.56.0/24
```

---

## 🎯 Objetivos Disponibles para Atacar

| Objetivo | IP | Puertos | Servicio | Vulnerabilidad |
|----------|-----|---------|---------|---------------|
| **Metasploitable2** | 192.168.56.x | 21,22,80,3306 | FTP,SSH,HTTP,MySQL | Múltiples |

---

## 🔨 Herramientas de Ataque Disponibles

Kali Linux ya viene con estas herramientas preinstaladas:

| Herramienta | Función | Comando Básico |
|-------------|---------|----------------|
| **nmap** | Escaneo de puertos | `nmap -sV objetivo` |
| **netdiscover** | Descubrimiento de red | `netdiscover -r 192.168.56.0/24` |
| **enum4linux** | Enumeración SMB | `enum4linux -a objetivo` |
| **nikto** | Scanner web | `nikto -h http://objetivo` |
| **whatweb** | Identificación web | `whatweb http://objetivo` |
| **dirb** | Buscar directorios | `dirb http://objetivo` |
| **wireshark** | Captura de tráfico | `wireshark &` |
| **tcpdump** | Análisis de tráfico | `tcpdump -i eth0` |

---

## ⚔️ EJERCICIOS DE ATAQUE - GUÍA DETALLADA

### Ejercicio 1: Descubrimiento de Red

**Objetivo**: Identificar todos los hosts activos en la red del laboratorio

**Duración estimada**: 10 minutos

**Procedimiento**:

```bash
# 1. Conectar a Kali
ssh root@localhost -p 2222
# Password: toor

# 2. Ver nuestra IP
ip addr show eth0
# Anota la IP (ejemplo: 192.168.56.2)

# 3. Descubrir hosts con Nmap (Ping Sweep)
nmap -sn 192.168.56.0/24

# 4. También puedes usar Netdiscover
netdiscover -r 192.168.56.0/24 -i eth0

# 5. Ver la tabla ARP
arp-scan -l
```

**Expected Output (ejemplo)**:
```
Nmap scan report for 192.168.56.2
Host is up (0.00010s latency).
Nmap scan report for 192.168.56.3
Host is up (0.00064s latency).
Nmap done: 256 IP addresses (2 hosts up) scanned in 2.34 seconds
```

**Entregable**: Lista de IPs activas con su MAC address

---

### Ejercicio 2: Enumeración de Puertos con Nmap

**Objetivo**: Descubrir todos los puertos abiertos en Metasploitable2

**Duración estimada**: 15 minutos

**Procedimiento**:

```bash
# 1. Escaneo rápido (los 100 puertos más comunes)
nmap -F 192.168.56.3

# 2. Escaneo completo de puertos (todos los 65535)
nmap -p- 192.168.56.3

# 3. Escaneo con detección de servicios y versiones
nmap -sV 192.168.56.3

# 4. Escaneo completo con scripts por defecto
nmap -sC 192.168.56.3

# 5. Escaneo Ultra completo (combina todo)
nmap -A -p- 192.168.56.3
```

**Explicación de flags**:
- `-p-`: Todos los puertos (1-65535)
- `-sV`: Detectar versiones de servicios
- `-sC`: Ejecutar scripts por defecto
- `-A`: Detección de SO, versiones, scripts y traceroute

**Expected Output (ejemplo)**:
```
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 2.3.4
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
23/tcp   open  telnet      Linux telnetd
25/tcp   open  smtp        Postfix smtpd
80/tcp   open  http        Apache httpd 2.2.8 ((Ubuntu) PHP/5.2.4-2ubuntu5.10)
...
```

**Entregable**: Tabla completa de puertos, servicios y versiones

---

### Ejercicio 3: Enumeración de Servicios Web

**Objetivo**: Identificar tecnologías y vulnerabilidades web

**Duración estimada**: 15 minutos

**Procedimiento**:

```bash
# 1. Identificar tecnologías con WhatWeb
whatweb http://192.168.56.3

# 2. Escaneo con Nikto
nikto -h http://192.168.56.3

# 3. Buscar directorios con Dirb
dirb http://192.168.56.3/

# 4. Enumeración con Nmap scripts HTTP
nmap --script=http-enum,http-title,http-headers 192.168.56.3
```

**Análisis de resultados**:
- WhatWeb muestra tecnologías (Apache, PHP, versión de Ubuntu)
- Nikto muestra vulnerabilidades potenciales
- Dirb descubre directorios ocultos

**Entregable**: Lista de vulnerabilidades web encontradas

---

### Ejercicio 4: Enumeración SMB (Linux/Windows)

**Objetivo**: Enumerar recursos compartidos y usuarios SMB

**Duración estimada**: 10 minutos

**Procedimiento**:

```bash
# 1. Enumeración completa con Enum4linux
enum4linux -a 192.168.56.3

# 2. Solo información del SO
enum4linux -o 192.168.56.3

# 3. Solo usuarios
enum4linux -U 192.168.56.3

# 4. Solo recursos compartidos
enum4linux -S 192.168.56.3

# 5. Nmap scripts SMB
nmap --script=smb-enum-users,smb-enum-shares 192.168.56.3
```

**Entregable**: Lista de usuarios y recursos compartidos encontrados

---

### Ejercicio 5: Análisis de Servicios Específicos

**Objetivo**: Conectar a servicios específicos y buscar vulnerabilidades

**Duración estimada**: 20 minutos

#### 5.1 FTP (Puerto 21)

```bash
# Conectar como anonymous
ftp 192.168.56.3
# Usuario: anonymous
# Password: (cualquier email)

# Listar archivos
ls

# Descargar archivos
get archivo.txt

# Salir
bye
```

#### 5.2 SSH (Puerto 22)

```bash
# Ver banner SSH
ssh -v 192.168.56.3

# Probar credenciales por defecto
# Usuario: msfadmin / msfadmin
ssh msfadmin@192.168.56.3
```

#### 5.3 MySQL (Puerto 3306)

```bash
# Intentar conexión sin password
mysql -h 192.168.56.3 -u root

# Si entra, enumerar bases de datos
show databases;
use mysql;
show tables;
select * from user;
```

#### 5.4 Telnet (Puerto 23)

```bash
# Conectar a Telnet
telnet 192.168.56.3

# Explorar el servicio
```

---

## 📊 Plantilla de Documentación de Hallazgos

Crea un documento con esta estructura:

```markdown
# Informe de Reconocimiento - Laboratorio 1

## 1. Resumen Ejecutivo
[Breve descripción de lo encontrado]

## 2. Hosts Descubiertos
| IP | Hostname | Estado | SO (supuesto) |
|----|----------|--------|----------------|
| 192.168.56.2 | kali | Activo | Kali Linux |
| 192.168.56.3 | metasploitable | Activo | Ubuntu 8.04 |

## 3. Servicios Enumerados - Metasploitable2 (192.168.56.3)

### Puerto 21 - FTP
- Servicio: vsftpd 2.3.4
- Estado: Ejecutando
- Vulnerabilidades potenciales: anonymous FTP enabled

### Puerto 22 - SSH
- Servicio: OpenSSH 4.7p1
- Estado: Ejecutando
- Info: Debian 8ubuntu1

[Continuar con todos los puertos...]

## 4. Vulnerabilidades Identificadas
1. [Vulnerabilidad 1]
2. [Vulnerabilidad 2]

## 5. Recomendaciones para siguiente fase
- [Ataque 1 a intentar]
- [Ataque 2 a intentar]

## 6. Evidencia
[Capturas de pantalla de los escaneos]
```

---

## 📋 Checklist de Entrega

| # | Tarea | Completado |
|---|-------|-----------|
| 1 | Hosts activos descubiertos | ☐ |
| 2 | Mapa de puertos completo | ☐ |
| 3 | Servicios identificados con versiones | ☐ |
| 4 | Tecnologías web identificadas | ☐ |
| 5 | Enumeración SMB completada | ☐ |
| 6 | Análisis de servicios (FTP, SSH, MySQL) | ☐ |
| 7 | Informe de reconocimiento | ☐ |

---

## 🔧 Troubleshooting

### Problema: No puedo conectar por SSH
```bash
# Verificar que el contenedor esté corriendo
docker ps | grep kali

# Ver logs del contenedor
docker logs ethical-hacking-kali

# Reiniciar el servicio SSH dentro del contenedor
docker exec -it ethical-hacking-kali service ssh restart
```

### Problema: No puedo ver las IPs de los contenedores
```bash
# Inspeccionar la red
docker network inspect docker-labs_lab-network

# Ver logs del objetivo
docker logs target-metasploitable

# Reiniciar contenedores
docker-compose restart
```

### Problema: Los contenedores no inician
```bash
# Ver errores
docker-compose logs

# Reconstruir desde cero
docker-compose down -v
docker-compose up --build
```

---

## 🛑 LIMPIEZA DEL LABORATORIO

```bash
# Navegar al directorio
cd docker-labs/unit1

# Detener contenedores (mantiene datos)
docker-compose down

# Eliminar contenedores y volúmenes (LIMPIEZA TOTAL)
docker-compose down -v

# Verificar que no queden contenedores
docker ps -a | grep -E "kali|metasploitable"
```

---

## ⚠️ Notas de Seguridad - IMPORTANTE

- **SOLO atacar objetivos dentro de la red del contenedor (192.168.56.0/24)**
- **NO intentar acceder a redes externas**
- **NO compartir las credenciales usadas** (son para aprendizaje)
- Este es un entorno de aprendizaje controlado
- Siempre documenta tus hallazgos

---

## ✅ Próximo Laboratorio

Una vez completado este laboratorio, continúa con:
- **Unit 2**: Vulnerabilidades en IA y LLMs
- Aprenderás sobre Prompt Injection y Jailbreak Attacks

---

## 📚 Recursos Adicionales

- [Nmap Official Documentation](https://nmap.org/book/man.html)
- [Kali Linux Tools](https://www.kali.org/tools/)
- [Metasploitable2 Documentation](https://docs.rapid7.com/metasploitploit/metasploitable-2)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
