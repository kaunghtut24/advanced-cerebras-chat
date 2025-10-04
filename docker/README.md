# Docker Deployment Guide

## Overview

This directory contains Docker configuration files for deploying the **Cerebras Chat Interface** as a containerized application. Supports both **AMD64** and **ARM64** architectures.

---

## 📁 Files in This Directory

| File | Description |
|------|-------------|
| `Dockerfile` | Standard Dockerfile for AMD64 (x86_64) systems |
| `Dockerfile.arm64` | Optimized Dockerfile for ARM64 devices (Jetson, Raspberry Pi) |
| `docker-compose.yml` | Docker Compose configuration for AMD64 |
| `docker-compose.arm64.yml` | Docker Compose configuration for ARM64 (optimized settings) |
| `.env.example` | Example environment variables file |
| `.dockerignore` | Files to exclude from Docker build |
| `build.sh` | Build script with multi-platform support |
| `run.sh` | Management script for easy container operations |
| `README.md` | This file |

---

## 🚀 Quick Start

### **1. Prerequisites**

- **Docker** installed (20.10+)
- **Docker Compose** installed (2.0+)
- **API Keys** (Cerebras required, Exa/Brave optional)

### **2. Setup Environment**

```bash
# Navigate to docker directory
cd docker

# Copy environment example
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

**Required in `.env`:**
```env
CEREBRAS_API_KEY=your_cerebras_api_key_here
```

### **3. Start the Application**

#### **Option A: Using run.sh (Recommended)**

```bash
# Make script executable (Linux/Mac)
chmod +x run.sh

# Start the container
./run.sh start

# View logs
./run.sh logs

# Stop the container
./run.sh stop
```

#### **Option B: Using Docker Compose Directly**

```bash
# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### **4. Access the Application**

Open your browser and navigate to:
```
http://localhost:5000
```

Or from another device on the same network:
```
http://<your-ip>:5000
```

---

## 🏗️ Building the Image

### **AMD64 (x86_64) Systems**

```bash
# Using build script
./build.sh

# Or manually
docker build -f Dockerfile -t cerebras-chat-interface:latest ..
```

### **ARM64 Systems (Jetson, Raspberry Pi)**

```bash
# Using build script (auto-detects ARM64)
./build.sh --arm

# Or manually
docker build -f Dockerfile.arm64 -t cerebras-chat-interface:latest ..
```

### **Multi-Platform Build**

```bash
# Build for both AMD64 and ARM64
./build.sh --multi

# With custom tag
./build.sh --multi -t v1.0
```

---

## 🛠️ Management Commands

The `run.sh` script provides easy management:

| Command | Description |
|---------|-------------|
| `./run.sh start` | Start the container |
| `./run.sh stop` | Stop the container |
| `./run.sh restart` | Restart the container |
| `./run.sh logs` | View logs (follow mode) |
| `./run.sh logs-tail` | Show last 100 lines |
| `./run.sh status` | Show container status |
| `./run.sh shell` | Open shell in container |
| `./run.sh build` | Build the Docker image |
| `./run.sh rebuild` | Rebuild and restart |
| `./run.sh clean` | Remove everything |

---

## 📦 Volumes and Persistence

### **Persistent Data**

The following data is stored in Docker volumes:

| Volume | Purpose | Path in Container |
|--------|---------|-------------------|
| `qdrant_data` | Vector database storage | `/app/qdrant_storage` |
| `chat_history` | Chat session history | `/app/chat_history_*.json` |
| `uploads` | Uploaded documents | `/app/uploads` |

### **Backup Data**

```bash
# Backup Qdrant database
docker run --rm -v cerebras_qdrant_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/qdrant_backup.tar.gz -C /data .

# Restore Qdrant database
docker run --rm -v cerebras_qdrant_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/qdrant_backup.tar.gz -C /data
```

---

## ⚙️ Configuration

### **Environment Variables**

All configuration is done via the `.env` file:

#### **Required:**
```env
CEREBRAS_API_KEY=your_api_key_here
```

#### **Optional - Web Search:**
```env
EXA_API_KEY=your_exa_api_key
BRAVE_API_KEY=your_brave_api_key
```

#### **Optional - RAG Settings:**
```env
RAG_ENABLED=true
RAG_TOP_K=5
RAG_SCORE_THRESHOLD=0.3
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

#### **Optional - Performance:**
```env
MAX_HISTORY_LENGTH=20
RATE_LIMIT_CHAT=30 per minute
RATE_LIMIT_UPLOAD=10 per minute
```

### **Port Configuration**

To change the port, edit `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Access on port 8080 instead of 5000
```

---

## 🔍 Troubleshooting

### **Problem 1: Container Won't Start**

**Check logs:**
```bash
./run.sh logs
```

**Common causes:**
- Missing API key in `.env`
- Port 5000 already in use
- Insufficient disk space

**Solution:**
```bash
# Check if port is in use
netstat -an | grep 5000

# Change port in docker-compose.yml if needed
```

---

### **Problem 2: Can't Access from Network**

**Cause:** Firewall blocking port 5000

**Solution:**
```bash
# Linux
sudo ufw allow 5000

# Check Docker network
docker network inspect cerebras-network
```

---

### **Problem 3: Out of Memory**

**Cause:** Insufficient RAM for embeddings

**Solution for ARM devices:**

Edit `docker-compose.arm64.yml`:
```yaml
deploy:
  resources:
    limits:
      memory: 2G  # Reduce from 4G
```

Or reduce settings in `.env`:
```env
RAG_TOP_K=3
MAX_HISTORY_LENGTH=10
```

---

### **Problem 4: Slow Performance**

**For ARM devices:**

1. Use ARM64-optimized compose file:
```bash
docker-compose -f docker-compose.arm64.yml up -d
```

2. Reduce resource usage in `.env`:
```env
RAG_TOP_K=3
CHUNK_SIZE=300
MAX_HISTORY_LENGTH=10
```

---

## 🌐 Network Access

### **Access from Other Devices**

1. Find your host IP:
```bash
# Linux/Mac
hostname -I

# Windows
ipconfig
```

2. Access from browser:
```
http://<host-ip>:5000
```

### **Reverse Proxy (Nginx)**

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 🔒 Security Best Practices

### **1. Use Non-Root User**

✅ Already configured in Dockerfile:
```dockerfile
USER appuser
```

### **2. Protect API Keys**

✅ Never commit `.env` file to git  
✅ Use Docker secrets for production  
✅ Rotate API keys regularly  

### **3. Network Security**

```bash
# Only expose to localhost
ports:
  - "127.0.0.1:5000:5000"

# Use reverse proxy with SSL
# Configure firewall rules
```

---

## 📊 Resource Requirements

### **AMD64 Systems**

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 2 cores | 4+ cores |
| **RAM** | 4GB | 8GB+ |
| **Storage** | 10GB | 20GB+ |

### **ARM64 Systems (Jetson, Raspberry Pi)**

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 4 cores | 6+ cores |
| **RAM** | 4GB | 8GB+ |
| **Storage** | 16GB | 32GB+ |

---

## 🚀 Production Deployment

### **1. Use Docker Compose with Restart Policy**

Already configured:
```yaml
restart: unless-stopped
```

### **2. Set Up Health Checks**

Already configured:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### **3. Monitor Logs**

```bash
# View logs
./run.sh logs

# Or use external logging
docker-compose logs --tail=1000 > app.log
```

### **4. Auto-Start on Boot**

```bash
# Enable Docker service
sudo systemctl enable docker

# Container will auto-start due to restart policy
```

---

## 📝 Examples

### **Example 1: Basic Deployment**

```bash
cd docker
cp .env.example .env
# Edit .env and add CEREBRAS_API_KEY
./run.sh start
```

### **Example 2: ARM64 Deployment (Jetson)**

```bash
cd docker
cp .env.example .env
# Edit .env
./build.sh --arm
docker-compose -f docker-compose.arm64.yml up -d
```

### **Example 3: Custom Port**

Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"
```

```bash
./run.sh start
# Access at http://localhost:8080
```

### **Example 4: Development Mode**

```bash
# Mount source code for live editing
docker-compose -f docker-compose.yml \
  -v $(pwd)/..:/app \
  up
```

---

## 🔄 Updates and Maintenance

### **Update Application**

```bash
# Pull latest code
git pull

# Rebuild and restart
./run.sh rebuild
```

### **Update Dependencies**

```bash
# Edit requirements.txt
# Then rebuild
./run.sh rebuild
```

### **Clean Up Old Images**

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune
```

---

## ✅ Checklist

### **Pre-Deployment:**
- [ ] Docker and Docker Compose installed
- [ ] `.env` file created with API keys
- [ ] Firewall configured (if needed)
- [ ] Sufficient disk space available

### **Deployment:**
- [ ] Image built successfully
- [ ] Container started
- [ ] Health check passing
- [ ] Application accessible

### **Post-Deployment:**
- [ ] Test chat functionality
- [ ] Test RAG upload and search
- [ ] Test web search (if enabled)
- [ ] Verify data persistence
- [ ] Set up monitoring/logging

---

## 📚 Additional Resources

- **Main Documentation:** `../README.md`
- **ARM Deployment Guide:** `../ARM_EDGE_DEPLOYMENT.md`
- **RAG Troubleshooting:** `../RAG_TROUBLESHOOTING.md`
- **Docker Documentation:** https://docs.docker.com/

---

## 🆘 Support

If you encounter issues:

1. Check logs: `./run.sh logs`
2. Verify `.env` configuration
3. Check Docker status: `./run.sh status`
4. Review troubleshooting section above
5. Check main documentation

---

**Your Cerebras Chat Interface is now containerized and ready for deployment!** 🐳✨
