#!/bin/bash

# Build script for Cerebras Chat Interface Docker image
# Supports both AMD64 and ARM64 architectures

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
PLATFORM="linux/amd64"
TAG="latest"
DOCKERFILE="Dockerfile"
PUSH=false

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

# Function to show usage
show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Build Docker image for Cerebras Chat Interface

OPTIONS:
    -p, --platform PLATFORM    Target platform (default: linux/amd64)
                              Options: linux/amd64, linux/arm64, linux/arm64/v8
    -t, --tag TAG             Image tag (default: latest)
    -a, --arm                 Build for ARM64 (shortcut for -p linux/arm64)
    -m, --multi               Build multi-platform image (amd64 and arm64)
    --push                    Push image to registry (requires login)
    -h, --help                Show this help message

EXAMPLES:
    # Build for AMD64 (default)
    $0

    # Build for ARM64 (Jetson, Raspberry Pi)
    $0 --arm

    # Build multi-platform image
    $0 --multi

    # Build and tag as v1.0
    $0 -t v1.0

    # Build for ARM64 and push to registry
    $0 --arm --push -t v1.0

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--platform)
            PLATFORM="$2"
            shift 2
            ;;
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        -a|--arm)
            PLATFORM="linux/arm64"
            DOCKERFILE="Dockerfile.arm64"
            shift
            ;;
        -m|--multi)
            PLATFORM="linux/amd64,linux/arm64"
            shift
            ;;
        --push)
            PUSH=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Detect architecture if not specified
if [[ "$PLATFORM" == "linux/amd64" ]]; then
    ARCH=$(uname -m)
    if [[ "$ARCH" == "aarch64" ]] || [[ "$ARCH" == "arm64" ]]; then
        print_warning "Detected ARM64 architecture, switching to ARM64 build"
        PLATFORM="linux/arm64"
        DOCKERFILE="Dockerfile.arm64"
    fi
fi

# Image name
IMAGE_NAME="cerebras-chat-interface"
FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

print_info "Building Docker image..."
print_info "Platform: $PLATFORM"
print_info "Dockerfile: $DOCKERFILE"
print_info "Tag: $TAG"
print_info "Image: $FULL_IMAGE_NAME"

# Change to project root directory
cd "$(dirname "$0")/.."

# Check if Dockerfile exists
if [[ ! -f "docker/$DOCKERFILE" ]]; then
    print_error "Dockerfile not found: docker/$DOCKERFILE"
    exit 1
fi

# Build the image
if [[ "$PLATFORM" == *","* ]]; then
    # Multi-platform build
    print_info "Building multi-platform image..."
    
    if [[ "$PUSH" == true ]]; then
        docker buildx build \
            --platform "$PLATFORM" \
            --file "docker/$DOCKERFILE" \
            --tag "$FULL_IMAGE_NAME" \
            --push \
            .
    else
        docker buildx build \
            --platform "$PLATFORM" \
            --file "docker/$DOCKERFILE" \
            --tag "$FULL_IMAGE_NAME" \
            --load \
            .
    fi
else
    # Single platform build
    print_info "Building for platform: $PLATFORM"
    
    docker build \
        --platform "$PLATFORM" \
        --file "docker/$DOCKERFILE" \
        --tag "$FULL_IMAGE_NAME" \
        .
    
    if [[ "$PUSH" == true ]]; then
        print_info "Pushing image to registry..."
        docker push "$FULL_IMAGE_NAME"
    fi
fi

# Check if build was successful
if [[ $? -eq 0 ]]; then
    print_info "Build completed successfully!"
    print_info "Image: $FULL_IMAGE_NAME"
    print_info ""
    print_info "To run the container:"
    echo "  cd docker"
    echo "  docker-compose up -d"
    print_info ""
    print_info "Or run directly:"
    echo "  docker run -d -p 5000:5000 --env-file docker/.env $FULL_IMAGE_NAME"
else
    print_error "Build failed!"
    exit 1
fi

