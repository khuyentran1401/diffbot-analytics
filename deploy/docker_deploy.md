# 🐳 Docker Deployment Guide

Deploy the Diffbot Analytics Dashboard using Docker for production environments, self-hosting, or local development.

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose (included with Docker Desktop)
- Diffbot API token

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/diffbot-analytics.git
   cd diffbot-analytics
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your DIFFBOT_API_TOKEN
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the app**
   - Open your browser to `http://localhost:8501`

### Using Docker Build

1. **Build the image**
   ```bash
   docker build -t diffbot-analytics .
   ```

2. **Run the container**
   ```bash
   docker run -d \
     --name diffbot-analytics \
     -p 8501:8501 \
     -e DIFFBOT_API_TOKEN=your_token_here \
     diffbot-analytics
   ```

> **Note**: The Docker image now uses uv for faster dependency resolution and installation.

## Production Deployment

### Environment Configuration

Create a production `.env` file:
```env
# Required
DIFFBOT_API_TOKEN=your_diffbot_token_here

# Optional production settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

### Docker Compose Production Setup

Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  diffbot-analytics:
    build: .
    ports:
      - "80:8501"  # Expose on port 80
    environment:
      - DIFFBOT_API_TOKEN=${DIFFBOT_API_TOKEN}
    volumes:
      - ./sample_data:/app/sample_data:ro
    restart: always
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Add reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - diffbot-analytics
```

### Run Production Setup

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Advanced Configuration

### Custom Dockerfile

For specific requirements, modify the `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && . $HOME/.cargo/env \
    && ln -s $HOME/.cargo/bin/uv /usr/local/bin/uv \
    && rm -rf /var/lib/apt/lists/*

# Copy project configuration and install Python deps
COPY pyproject.toml .
RUN uv sync --no-dev

# Copy application
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Expose port
EXPOSE 8501

# Run application using uv
CMD ["uv", "run", "streamlit", "run", "analytics_dashboard.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
```

### Nginx Reverse Proxy

Create `nginx.conf` for SSL termination and load balancing:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream streamlit {
        server diffbot-analytics:8501;
    }

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://streamlit;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

## Container Management

### Basic Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Update containers
docker-compose pull
docker-compose up -d --force-recreate
```

### Monitoring

```bash
# Check container status
docker ps

# Monitor resource usage
docker stats

# View application logs
docker logs diffbot-analytics -f

# Execute commands in container
docker exec -it diffbot-analytics bash
```

## Security Best Practices

### 1. Use Non-Root User
The Dockerfile creates a non-root user for security:
```dockerfile
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
```

### 2. Secure Environment Variables
```bash
# Use Docker secrets in production
echo "your_diffbot_token" | docker secret create diffbot_token -

# Reference in compose file
services:
  app:
    secrets:
      - diffbot_token
```

### 3. Network Security
```yaml
# Create custom network
networks:
  app-network:
    driver: bridge

services:
  diffbot-analytics:
    networks:
      - app-network
```

### 4. Resource Limits
```yaml
deploy:
  resources:
    limits:
      memory: 1G
      cpus: '0.5'
    reservations:
      memory: 512M
      cpus: '0.25'
```

## Troubleshooting

### Common Issues

**Container Won't Start**
```bash
# Check logs
docker logs diffbot-analytics

# Check if port is available
netstat -tlnp | grep 8501

# Verify environment variables
docker exec diffbot-analytics env | grep DIFFBOT
```

**Health Check Failures**
```bash
# Test health endpoint manually
docker exec diffbot-analytics curl http://localhost:8501/_stcore/health

# Check container resources
docker stats diffbot-analytics
```

**Permission Errors**
```bash
# Fix file permissions
sudo chown -R $(id -u):$(id -g) .

# Check Docker daemon permissions
sudo usermod -aG docker $USER
```

### Performance Optimization

1. **Multi-stage Builds**
```dockerfile
# Build stage
FROM python:3.11 as builder
# ... build dependencies

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /app /app
```

2. **Layer Caching**
```dockerfile
# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code last
COPY . .
```

3. **Image Size Optimization**
```bash
# Use alpine images
FROM python:3.11-alpine

# Install uv and dependencies efficiently
RUN apk add --no-cache curl gcc musl-dev \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && . $HOME/.cargo/env \
    && ln -s $HOME/.cargo/bin/uv /usr/local/bin/uv \
    && apk del gcc musl-dev
```

## Backup and Recovery

### Data Backup
```bash
# Backup container data
docker run --volumes-from diffbot-analytics -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz /app

# Restore data
docker run --volumes-from diffbot-analytics -v $(pwd):/backup alpine tar xzf /backup/backup.tar.gz
```

### Configuration Backup
```bash
# Export container configuration
docker inspect diffbot-analytics > container-config.json

# Backup Docker Compose files
tar czf docker-backup.tar.gz docker-compose.yml .env nginx.conf
```

## Support

- **Docker Documentation**: [docs.docker.com](https://docs.docker.com)
- **Docker Compose Reference**: [docs.docker.com/compose](https://docs.docker.com/compose)
- **Issue Reporting**: [GitHub Issues](https://github.com/yourusername/diffbot-analytics/issues)