#!/bin/bash
# Script para pushear a GitHub

set -e

echo "🔧 Setup para GitHub..."

# Cambiar a rama main
git branch -M main

# Agregar remote
git remote add origin https://github.com/abacom/ethical-hacking-labs.git

# Pushear a main
git push -u origin main

echo "✅ Repositorio pusheado a GitHub"
echo ""
echo "📝 Próximos pasos en GitHub:"
echo "1. Ve a Settings > Pages"
echo "2. Source: Deploy from a branch"
echo "3. Branch: main, carpeta: /root (o /docs después de build Quarto)"
echo "4. Espera a que se despliegue (2-3 minutos)"
echo "5. Tu sitio estará en: https://abacom.github.io/ethical-hacking-labs"
