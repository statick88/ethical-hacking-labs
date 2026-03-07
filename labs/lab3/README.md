# Lab 3: Web Security (OWASP WebGoat)

## Overview

Lab 3 teaches web security principles and common web vulnerabilities using OWASP WebGoat. Students will learn about SQL injection, cross-site scripting (XSS), authentication flaws, and other OWASP Top 10 vulnerabilities through interactive exercises.

## Requirements

- Docker Engine 24.0+
- Docker Compose 2.0+
- 3GB RAM minimum (4GB recommended)
- 5GB free disk space
- Web browser (Chrome, Firefox, or Edge)

## Architecture

```
┌─────────────────────────────────────────┐
│        Docker Network (172.18.3.0/24)   │
├─────────────────────────────────────────┤
│  WebGoat (172.18.3.10)                  │
│  ├── Java Web Application               │
│  ├── OWASP Top 10 Lessons               │
│  ├── Port 8080 (Web)                    │
│  └── Port 9001 (WebWolf - Backend)      │
│                                         │
│  Firefox + Selenium (172.18.3.20)      │
│  ├── Browser Testing Environment       │
│  └── VNC Port 6900                      │
└─────────────────────────────────────────┘
```

## Quick Start

### 1. Start the Lab

```bash
cd lab3
docker-compose up -d
```

**Expected output:**
```
Creating network "lab3_lab3_network" with driver "bridge"
Creating lab3-webgoat ... done
Creating lab3-firefox ... done
```

### 2. Access WebGoat

Open your browser and navigate to:

```
http://localhost:8080/WebGoat/
```

### 3. Register and Login

- Username: `student`
- Password: `password` (choose your own)

## Learning Objectives

By the end of this lab, students will be able to:

- ✓ Identify common web vulnerabilities
- ✓ Exploit and fix SQL injection vulnerabilities
- ✓ Understand Cross-Site Scripting (XSS) attacks
- ✓ Learn authentication and session management flaws
- ✓ Implement secure coding practices
- ✓ Use web security testing tools

## Curriculum Path

WebGoat contains ~30 lessons organized by vulnerability type. Recommended order:

### Part 1: Fundamentals (Days 1-2)

1. **Getting Started**: Introduction to WebGoat
2. **General**: HTTP Basics, Cookies
3. **Authentication**: Weak Authentication, Password Storage
4. **Session Management**: Session Fixation, Session Prediction

### Part 2: Injection Attacks (Days 3-4)

5. **SQL Injection**: Introduction, Advanced Techniques
6. **NoSQL Injection**: Basic and Advanced
7. **Path Traversal**: File System Access
8. **Command Injection**: OS Command Execution

### Part 3: XSS and Client-Side (Days 5-6)

9. **Cross-Site Scripting (XSS)**: Stored, Reflected, DOM-based
10. **CSRF**: Cross-Site Request Forgery
11. **Insecure Deserialization**: Java Serialization Attacks
12. **Broken Access Control**: Authorization Flaws

### Part 4: Advanced Topics (Days 7-8)

13. **XML Attacks**: XXE, XPath Injection
14. **Cryptography**: Weak Encryption
15. **AJAX Security**: Client-Side Validation
16. **Missing Functional ACL**: Authorization Issues

## Exercises

### Exercise 1: SQL Injection

**Objective**: Learn and exploit SQL injection vulnerabilities

1. Navigate to: **Injection → SQL Injection**
2. Complete lessons 1-5 on SQL injection
3. Exploit the vulnerable authentication form
4. Modify database queries to bypass authentication

**Key Concepts:**
- `' OR '1'='1` - Comment operator bypass
- `UNION` - Data extraction
- `DROP TABLE` - Data destruction

### Exercise 2: Cross-Site Scripting (XSS)

**Objective**: Perform XSS attacks and learn impact

1. Navigate to: **Client-side → Cross-Site Scripting**
2. Complete lessons on Stored, Reflected, and DOM XSS
3. Inject JavaScript payloads
4. Demonstrate cookie stealing and session hijacking

**Key Payloads:**
```javascript
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
```

### Exercise 3: Authentication Flaws

**Objective**: Bypass weak authentication mechanisms

1. Navigate to: **Authentication**
2. Exploit weak password reset mechanisms
3. Perform brute force attacks
4. Break authentication schemes

### Exercise 4: Access Control

**Objective**: Bypass authorization checks

1. Navigate to: **Access Control**
2. Modify user IDs in URLs
3. Access admin panels without authorization
4. Escalate privileges

## Tools and Browser Extensions

### Recommended Browser Extensions

1. **Burp Suite Community** (or **ZAP**)
   - Intercept and modify HTTP requests
   - Test parameters and headers
   - Spider and scan applications

2. **OWASP ZAP** (Free Alternative)
   - Proxy-based testing
   - Automated scanning
   - Payload injection

3. **Cookie Editor**
   - View and modify cookies
   - Session manipulation

### Command Line Tools (from Host)

```bash
# Test with curl
curl http://localhost:8080/WebGoat/

# Use sqlmap for SQL injection
sqlmap -u "http://localhost:8080/WebGoat/...vulnerable...endpoint" --dbs

# Use ffuf for fuzzing
ffuf -u "http://localhost:8080/WebGoat/FUZZ" -w wordlist.txt
```

## WebGoat Configuration

### Access WebWolf (Collaboration Tool)

WebWolf runs on port 9001 and provides:
- Email simulation for testing
- File upload testing
- SSRF target
- XXE testing environment

```
http://localhost:9001/
```

### Disable Hints (for harder challenges)

Edit user preferences in WebGoat to disable hints and increase difficulty.

## Troubleshooting

### WebGoat not starting

```bash
# Check logs
docker-compose logs -f webgoat

# Ensure Java is running
docker-compose exec webgoat ps aux | grep java
```

### Port 8080 already in use

Option 1: Stop conflicting services
```bash
lsof -i :8080
kill -9 <PID>
```

Option 2: Map to different port in docker-compose.yml
```yaml
ports:
  - "8888:8080"  # Changed to 8888
```

### Browser can't connect to WebGoat

```bash
# Verify container is running
docker-compose ps

# Check network connectivity
docker-compose exec firefox curl -v http://webgoat:8080/WebGoat/

# Check firewall
sudo firewall-cmd --list-ports
```

### Login loop / Session issues

```bash
# Clear browser cookies
# In Firefox: Preferences → Privacy → Clear Cookies

# Or clear via container
docker-compose restart webgoat
```

### Low memory or slow performance

Reduce memory limits or close other applications:

```bash
# Monitor resource usage
docker stats

# Reduce Firefox memory
# Edit docker-compose.yml: memory: 512m
docker-compose down
docker-compose up -d
```

## Cleanup

### Stop containers (preserves data)

```bash
docker-compose stop
```

### Remove containers (preserves volumes)

```bash
docker-compose down
```

### Complete cleanup (removes everything)

```bash
docker-compose down -v
```

### Reset WebGoat progress

```bash
docker-compose down -v
docker-compose up -d
```

## Importing Certificates (for proxy testing)

If using Burp Suite or OWASP ZAP:

1. Export certificate from proxy tool
2. Import into Firefox:
   - Preferences → Privacy & Security → Certificates
   - Import certificate
   - Trust for identifying websites

## Resources

- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)

## Success Criteria

You have completed Lab 3 when you can:

- ✓ Perform SQL injection attacks and fix vulnerabilities
- ✓ Execute XSS payloads and explain impact
- ✓ Bypass weak authentication mechanisms
- ✓ Identify and exploit broken access controls
- ✓ Document at least 10 vulnerabilities found
- ✓ Propose fixes for each vulnerability

## Next Steps

After completing Lab 3, you should:

1. Document all exploits with proofs of concept
2. Practice with PortSwigger Web Security Academy
3. Move to Lab 4: Active Directory & BloodHound
4. Begin network penetration testing phase

---

**Lab Created**: March 2026  
**Last Updated**: March 2026  
**Status**: Ready for Student Use
