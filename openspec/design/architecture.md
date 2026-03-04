# Arquitectura del Proyecto

## Visión General

El proyecto de laboratorios de hacking ético sigue una arquitectura modular y escalable, diseñada para proporcionar entornos de laboratorio aislados y fácilmente configurables usando contenedores Docker.

## Arquitectura de Contenedores

### Estructura de Contenedores

Cada laboratorio se compone de uno o más contenedores Docker, con la siguiente arquitectura básica:

```
┌─────────────────┐
│  Host Machine   │
├─────────────────┤
│ Docker Engine   │
├─────────────────┤
│  Container 1    │
│  (Kali Linux)   │
├─────────────────┤
│  Container 2    │
│  (Target App)   │
├─────────────────┤
│  Container 3    │
│  (Database)     │
└─────────────────┘
```

### Imágenes Oficiales Usadas

1. **Kali Linux**: `kalilinux/kali-rolling` - Distribución de pentesting
2. **OWASP ZAP**: `owasp/zap2docker-stable` - Analizador de vulnerabilidades web
3. **OpenVAS**: `mikesplain/openvas` - Scanner de vulnerabilidades
4. **BloodHound**: `neowulf33/bloodhound` - Analizador de Active Directory

### Redes de Contenedores

Cada laboratorio se ejecuta en una red Docker aislada:
- **Puertos expuestos**: 22 (SSH), 8080 (VNC/noVNC)
- **Rango IP**: 192.168.0.0/24 por defecto
- **Volúmenes**: Montajes para persistencia de datos

## Estructura de Directorios

```
ethical-hacking-labs/
├── README.md                  # Descripción general del proyecto
├── package.json               # Configuración de npm
├── docs/                      # Documentación general
│   ├── setup.md              # Guía de instalación
│   └── troubleshooting.md    # Solución de problemas
├── docker-labs/               # Laboratorios Docker
│   ├── unit1/
│   │   ├── Dockerfile        # Dockerfile para la imagen
│   │   ├── docker-compose.yml # Configuración de contenedores
│   │   ├── README.md         # Instrucciones específicas
│   │   └── data/             # Datos persistentes
│   └── unit8/
└── openspec/                  # Documentación SDD
    ├── initiate/             # Inicialización del proyecto
    ├── propose/              # Propuestas de cambio
    ├── spec/                 # Especificaciones
    ├── design/               # Diseño técnico
    ├── tasks/                # Tareas de implementación
    ├── apply/                # Aplicación de cambios
    ├── verify/               # Verificación
    └── archive/              # Archivado
```

## Arquitectura de Servicios

### Servicios Principales

1. **Kali Linux Container**: 
   - Proporciona entorno de pentesting
   - Acceso por SSH y VNC/noVNC
   - Contiene herramientas preinstaladas

2. **Target Applications**:
   - Aplicaciones web vulnerables para pruebas
   - Bases de datos vulnerables
   - APIs para pruebas de seguridad

3. **Security Tools**:
   - OWASP ZAP para análisis de vulnerabilidades
   - Metasploit para explotación
   - OpenVAS para escaneo

## Escalabilidad y Mantenibilidad

### Modularidad

- Cada laboratorio es independiente y autocontenido
- Componentes reutilizables entre laboratorios
- Posibilidad de agregar nuevas unidades sin afectar las existentes

### Actualización

- Imágenes Docker actualizadas automáticamente
- Herramientas instaladas desde repositorios oficiales
- Documentación versionada en git

## Seguridad y Aislamiento

### Aislamiento de Laboratorios

- Cada laboratorio se ejecuta en su propia red Docker
- Puertos expuestos en hosts son únicos por laboratorio
- Datos persistentes se almacenan en volúmenes locales

### Configuración Segura

- Usar imágenes oficiales y de fuentes confiables
- Configuración mínima de privilegios para contenedores
- Passwd predeterminados con cambios recomendados

## Despliegue y Escalado

### Despliegue Local

1. Clonar el repositorio
2. Instalar dependencias
3. Construir contenedores
4. Iniciar servicios

### Despliegue en Nube

1. Usar Docker Machine para provisionar hosts en la nube
2. Configurar docker-compose con ajustes para la nube
3. Usar herramientas de orquestación (Swarm, Kubernetes) para escalar

## Arquitectura de Datos

### Almacenamiento de Datos

- Datos de laboratorio se almacenan en volúmenes Docker
- Archivos de configuración y resultados se guardan en el host
- Bases de datos se guardan en volúmenes persistentes

### Backups

- Copias de seguridad de volúmenes Docker
- Exportación de resultados de laboratorio
- Almacenamiento de datos en repositorios git

## Conclusión

La arquitectura del proyecto se diseñó para ser:
1. **Fácil de usar**: Configuración rápida y contenedores listos para usar
2. **Modular**: Laboratorios independientes y escalables
3. **Segura**: Aislamiento y configuraciones seguras
4. **Mantenible**: Actualización automatizada y componentes reutilizables
