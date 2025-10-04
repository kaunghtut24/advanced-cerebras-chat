#!/bin/bash

# Run script for Cerebras Chat Interface Docker container
# Provides easy commands to start, stop, and manage the container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Function to show usage
show_usage() {
    cat << EOF
Usage: $0 [COMMAND]

Manage Cerebras Chat Interface Docker container

COMMANDS:
    start           Start the container (docker-compose up -d)
    stop            Stop the container (docker-compose down)
    restart         Restart the container
    logs            Show container logs (follow mode)
    logs-tail       Show last 100 lines of logs
    status          Show container status
    shell           Open shell in running container
    build           Build the Docker image
    rebuild         Rebuild and restart the container
    clean           Stop and remove all containers, volumes, and images
    help            Show this help message

EXAMPLES:
    # Start the container
    $0 start

    # View logs
    $0 logs

    # Restart the container
    $0 restart

    # Open shell in container
    $0 shell

    # Clean everything
    $0 clean

EOF
}

# Change to docker directory
cd "$(dirname "$0")"

# Check if .env file exists
if [[ ! -f .env ]]; then
    print_warning ".env file not found!"
    print_info "Creating .env from .env.example..."
    
    if [[ -f .env.example ]]; then
        cp .env.example .env
        print_warning "Please edit docker/.env and add your API keys before starting!"
        print_info "Required: CEREBRAS_API_KEY"
        print_info "Optional: EXA_API_KEY, BRAVE_API_KEY"
        exit 1
    else
        print_error ".env.example not found!"
        exit 1
    fi
fi

# Detect architecture
ARCH=$(uname -m)
COMPOSE_FILE="docker-compose.yml"

if [[ "$ARCH" == "aarch64" ]] || [[ "$ARCH" == "arm64" ]]; then
    print_info "Detected ARM64 architecture"
    if [[ -f "docker-compose.arm64.yml" ]]; then
        COMPOSE_FILE="docker-compose.arm64.yml"
        print_info "Using ARM64-optimized compose file"
    fi
fi

# Parse command
COMMAND=${1:-help}

case $COMMAND in
    start)
        print_step "Starting Cerebras Chat Interface..."
        docker-compose -f "$COMPOSE_FILE" up -d
        print_info "Container started successfully!"
        print_info "Access the application at: http://localhost:5000"
        print_info ""
        print_info "To view logs: $0 logs"
        ;;
    
    stop)
        print_step "Stopping Cerebras Chat Interface..."
        docker-compose -f "$COMPOSE_FILE" down
        print_info "Container stopped successfully!"
        ;;
    
    restart)
        print_step "Restarting Cerebras Chat Interface..."
        docker-compose -f "$COMPOSE_FILE" restart
        print_info "Container restarted successfully!"
        ;;
    
    logs)
        print_info "Showing logs (Ctrl+C to exit)..."
        docker-compose -f "$COMPOSE_FILE" logs -f
        ;;
    
    logs-tail)
        print_info "Showing last 100 lines of logs..."
        docker-compose -f "$COMPOSE_FILE" logs --tail=100
        ;;
    
    status)
        print_info "Container status:"
        docker-compose -f "$COMPOSE_FILE" ps
        ;;
    
    shell)
        print_info "Opening shell in container..."
        docker-compose -f "$COMPOSE_FILE" exec cerebras-chat /bin/bash
        ;;
    
    build)
        print_step "Building Docker image..."
        if [[ "$ARCH" == "aarch64" ]] || [[ "$ARCH" == "arm64" ]]; then
            ./build.sh --arm
        else
            ./build.sh
        fi
        ;;
    
    rebuild)
        print_step "Rebuilding and restarting container..."
        docker-compose -f "$COMPOSE_FILE" down
        docker-compose -f "$COMPOSE_FILE" build --no-cache
        docker-compose -f "$COMPOSE_FILE" up -d
        print_info "Container rebuilt and started successfully!"
        ;;
    
    clean)
        print_warning "This will remove all containers, volumes, and images!"
        read -p "Are you sure? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_step "Cleaning up..."
            docker-compose -f "$COMPOSE_FILE" down -v --rmi all
            print_info "Cleanup completed!"
        else
            print_info "Cleanup cancelled"
        fi
        ;;
    
    help|--help|-h)
        show_usage
        ;;
    
    *)
        print_error "Unknown command: $COMMAND"
        show_usage
        exit 1
        ;;
esac

