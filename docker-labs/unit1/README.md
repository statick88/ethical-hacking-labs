# 🦸 Unit 1: Reconocimiento y Enumeración - LAB PRÁCTICO

## 🎯 Objetivos del Laboratorio

En este laboratorio practicarás **técnicas de reconocimiento y enumeración** atacando objetivos reales en un entorno controlado:

1. **OSINT** - Recolección de información de fuentes abiertas
2. **Escaneo de red** - Identificar hosts y servicios activos
3. **Enumeración de puertos** - Descubrir servicios expuestos
4. **Análisis de servicios** - Identificar versiones y vulnerabilidades

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

---

## 🚀 Iniciar el Laboratorio

```bash
cd docker-labs/unit1
docker-compose up -d
```

### Verificar que todo esté corriendo:

```bash
docker ps | grep -E "kali|target|vuln"
```

**Esperado:**
```
CONTAINER ID   IMAGE                    PORTS                    NAMES
...           ethical-hacking-kali      2222->22, 6080->6080    ethical-hacking-kali
...           target-metasploitable     80->80, 22->2222        target-metasploitable
...           target-coldfusion         80->8081                target-coldfusion
```

---

## 🎯 Objetivos Disponibles para Atacar

| Objetivo | IP | Puertos | Servicio | Vulnerabilidad |
|----------|-----|---------|---------|---------------|
| **Metasploitable2** | 192.168.56.x | 21,22,80,3306 | FTP,SSH,HTTP,MySQL | Múltiples |
| **ColdFusion 10** | 192.168.56.x | 80 | HTTP | ColdFusion |

---

## 🔨 Herramientas de Ataque

Ya incluidas en Kali:
- **nmap** - Escaneo de puertos
- **netdiscover** - Descubrimiento de hosts
- **enum4linux** - Enumeración SMB
- **nikto** - Scanner web
- **whatweb** - Identificación web
- **dirb** - Directorios web
- **wireshark** - Captura de tráfico

---

## ⚔️ EJERCICIOS DE ATAQUE

### Ejercicio 1: Descubrimiento de Red

```bash
# Conectar al Kali
ssh root@localhost -p 2222
# Password: toor

# Descubrir hosts en la red
nmap -sn 192.168.56.0/24

# Escaneo rápido de puertos
nmap -F 192.168.56.0/24
```

### Ejercicio 2: Enumeración de Metasploitable2

```bash
# Escaneo completo
nmap -sV -sC -p- 192.168.56.x

# Enumerar servicios
nmap -sV --script=banner 192.168.56.x

# Detectar SO
nmap -O 192.168.56.x
```

### Ejercicio 3: Enumeración Web

```bash
# Identificar tecnologías
whatweb http://192.168.56.x

# Buscar directorios
nikto -h http://192.168.56.x

# Dirb
dirb http://192.168.56.x
```

### Ejercicio 4: Enumeración SMB

```bash
# Enum4Linux
enum4linux 192.168.56.x

# Nmap scripts SMB
nmap --script=smb-enum-users,smb-enum-shares 192.168.56.x
```

### Ejercicio 5: Análisis de Servicios

```bash
# FTP anónimo
ftp 192.168.56.x
# Probar: anonymous/anonymous

# MySQL
mysql -h 192.168.56.x -u root -p
# Probar sin password

# SSH
ssh -v 192.168.56.x
```

---

## 📋 Checklist de Entrega

| # | Tarea | Completado |
|---|-------|-----------|
| 1 | Hosts activos descubiertos | ☐ |
| 2 | Mapa de puertos completo | ☐ |
| 3 | Servicios identificados con versiones | ☐ |
| 4 | Vulnerabilidades encontradas | ☐ |
| 5 | Informe de reconocimiento | ☐ |

---

## 🛑 cleanup

```bash
# Detener laboratorio
docker-compose down

# Eliminar todo
docker-compose down -v
```

---

## ⚠️ Notas de Seguridad

- **SOLO atacar objetivos dentro de la red del contenedor**
- **NO intentar acceder a redes externas**
- Este es un entorno de aprendizaje controlado
