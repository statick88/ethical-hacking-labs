# 🦸 Unit 7: Ciberseguridad Industrial - LAB PRÁCTICO

## 🎯 Objetivos

Practicar **ataques a sistemas ICS/SCADA**:

1. **Modbus** - Protocolo industrial
2. **Enumeración PLC** - Encontrar dispositivos
3. **Lectura/Escritura** - Manipular registros
4. **Hardening** - Proteger sistemas ICS

---

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────────────────┐
│                      LABORATORIO 7                                │
│                 CIBERSEGURIDAD INDUSTRIAL                           │
├──────────────────────────────────────────────────────────────────┤
│   ┌─────────────┐                            ┌─────────────┐      │
│   │    KALI    │        ATAQUE              │    PLC      │      │
│   │   LINUX    │  ──────────────────────→  │  OpenPLC    │      │
│   │ (Atacante) │                            │             │      │
│   └─────────────┘                            └─────────────┘      │
│        │                                            │              │
│        │  • nmap                                   │              │
│        │  • pymodbus                            │              │
│        │  • Wireshark                         │              │
│        │        ┌─────────────┐               │              │
│        │        │  Modbus    │               │              │
│        │        │   :502     │               │              │
│        │        └─────────────┘               │              │
│        │            RED: 192.168.62.0/24   │              │
└────────┼──────────────────────────────────────┼──────────────┘
         │
    SSH:2222
```

---

## 🚀 Iniciar

```bash
cd docker-labs/unit7
docker-compose up -d
```

---

## ⚔️ EJERCICIOS DE ATAQUE

### Ejercicio 1: Reconocimiento ICS

```bash
ssh root@localhost -p 2222

# Escanear puertos Modbus
nmap -p 502 192.168.62.x

# Detectar servicios
nmap -sV -p 502 192.168.62.x
```

### Ejercicio 2: Conexión Modbus

```bash
# Con Python
python3 << 'EOF'
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('192.168.62.x', port=502)
result = client.read_holding_registers(0, 10, slave=1)
print(result.registers)
client.close()
EOF
```

### Ejercicio 3: Leer Registros

```bash
# Leer coils
python3 -c "
from pymodbus.client import ModbusTcpClient
c = ModbusTcpClient('192.168.62.x')
r = c.read_coils(0, 10, slave=1)
print('Coils:', r.bits)
"
```

---

## 🛑 Cleanup

```bash
docker-compose down -v
```
