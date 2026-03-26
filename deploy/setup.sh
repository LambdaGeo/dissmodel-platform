#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# DISSMODEL PLATFORM - Setup Script
# ═══════════════════════════════════════════════════════════════

set -e

echo "🚀 DisSModel Platform - Setup"
echo "═══════════════════════════════════════════════════════════"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose found"

# Create .env if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env created. Please review and adjust values."
else
    echo "✅ .env already exists"
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p data/inputs data/outputs data/storage data/redis
mkdir -p workspace examples docs

# Set permissions
echo "🔐 Setting permissions..."
chmod 755 data/inputs data/outputs data/storage data/redis workspace

# Build images
echo "🏗️  Building Docker images..."
docker compose build

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ Setup complete!"
echo ""
echo "📌 Next steps:"
echo "   1. Review .env file and adjust credentials"
echo "   2. Run: docker compose up -d"
echo "   3. Access JupyterLab: http://localhost:8888"
echo "   4. Access API Docs:   http://localhost:8000/docs"
echo "   5. Access MinIO:      http://localhost:9001"
echo ""
echo "═══════════════════════════════════════════════════════════"