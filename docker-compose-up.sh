#!/bin/bash

# KisanSathi Docker Compose Startup Script

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         KisanSathi - Docker Compose Startup                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo ""
echo "📋 Checking prerequisites..."
echo "   ✅ Docker: $(docker --version)"
echo "   ✅ Docker Compose: $(docker-compose --version)"

echo ""
echo "🔨 Building images..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ All services started successfully!"
echo ""
echo "📍 Access points:"
echo "   • Backend:  http://localhost:5000"
echo "   • Frontend: http://localhost:3000"
echo "   • Nginx:    http://localhost:80"
echo "   • MongoDB:  localhost:27017"
echo "   • Redis:    localhost:6379"
echo ""
echo "📝 Useful commands:"
echo "   • View logs:     docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Remove data:   docker-compose down -v"
echo ""
echo "🎉 Ready to go!"
