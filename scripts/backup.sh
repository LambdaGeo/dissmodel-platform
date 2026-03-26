#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# DISSMODEL PLATFORM - Backup Script
# ═══════════════════════════════════════════════════════════════

set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_FILE="${BACKUP_DIR}/backup-${TIMESTAMP}.tar.gz"

echo "💾 DisSModel Platform - Backup"
echo "═══════════════════════════════════════════════════════════"

# Create backup directory
mkdir -p ${BACKUP_DIR}

# Stop platform (optional, for consistency)
echo "🛑 Stopping services..."
docker compose down

# Create backup
echo "📦 Creating backup..."
tar -czvf ${BACKUP_FILE} \
    data/inputs \
    data/outputs \
    data/storage \
    data/redis \
    .env

# Restart platform
echo "🚀 Restarting services..."
docker compose up -d

echo ""
echo "✅ Backup created: ${BACKUP_FILE}"
echo "═══════════════════════════════════════════════════════════"