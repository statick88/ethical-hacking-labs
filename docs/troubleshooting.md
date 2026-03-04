# Troubleshooting

This guide helps you troubleshoot common issues with the ethical hacking labs.

## Docker Issues

### Docker Desktop Won't Start

#### macOS
1. Check if virtualization is enabled (Apple Silicon: System Settings → Privacy & Security → Virtualization)
2. Restart Docker Desktop
3. Restart your computer

#### Linux
1. Check Docker daemon status:
   ```bash
   sudo systemctl status docker
   ```

2. Start Docker daemon:
   ```bash
   sudo systemctl start docker
   ```

3. Enable Docker on boot:
   ```bash
   sudo systemctl enable docker
   ```

### Containers Won't Start

1. Check Docker engine is running:
   ```bash
   docker info
   ```

2. Check container logs:
   ```bash
   cd docker-labs/unit1
   docker-compose logs -f
   ```

3. Verify port availability:
   ```bash
   # Check if port 8080 is in use
   lsof -ti :8080  # macOS
   ss -tuln | grep 8080  # Linux
   ```

### Port Already in Use

1. Stop the process using the port:
   ```bash
   kill -9 $(lsof -ti :8080)  # macOS
   ```

2. Or modify the `docker-compose.yml` to use a different port

## Performance Issues

### Containers Are Running Slow

1. Allocate more resources to Docker:
   - macOS: Docker Desktop → Settings → Resources → Advanced
   - Linux: Edit `/etc/docker/daemon.json`

2. Close unused applications

3. Clean up Docker system:
   ```bash
   docker system prune -f
   ```

### High CPU Usage

1. Check which container is using resources:
   ```bash
   docker stats
   ```

2. Restart problematic containers:
   ```bash
   cd docker-labs/unit1
   docker-compose restart <container-name>
   ```

## Network Issues

### Cannot Access Web Interfaces

1. Verify containers are running:
   ```bash
   docker-compose ps
   ```

2. Check if the service is listening on the correct port

3. Try accessing using `http://127.0.0.1:8080` instead of `localhost`

### DNS Resolution Issues

1. Check Docker DNS settings
2. Restart the Docker daemon
3. Try using Google DNS in Docker settings

## Data Persistence

### Volumes Not Mounting

1. Check the `volumes` section in `docker-compose.yml`
2. Verify the host directory exists
3. Check permissions on the host directory:
   ```bash
   chmod -R 755 /path/to/directory
   ```

### Container Data Lost

1. Use named volumes instead of bind mounts
2. Create backups:
   ```bash
   docker run --rm --volumes-from <container-name> -v $(pwd):/backup busybox tar czf /backup/backup.tar.gz /path/to/data
   ```

## Common Commands for Troubleshooting

```bash
# List all containers (running and stopped)
docker ps -a

# Show container logs
docker logs <container-id>

# Exec into a container
docker exec -it <container-id> bash

# View Docker system events
docker events

# Check Docker daemon status
docker info

# Test Docker network connectivity
docker run --rm busybox ping google.com
```

## Getting Help

1. Check the unit's specific README.md
2. Search the [GitHub Issues](../../issues)
3. Ask your instructor for assistance

Include these details when reporting issues:
- Operating system
- Docker version
- Unit number
- Error messages (copy and paste)
- Steps to reproduce
