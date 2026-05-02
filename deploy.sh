#!/bin/bash

# KisanSathi Deployment Script
# This script automates the deployment process

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker is installed: $(docker --version)"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    print_success "Docker Compose is installed: $(docker-compose --version)"
    
    # Check Git
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed"
        exit 1
    fi
    print_success "Git is installed: $(git --version)"
}

# Validate environment
validate_environment() {
    print_header "Validating Environment"
    
    if [ ! -f ".env" ]; then
        print_warning ".env file not found"
        print_info "Creating .env file from template..."
        
        cat > .env << 'EOF'
# Backend Configuration
GEMINI_API_KEY=your_gemini_api_key_here
WEATHERAPI_KEY=your_openweathermap_api_key_here
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=kisansathi_secret_key_2024

# MongoDB Configuration
MONGODB_URI=mongodb://admin:password@mongodb:27017/kisansathi?authSource=admin
MONGODB_DATABASE=kisansathi

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_ENABLED=True

# Cloudinary Configuration (Optional)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
EOF
        
        print_warning "Please update .env file with your API keys"
        print_info "Edit .env and run the script again"
        exit 1
    fi
    
    print_success ".env file found"
    
    # Check for required API keys
    if grep -q "your_gemini_api_key_here" .env; then
        print_error "GEMINI_API_KEY not configured in .env"
        exit 1
    fi
    
    if grep -q "your_openweathermap_api_key_here" .env; then
        print_error "WEATHERAPI_KEY not configured in .env"
        exit 1
    fi
    
    print_success "API keys configured"
}

# Build Docker images
build_images() {
    print_header "Building Docker Images"
    
    print_info "Building backend image..."
    docker-compose build backend
    print_success "Backend image built"
    
    print_info "Building frontend image..."
    docker-compose build frontend
    print_success "Frontend image built"
    
    print_info "Building other services..."
    docker-compose build
    print_success "All images built successfully"
}

# Start services
start_services() {
    print_header "Starting Services"
    
    print_info "Starting all services..."
    docker-compose up -d
    
    print_info "Waiting for services to be healthy..."
    sleep 10
    
    # Check MongoDB
    if docker-compose exec -T mongodb mongosh -u admin -p password --eval "db.adminCommand('ping')" &> /dev/null; then
        print_success "MongoDB is running"
    else
        print_error "MongoDB failed to start"
        exit 1
    fi
    
    # Check Redis
    if docker-compose exec -T redis redis-cli ping &> /dev/null; then
        print_success "Redis is running"
    else
        print_error "Redis failed to start"
        exit 1
    fi
    
    # Check Backend
    if curl -s http://localhost:5000/api/health &> /dev/null; then
        print_success "Backend is running"
    else
        print_warning "Backend is starting (may take a moment)"
    fi
    
    # Check Frontend
    if curl -s http://localhost:3000 &> /dev/null; then
        print_success "Frontend is running"
    else
        print_warning "Frontend is starting (may take a moment)"
    fi
}

# Display service status
show_status() {
    print_header "Service Status"
    docker-compose ps
}

# Display access information
show_access_info() {
    print_header "Access Information"
    
    echo ""
    echo -e "${GREEN}Application URLs:${NC}"
    echo -e "  Frontend:        ${BLUE}http://localhost:3000${NC}"
    echo -e "  Backend API:     ${BLUE}http://localhost:5000${NC}"
    echo -e "  Nginx Proxy:     ${BLUE}http://localhost:80${NC}"
    echo -e "  Flower (Celery): ${BLUE}http://localhost:5555${NC}"
    
    echo ""
    echo -e "${GREEN}Database Access:${NC}"
    echo -e "  MongoDB:  mongodb://admin:password@localhost:27017"
    echo -e "  Redis:    redis://localhost:6379"
    
    echo ""
    echo -e "${GREEN}Useful Commands:${NC}"
    echo -e "  View logs:       ${BLUE}docker-compose logs -f${NC}"
    echo -e "  Stop services:   ${BLUE}docker-compose down${NC}"
    echo -e "  Restart service: ${BLUE}docker-compose restart <service>${NC}"
    echo -e "  Execute command: ${BLUE}docker-compose exec <service> <command>${NC}"
    
    echo ""
}

# Main deployment flow
main() {
    print_header "KisanSathi Deployment Script"
    
    # Parse command line arguments
    COMMAND=${1:-deploy}
    
    case $COMMAND in
        deploy)
            check_prerequisites
            validate_environment
            build_images
            start_services
            show_status
            show_access_info
            print_success "Deployment completed successfully!"
            ;;
        
        start)
            print_info "Starting services..."
            docker-compose up -d
            show_status
            show_access_info
            ;;
        
        stop)
            print_info "Stopping services..."
            docker-compose down
            print_success "Services stopped"
            ;;
        
        restart)
            print_info "Restarting services..."
            docker-compose restart
            show_status
            ;;
        
        logs)
            docker-compose logs -f --tail=100
            ;;
        
        status)
            show_status
            show_access_info
            ;;
        
        clean)
            print_warning "This will remove all containers and volumes"
            read -p "Are you sure? (yes/no): " confirm
            if [ "$confirm" = "yes" ]; then
                docker-compose down -v
                print_success "Cleanup completed"
            fi
            ;;
        
        backup)
            print_header "Backing Up Data"
            mkdir -p backups
            
            print_info "Backing up MongoDB..."
            docker-compose exec -T mongodb mongodump --uri="mongodb://admin:password@localhost:27017/kisansathi?authSource=admin" --out=/backup
            docker cp kisansathi-mongodb:/backup ./backups/mongodb_$(date +%Y%m%d_%H%M%S)
            print_success "MongoDB backup completed"
            
            print_info "Backing up Redis..."
            docker-compose exec -T redis redis-cli BGSAVE
            docker cp kisansathi-redis:/data/dump.rdb ./backups/redis_$(date +%Y%m%d_%H%M%S).rdb
            print_success "Redis backup completed"
            ;;
        
        *)
            echo "Usage: $0 {deploy|start|stop|restart|logs|status|clean|backup}"
            echo ""
            echo "Commands:"
            echo "  deploy   - Full deployment (build and start)"
            echo "  start    - Start services"
            echo "  stop     - Stop services"
            echo "  restart  - Restart services"
            echo "  logs     - View logs"
            echo "  status   - Show service status"
            echo "  clean    - Remove all containers and volumes"
            echo "  backup   - Backup MongoDB and Redis"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
