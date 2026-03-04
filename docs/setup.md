# Setup Guide

This guide explains how to set up the ethical hacking labs on your local machine.

## Prerequisites

### Docker Installation

#### macOS
1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
2. Open the DMG file and drag Docker to Applications
3. Open Docker Desktop and follow the installation instructions
4. Verify installation:
   ```bash
   docker --version
   docker-compose --version
   ```

#### Linux (Ubuntu/Debian)
1. Update packages:
   ```bash
   sudo apt update
   ```

2. Install Docker:
   ```bash
   sudo apt install -y docker.io docker-compose
   ```

3. Add user to docker group (to run without sudo):
   ```bash
   sudo usermod -aG docker $USER
   ```

4. Log out and log back in
5. Verify installation:
   ```bash
   docker --version
   docker-compose --version
   ```

## Repository Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ethical-hacking-labs
   ```

2. Install npm dependencies:
   ```bash
   npm install
   ```

## Running a Lab

### Single Unit Setup

1. Navigate to the unit directory:
   ```bash
   cd docker-labs/unit1
   ```

2. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

3. Check container status:
   ```bash
   docker-compose ps
   ```

4. Access the lab using the instructions in the unit's README.md

### Stopping a Lab

```bash
cd docker-labs/unit1
docker-compose down
```

### Cleaning Up

```bash
cd docker-labs/unit1
docker-compose down -v  # Remove volumes
```

## System Requirements

- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 20GB free disk space
- **CPU**: 4 cores minimum

## Performance Optimization

1. Allocate more resources to Docker:
   - macOS: Docker Desktop → Settings → Resources → Advanced
   - Linux: Configure Docker daemon settings

2. Clean up unused containers and images:
   ```bash
   docker system prune
   ```

## Next Steps

Once you have Docker configured, start with **Unit 1 - Fundamentos y Reconocimiento Agéntico**.
