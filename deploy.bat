@echo off
REM KisanSathi Deployment Script for Windows
REM This script automates the deployment process

setlocal enabledelayedexpansion

REM Colors (using ANSI escape codes)
set "RESET=[0m"
set "RED=[0;31m"
set "GREEN=[0;32m"
set "YELLOW=[1;33m"
set "BLUE=[0;34m"

REM Functions
:print_header
echo.
echo %BLUE%========================================%RESET%
echo %BLUE%%~1%RESET%
echo %BLUE%========================================%RESET%
echo.
exit /b

:print_success
echo %GREEN%[OK] %~1%RESET%
exit /b

:print_error
echo %RED%[ERROR] %~1%RESET%
exit /b

:print_warning
echo %YELLOW%[WARNING] %~1%RESET%
exit /b

:print_info
echo %BLUE%[INFO] %~1%RESET%
exit /b

REM Check prerequisites
:check_prerequisites
call :print_header "Checking Prerequisites"

where docker >nul 2>nul
if %errorlevel% neq 0 (
    call :print_error "Docker is not installed"
    exit /b 1
)
for /f "tokens=*" %%i in ('docker --version') do set DOCKER_VERSION=%%i
call :print_success "Docker is installed: %DOCKER_VERSION%"

where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    call :print_error "Docker Compose is not installed"
    exit /b 1
)
for /f "tokens=*" %%i in ('docker-compose --version') do set COMPOSE_VERSION=%%i
call :print_success "Docker Compose is installed: %COMPOSE_VERSION%"

where git >nul 2>nul
if %errorlevel% neq 0 (
    call :print_error "Git is not installed"
    exit /b 1
)
for /f "tokens=*" %%i in ('git --version') do set GIT_VERSION=%%i
call :print_success "Git is installed: %GIT_VERSION%"

exit /b 0

REM Validate environment
:validate_environment
call :print_header "Validating Environment"

if not exist ".env" (
    call :print_warning ".env file not found"
    call :print_info "Creating .env file from template..."
    
    (
        echo # Backend Configuration
        echo GEMINI_API_KEY=your_gemini_api_key_here
        echo WEATHERAPI_KEY=your_openweathermap_api_key_here
        echo FLASK_ENV=production
        echo FLASK_DEBUG=False
        echo SECRET_KEY=kisansathi_secret_key_2024
        echo.
        echo # MongoDB Configuration
        echo MONGODB_URI=mongodb://admin:password@mongodb:27017/kisansathi?authSource=admin
        echo MONGODB_DATABASE=kisansathi
        echo.
        echo # Redis Configuration
        echo REDIS_HOST=redis
        echo REDIS_PORT=6379
        echo REDIS_DB=0
        echo REDIS_ENABLED=True
        echo.
        echo # Cloudinary Configuration (Optional)
        echo CLOUDINARY_CLOUD_NAME=your_cloud_name
        echo CLOUDINARY_API_KEY=your_api_key
        echo CLOUDINARY_API_SECRET=your_api_secret
    ) > .env
    
    call :print_warning "Please update .env file with your API keys"
    call :print_info "Edit .env and run the script again"
    exit /b 1
)

call :print_success ".env file found"
exit /b 0

REM Build Docker images
:build_images
call :print_header "Building Docker Images"

call :print_info "Building backend image..."
docker-compose build backend
if %errorlevel% neq 0 (
    call :print_error "Failed to build backend image"
    exit /b 1
)
call :print_success "Backend image built"

call :print_info "Building frontend image..."
docker-compose build frontend
if %errorlevel% neq 0 (
    call :print_error "Failed to build frontend image"
    exit /b 1
)
call :print_success "Frontend image built"

call :print_info "Building other services..."
docker-compose build
if %errorlevel% neq 0 (
    call :print_error "Failed to build images"
    exit /b 1
)
call :print_success "All images built successfully"
exit /b 0

REM Start services
:start_services
call :print_header "Starting Services"

call :print_info "Starting all services..."
docker-compose up -d
if %errorlevel% neq 0 (
    call :print_error "Failed to start services"
    exit /b 1
)

call :print_info "Waiting for services to be healthy..."
timeout /t 10 /nobreak

call :print_success "Services started"
exit /b 0

REM Display service status
:show_status
call :print_header "Service Status"
docker-compose ps
exit /b 0

REM Display access information
:show_access_info
call :print_header "Access Information"

echo.
echo %GREEN%Application URLs:%RESET%
echo   Frontend:        %BLUE%http://localhost:3000%RESET%
echo   Backend API:     %BLUE%http://localhost:5000%RESET%
echo   Nginx Proxy:     %BLUE%http://localhost:80%RESET%
echo   Flower (Celery): %BLUE%http://localhost:5555%RESET%

echo.
echo %GREEN%Database Access:%RESET%
echo   MongoDB:  mongodb://admin:password@localhost:27017
echo   Redis:    redis://localhost:6379

echo.
echo %GREEN%Useful Commands:%RESET%
echo   View logs:       %BLUE%docker-compose logs -f%RESET%
echo   Stop services:   %BLUE%docker-compose down%RESET%
echo   Restart service: %BLUE%docker-compose restart ^<service^>%RESET%
echo   Execute command: %BLUE%docker-compose exec ^<service^> ^<command^>%RESET%

echo.
exit /b 0

REM Main deployment flow
:main
call :print_header "KisanSathi Deployment Script"

set "COMMAND=%~1"
if "%COMMAND%"=="" set "COMMAND=deploy"

if "%COMMAND%"=="deploy" (
    call :check_prerequisites
    if %errorlevel% neq 0 exit /b 1
    
    call :validate_environment
    if %errorlevel% neq 0 exit /b 1
    
    call :build_images
    if %errorlevel% neq 0 exit /b 1
    
    call :start_services
    if %errorlevel% neq 0 exit /b 1
    
    call :show_status
    call :show_access_info
    call :print_success "Deployment completed successfully!"
    
) else if "%COMMAND%"=="start" (
    call :print_info "Starting services..."
    docker-compose up -d
    call :show_status
    call :show_access_info
    
) else if "%COMMAND%"=="stop" (
    call :print_info "Stopping services..."
    docker-compose down
    call :print_success "Services stopped"
    
) else if "%COMMAND%"=="restart" (
    call :print_info "Restarting services..."
    docker-compose restart
    call :show_status
    
) else if "%COMMAND%"=="logs" (
    docker-compose logs -f --tail=100
    
) else if "%COMMAND%"=="status" (
    call :show_status
    call :show_access_info
    
) else if "%COMMAND%"=="clean" (
    call :print_warning "This will remove all containers and volumes"
    set /p confirm="Are you sure? (yes/no): "
    if "!confirm!"=="yes" (
        docker-compose down -v
        call :print_success "Cleanup completed"
    )
    
) else if "%COMMAND%"=="backup" (
    call :print_header "Backing Up Data"
    
    if not exist "backups" mkdir backups
    
    call :print_info "Backing up MongoDB..."
    docker-compose exec -T mongodb mongodump --uri="mongodb://admin:password@localhost:27017/kisansathi?authSource=admin" --out=/backup
    docker cp kisansathi-mongodb:/backup backups/mongodb_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    call :print_success "MongoDB backup completed"
    
    call :print_info "Backing up Redis..."
    docker-compose exec -T redis redis-cli BGSAVE
    docker cp kisansathi-redis:/data/dump.rdb backups/redis_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.rdb
    call :print_success "Redis backup completed"
    
) else (
    echo Usage: %0 [deploy^|start^|stop^|restart^|logs^|status^|clean^|backup]
    echo.
    echo Commands:
    echo   deploy   - Full deployment (build and start)
    echo   start    - Start services
    echo   stop     - Stop services
    echo   restart  - Restart services
    echo   logs     - View logs
    echo   status   - Show service status
    echo   clean    - Remove all containers and volumes
    echo   backup   - Backup MongoDB and Redis
    exit /b 1
)

exit /b 0

REM Run main function
call :main %*
