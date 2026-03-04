# Archivo del Proyecto

## Versión 1.0

### Información General

- **Fecha de Llegada**: [Fecha]
- **Versión**: 1.0
- **Estado**: Finalizado

### Contenido del Archivo

1. **Código Fuente**: Repositorio git completo
2. **Imágenes Docker**: Copias de las imágenes usadas
3. **Documentación**: Todos los documentos en formato Markdown
4. **Resultados**: Datos y resultados de pruebas

### Estructura del Archivo

```
archivo/
├── version_1.0/
│   ├── codigo_fuente/
│   ├── imagenes_docker/
│   ├── documentacion/
│   ├── resultados/
│   └── informe_final.md
└── version_1.1/
```

### Proceso de Archivado

1. Generar una copia del repositorio:
   ```bash
   git clone <repository-url> ethical-hacking-labs_1.0
   cd ethical-hacking-labs_1.0
   ```

2. Crear tags de version:
   ```bash
   git tag -a v1.0 -m "Version 1.0"
   git push origin v1.0
   ```

3. Exportar imágenes Docker:
   ```bash
   for i in {1..8}; do
       docker save kalilinux/kali-rolling:latest > unit${i}_kali_rolling.tar
   done
   ```

4. Comprimir contenido:
   ```bash
   zip -r ethical-hacking-labs_1.0.zip ethical-hacking-labs_1.0
   ```

### Acceso al Archivo

El archivo está disponible en:
- [GitHub Releases](https://github.com/<usuario>/ethical-hacking-labs/releases)
- [Google Drive](https://drive.google.com/drive/folders/<id>)
- [SFTP](sftp://<servidor>/archivos/ethical-hacking-labs)

### Requisitos para Restauración

1. Docker Engine instalado
2. Docker Compose instalado
3. Acceso a Internet para descargar imágenes

### Instrucciones de Restauración

1. Descargar y extraer el archivo:
   ```bash
   wget <url-archivo>.zip
   unzip <archivo>.zip
   ```

2. Cargar imágenes Docker:
   ```bash
   for i in {1..8}; do
       docker load -i unit${i}_kali_rolling.tar
   done
   ```

3. Construir y ejecutar contenedores:
   ```bash
   cd docker-labs/unit1
   docker-compose up -d
   ```

## Historial de Versiones

| Versión | Fecha | Cambios |
|---------|-------|----------|
| 1.0     | [Fecha] | Versión inicial completa |
| 1.1     | [Fecha] | Optimización de contenedores y seguridad |

## Notas Finales

Este archivo es una copia completa del proyecto y puede ser restaurado en cualquier entorno compatible con Docker.
