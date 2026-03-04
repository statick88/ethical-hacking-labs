# Ethical Hacking Labs - Máster UCM Ciberseguridad

Comprehensive ethical hacking labs for the **Máster Oficial en Ciberseguridad: Seguridad Defensiva y Ofensiva** at UCM.

## Overview

This repository contains 8 units of hands-on ethical hacking labs designed to provide practical experience in modern cybersecurity techniques. Each lab is containerized with Docker for easy setup and isolation.

## Course Units

1. **Unit 1 - Fundamentos y Reconocimiento Agéntico**
2. **Unit 2 - Vulnerabilidades en IA y Modelos de Lenguaje**
3. **Unit 3 - Explotación Web y APIs 2026**
4. **Unit 4 - Hacking de Identidad y AD Moderno**
5. **Unit 5 - Pentesting Autónomo y Red Teaming Agéntico**
6. **Unit 6 - Evasión de Defensas**
7. **Unit 7 - Ciberseguridad Industrial**
8. **Unit 8 - Post-Explotación, Reporte y Ética**

## Getting Started

### Prerequisites

- Docker Desktop (macOS) or Docker Engine (Linux)
- Git
- At least 16GB RAM (8GB minimum, 16GB recommended)
- 20GB free disk space

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ethical-hacking-labs
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build and start a lab unit:
   ```bash
   # Example for Unit 1
   cd docker-labs/unit1
   docker-compose up -d
   ```

### Accessing Labs

- Web-based tools: `http://localhost:8080`
- SSH: Use the instructions in each unit's README

## Documentation

- **Setup Guide**: [docs/setup.md](docs/setup.md)
- **Troubleshooting**: [docs/troubleshooting.md](docs/troubleshooting.md)
- **SDD Process**: [openspec/](openspec/) - Spec-Driven Development documentation

## SDD Structure

This project follows the Spec-Driven Development methodology with the following phases:

- **initiate**: Project initialization and requirements gathering
- **propose**: Change proposals and scope definition
- **spec**: Detailed specifications and acceptance criteria
- **design**: Technical architecture and implementation design
- **tasks**: Task breakdown and implementation checklist
- **apply**: Implementation and code changes
- **verify**: Verification and testing
- **archive**: Documentation archiving and version control

## License

ISC
