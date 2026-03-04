# Especificaciones Funcionales

## Visión General

El sistema de laboratorios de hacking ético es una plataforma educativa diseñada para proporcionar experiencia práctica en técnicas de ciberseguridad. Los laboratorios se ejecutan en contenedores Docker para una fácil configuración y aislamiento.

## Alcance Funcional

### 1. Laboratorios Docker

#### 1.1. Estructura de Laboratorios

Cada laboratorio está estructurado como:

```
docker-labs/
└── unitX/
    ├── Dockerfile        # Imagen Docker personalizada
    ├── docker-compose.yml # Configuración de servicios
    ├── README.md         # Instrucciones del laboratorio
    └── data/             # Volumen para persistencia de datos
```

#### 1.2. Servicios Principales

**Kali Linux Container**
- **Descripción**: Entorno de pentesting con herramientas preinstaladas
- **Ports**: SSH (22), VNC/noVNC (8080)
- **Configuración**: 
  - Usuario: root
  - Password: toor
  - Timezone: Europe/Madrid

**Red Docker**
- **Subred**: 192.168.0.0/24
- **Nombre**: lab-network
- **Modo**: bridge

#### 1.3. Herramientas Preinstaladas

| Unidad | Herramientas Principales |
|-------|--------------------------|
| 1     | Nmap, Wireshark, Recon-ng, Sublist3r, Dirb |
| 2     | OpenAI API, Python ML libraries |
| 3     | SQLMap, OWASP ZAP, Burp Suite, XSSer |
| 4     | Impacket, BloodHound, CrackMapExec, PowerView |
| 5     | OpenVAS, Metasploit, Wfuzz, AI Scanner |
| 6     | Veil-Evasion, Meterpreter, Covenant, PowerShell Empire |
| 7     | Modbus Tools, DNP3 Tools, Wireshark |
| 8     | Mimikatz, PowerSploit, BloodHound |

### 2. Interfaz de Usuario

#### 2.1. Acceso SSH

```bash
ssh root@localhost -p 222X
Password: toor
```

#### 2.2. Acceso VNC/noVNC

```
URL: http://localhost:808X
Password: toor
```

### 3. Documentación

#### 3.1. Documentación General

- **README.md**: Descripción del proyecto, objetivos, prerequisitos
- **docs/setup.md**: Guía de instalación en diferentes plataformas
- **docs/troubleshooting.md**: Solución de problemas comunes

#### 3.2. Documentación de Laboratorio

Cada laboratorio incluye:

1. **Objetivos**: Que aprenderá el estudiante
2. **Herramientas**: Lista de herramientas a usar
3. **Setup**: Instrucciones para construir y ejecutar el laboratorio
4. **Ejercicios**: Pasos detallados para cada experimento
5. **Recursos**: Enlaces a documentación adicional
6. **Troubleshooting**: Solución de problemas específicos del laboratorio

### 4. Procesamiento SDD

#### 4.1. Fases del SDD

| Fase | Documentación |
|-----|---------------|
| initiate | requirements.md - Requisitos del proyecto |
| propose | project-proposal.md - Propuesta del proyecto |
| spec | functional-spec.md - Especificaciones funcionales |
| design | architecture.md - Diseño técnico |
| tasks | task-list.md - Lista de tareas |
| apply | Implementación en código |
| verify | Verificación y pruebas |
| archive | Documentación final |

## Flujo de Trabajo

### 1. Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd ethical-hacking-labs

# Instalar dependencias
npm install

# Construir y ejecutar un laboratorio
cd docker-labs/unit1
docker-compose up -d

# Acceder al laboratorio
ssh root@localhost -p 2222
```

### 2. Uso Normal

```bash
# Verificar estado de contenedores
docker-compose ps

# Ver logs de contenedores
docker-compose logs -f

# Parar contenedores
docker-compose down
```

## Restricciones

1. Los contenedores deben estar configurados para escuchar en 0.0.0.0 para acceso desde el host
2. Los puertos expuestos en el host deben ser únicos para cada laboratorio
3. Los volúmenes Docker deben estar en el directorio local del proyecto
4. Las imágenes Docker deben ser oficiales o personalizadas a partir de imágenes oficiales
