# 🛡️ Ethical Hacking Labs & Ebook

**ABACOM™ Capacitación y Servicios Informáticos**  
Acreditado por SETEC-CAL-2019-0183 (Ministerio de Trabajo, Ecuador)  
📍 Loja, Ecuador

---

## 📚 Contenido

Este repositorio contiene los **laboratorios Docker** y el **ebook Quarto** para el curso **"Introducción a Ethical Hacking"** modernizado (2026).

### 📁 Estructura

```
ethical-hacking-labs/
├── labs/                 # 8 laboratorios Docker hands-on
│   ├── lab1/            # Fundamentos y Reconocimiento Agéntico
│   ├── lab2/            # Vulnerabilidades en IA y LLMs
│   ├── lab3/            # Explotación Web y APIs 2026
│   ├── lab4/            # Hacking de Identidad y AD Moderno
│   ├── lab5/            # Pentesting Autónomo y Red Teaming Agéntico
│   ├── lab6/            # Evasión de Defensas
│   ├── lab7/            # Ciberseguridad Industrial
│   └── lab8/            # Post-Explotación, Reporte y Ética (Capstone)
└── ebook/               # Ebook Quarto con contenido del curso
    ├── index.qmd        # Portada e índice principal
    └── presentaciones/  # Presentaciones por unidad
```

---

## 🚀 Inicio Rápido

### Prerrequisitos

- **Docker** y **Docker Compose** (instalados)
- **Git** (para clonar el repositorio)
- Para el ebook: **Quarto** (`quarto --version`)

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/abacom/ethical-hacking-labs.git
cd ethical-hacking-labs
```

### 2️⃣ Ejecutar un Laboratorio

Cada laboratorio es independiente y tiene su propio `docker-compose.yml`:

```bash
cd labs/lab1
docker-compose up -d
```

Consulta el `README.md` en cada carpeta de lab para instrucciones específicas.

### 3️⃣ Generar el Ebook

```bash
cd ebook
quarto render index.qmd --to html
# O PDF
quarto render index.qmd --to pdf
```

---

## 📖 Currículo (150 horas)

### 🔴 Módulo I: Fundamentos y Reconocimiento Agéntico (15h)
- OSINT avanzada con herramientas de IA
- Reconocimiento pasivo y activo automatizado
- Escaneo adaptativo con Nmap + IA
- Enumeración de servicios y vulnerabilidades
- Setup de laboratorio con Docker

**Lab**: `labs/lab1/`

---

### 🟠 Módulo II: Vulnerabilidades en IA y Modelos de Lenguaje (20h)
- Prompt Injection y Jailbreaking
- Técnicas de Jailbreak para Bug Bounty: DAN, RUIN, Master-of-Prompt
- Ataques a APIs de LLMs
- Token smuggling y context overflow
- Evaluación de seguridad de LLMs
- Defensa contra Prompt Attacks
- Bug Bounty en plataformas de IA: OpenAI, Anthropic, Google

**Lab**: `labs/lab2/`

---

### 🟡 Módulo III: Explotación Web y APIs 2026 (20h)
- OWASP Top 10 2025
- GraphQL Security Testing
- Business Logic Vulnerabilities
- Server-Side Request Forgery (SSRF)
- API REST Security con OWASP ZAP

**Lab**: `labs/lab3/`

---

### 🟢 Módulo IV: Hacking de Identidad y AD Moderno (20h)
- Active Directory Attacks
- Golden Ticket y Silver Ticket
- Kerberoasting y AS-REP Roasting
- Elusión de MFA y Pass-the-Cookie
- Zero Trust 2.0: ZTNA vs VPN

**Lab**: `labs/lab4/`

---

### 🔵 Módulo V: Pentesting Autónomo y Red Teaming Agéntico (20h)
- XBOW: Cross Site OWASP Scanning
- Orquestación de agentes de pentesting
- Automatización de reconocimiento
- Red Team Operations
- C2 frameworks: Sliver, Mythic

**Lab**: `labs/lab5/`

---

### 🟣 Módulo VI: Evasión de Defensas (20h)
- Bypass de EDRs modernas
- Technique for Evading Trend Micro (Tricks)
- Zig: Modern payload generation
- Living Off the Land (LOLBAS)
- Process injection techniques

**Lab**: `labs/lab6/`

---

### ⚫ Módulo VII: Ciberseguridad Industrial (20h)
- Arquitectura OT/ICS
- Protocolos Industriales: Modbus, OPC-UA, MQTT
- SCADA Security Assessment
- IoT Vulnerabilities
- Hardening de Sistemas Industriales con OpenClaw
- Pentesting Automatizado con Pentagi
- Herramientas: PLCSploit, s7scan, OpenClaw, Pentagi

**Lab**: `labs/lab7/`

---

### ⚪ Módulo VIII: Post-Explotación, Reporte y Ética (15h)
- Post-explotación y pivoting
- Persistencia y covert channels
- Reporting profesional
- Marco legal: GDPR, DORA
- Código de ética del hacker ético

**Lab**: `labs/lab8/` (Capstone Project)

---

## 🔧 Herramientas Principales

| Categoría | Herramientas |
|-----------|-------------|
| **Reconocimiento** | Nmap, Shodan, SpiderFoot, theHarvester, Recon-ng |
| **Web** | OWASP ZAP, Burp Suite, SQLi, XSS, GraphQL tools |
| **Active Directory** | Mimikatz, BloodHound, CrackMapExec, Rubeus |
| **Automatización** | Python, Bash, n8n, Make.com |
| **Evasión** | Zig, Sliver, Mythic, Covenant |
| **OT/ICS** | OpenClaw, Pentagi, s7scan, PLCSploit |
| **Reporting** | Markdown, HTML, PDF, Obsidian |

---

## 🧪 Plataformas Online (CTF & Práctica)

- **TryHackMe** — Máquinas guiadas (nivel principiante/intermedio)
- **HackTheBox** — Máquinas reales y desafíos (nivel avanzado)
- **OverTheWire** — Wargames y desafíos progresivos
- **PicoCTF** — Competencia anual, desafíos educativos

---

## 📜 Certificaciones Objetivo

### 🥇 Primaria
- **OSCP+** — Offensive Security Certified Professional Plus (180 horas)

### 🥈 Secundaria
- **CEH v13** — Certified Ethical Hacker (experiencia + examen)

### 🎯 Alternativas (según especialización)
- **Bug Bounty certifications** (Intigriti, HackerOne)
- **eCRE** — eLearnSecurity Certified Penetration Tester
- **GIAC certifications** (GPEN, GWAPT)

---

## 📋 Requisitos del Curso

### Conocimientos Previos
- Computación básica
- Fundamentos de redes (TCP/IP)
- Conceptos básicos de Linux

### Hardware/Software (Online)
- Computadora con mínimo 8GB RAM
- Docker y Docker Compose instalados
- Terminal/Bash
- Navegador web (Chrome, Firefox)
- Webcam, micrófono, parlantes/audífonos

---

## 🎓 Estructura del Curso

| Componente | Duración | Descripción |
|-----------|----------|------------|
| **Clases Teóricas** | 60h | Conceptos, metodologías, herramientas |
| **Laboratorios Prácticos** | 70h | Hands-on con Docker labs + CTF platforms |
| **Proyecto Capstone** | 15h | Lab 8: Pentesting real + reporting |
| **Evaluaciones** | 5h | Quizzes, prácticas finales |
| **Total** | **150h** | |

---

## 📧 Soporte y Contacto

**ABACOM™ Capacitación y Servicios Informáticos**

- 📍 Calle Máximo Agustín Rodríguez 16-40 y, Loja, Ecuador
- 📞 Información y matrículas
- 🌐 [www.abacom.ec](https://www.abacom.ec)
- 📧 contacto@abacom.ec

---

## 📄 Licencia

Este material está bajo **licencia educativa de ABACOM™**. Uso únicamente con fines educativos y de capacitación profesional.

Para distribución, contacta con ABACOM.

---

## 🙏 Créditos

Desarrollado por el equipo de capacitación de ABACOM™, acreditado por el Ministerio de Trabajo de Ecuador.

**Acreditación**: SETEC-CAL-2019-0183

Modernización curricular 2026 con énfasis en IA, automatización y defensas contemporáneas.

---

**"Capacitación de calidad para el desarrollo tecnológico de la región sur del Ecuador"** 🇪🇨

