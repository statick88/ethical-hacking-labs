# Lab 1: Reconocimiento y Enumeración

## Objetivos

- Realizar reconocimiento pasivo con herramientas OSINT
- Escanear una red y enumerar puertos con Nmap
- Enumerar servicios vulnerables con scripts de Nmap
- Analizar una máquina vulnerable (Metasploitable 2)
- Documentar hallazgos de seguridad

## Prerrequisitos

- Docker Engine 24.0 o superior
- Docker Compose 2.0 o superior
- 8GB RAM mínimo (16GB recomendado)
- 10GB de almacenamiento disponible
- Conexión a internet para descargar imágenes

## Arquitectura

```
lab1-net (172.18.1.0/24)
├── kali (172.18.1.10) — Atacante con herramientas de reconocimiento
└── metasploitable2 (172.18.1.20) — Objetivo vulnerable
```

## Setup

### Paso 1: Clonar el repositorio (si no lo has hecho)

```bash
cd /ruta/a/tu/directorio
git clone <repo-url>
cd Ethical_Hacking/docker-labs/lab1
```

### Paso 2: Levantar el entorno

```bash
# Levantar servicios en modo detached (fondo)
docker compose up -d

# Verificar que los servicios están corriendo
docker compose ps
```

### Paso 3: Acceder a la máquina Kali

```bash
# Ingresar a la consola de Kali
docker compose exec kali bash

# Actualizar paquetes e instalar herramientas
apt update && apt install -y nmap whois dig theharvester subfinder gobuster enum4linux
```

## Laboratorio

### Paso 1: Reconocimiento Pasivo

**Objetivo**: Recolectar información sobre el objetivo sin interactuar directamente con él.

```bash
# Verificar conectividad a metasploitable
ping 172.18.1.20

# Obtener información DNS (simulada)
host metasploitable2
```

### Paso 2: Escaneo de Red con Nmap

**Objetivo**: Identificar puertos abiertos y servicios.

```bash
# Escaneo TCP SYN rápido
nmap -sS -F 172.18.1.20

# Escaneo completo con detección de servicios
nmap -sS -sV -sC -p- 172.18.1.20 -oN scan_full.txt

# Detección de sistema operativo
nmap -O 172.18.1.20

# Scripts de vulnerabilidad
nmap --script vuln 172.18.1.20
```

**Output esperado**:
```
Starting Nmap 7.93 ( https://nmap.org ) at 2026-03-04 10:30 UTC
Nmap scan report for metasploitable2 (172.18.1.20)
Host is up (0.00023s latency).
Not shown: 65523 closed tcp ports (reset)
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.3.4
22/tcp  open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1
23/tcp  open  telnet      Linux telnetd
25/tcp  open  smtp        Postfix smtpd
80/tcp  open  http        Apache httpd 2.2.8 ((Ubuntu) DAV/2)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
3306/tcp open mysql        MySQL 5.0.51a-3ubuntu5
8080/tcp open http        Apache Tomcat/Coyote JSP engine 1.1
```

### Paso 3: Enumeración de Servicios

```bash
# Enumeración FTP (anónimo)
ftp 172.18.1.20
# Usuario: anonymous
# Contraseña: anonymous

# Enumeración SMB
enum4linux 172.18.1.20

# Enumeración HTTP
whatweb http://172.18.1.20
nikto -h http://172.18.1.20

# Enumeración de directorios web
gobuster dir -u http://172.18.1.20 -w /usr/share/wordlists/dirb/common.txt
```

### Paso 4: Análisis de Vulnerabilidades

```bash
# Crear resumen de hallazgos
cat > reconnaissance_report.md << EOF
# Reporte de Reconocimiento — Metasploitable2
## Objetivo: 172.18.1.20
## Fecha: $(date)

---

## Información Básica

IP: 172.18.1.20
Hostname: metasploitable2

---

## Puertos Abiertos y Servicios

$(grep "^[0-9]*\/" scan_full.txt)

---

## Vulnerabilidades Detectadas

1. **FTP vsftpd 2.3.4**: Vulnerable a backdoor (CVE-2011-2523)
2. **Apache httpd 2.2.8**: Vulnerable a Directory Traversal
3. **Samba smbd 3.X**: Vulnerable a Remote Code Execution
4. **MySQL 5.0.51a**: Vulnerable a autenticación bypass

---

## Recomendaciones

1. Cerrar el puerto 21 (FTP anónimo)
2. Actualizar Apache a la última versión
3. Configurar autenticación fuerte en MySQL
4. Implementar firewall para filtrar tráfico

EOF

# Verificar el reporte
cat reconnaissance_report.md
```

## Troubleshooting

### Problema: No hay conectividad entre contenedores

**Solución**: Verifica que la red `lab1-net` esté creada:

```bash
docker network ls
docker network inspect lab1-net
```

### Problema: No se puede acceder a Kali

**Solución**: Reinicia el servicio:

```bash
docker compose restart kali
docker compose exec kali bash
```

### Problema: Nmap no está instalado

**Solución**: Instálalo desde dentro de Kali:

```bash
apt update && apt install -y nmap
```

## Cleanup

### Paso 1: Parar los servicios

```bash
docker compose down
```

### Paso 2: Eliminar volúmenes (opcional)

```bash
docker compose down -v
```

### Paso 3: Eliminar imágenes (opcional)

```bash
docker rmi kalilinux/kali-rolling tutum/metasploitable:latest
```

## Recursos

- [Nmap Documentation](https://nmap.org/book/man.html)
- [Metasploitable 2 Vulnerabilities](https://docs.rapid7.com/metasploit/metasploitable-2/)
- [OSINT Framework](https://osintframework.com/)
