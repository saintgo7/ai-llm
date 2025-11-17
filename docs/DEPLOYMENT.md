# Deployment Guide

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Environment Variables](#environment-variables)
4. [Production Deployment](#production-deployment)
5. [Monitoring](#monitoring)

---

## Local Development

### Prerequisites
- Python 3.8 or higher
- pip
- virtualenv (recommended)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/saintgo7/ai-llm.git
cd ai-llm
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create .env file:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run programs:**
```bash
# REST API Server
python 01_web_api/01_rest_api_server.py

# JWT Authentication
python 01_web_api/04_jwt_authentication.py

# Data Structures
python 02_data_structures_algorithms/11_binary_search_tree.py
```

---

## Docker Deployment

### Quick Start

**Start all services:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop services:**
```bash
docker-compose down
```

### Individual Services

**Build image:**
```bash
docker build -t ai-llm:latest .
```

**Run REST API:**
```bash
docker run -d \
  -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  --name ai-llm-api \
  ai-llm:latest
```

**Run JWT Auth:**
```bash
docker run -d \
  -p 5001:5001 \
  -e JWT_SECRET_KEY=your-jwt-secret \
  --name ai-llm-auth \
  ai-llm:latest \
  python 01_web_api/04_jwt_authentication.py
```

---

## Environment Variables

### Required Variables
```bash
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key
```

### Optional Variables
```bash
# Flask
FLASK_ENV=production
FLASK_DEBUG=False

# Database
DATABASE_URL=sqlite:///app.db
DATABASE_NAME=app.db

# API
API_HOST=0.0.0.0
API_PORT=5000

# Security
PASSWORD_HASH_ALGORITHM=sha256
ENABLE_RATE_LIMITING=True
MAX_REQUESTS_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
ENABLE_FILE_LOGGING=True
```

---

## Production Deployment

### AWS EC2

1. **Launch EC2 instance** (Ubuntu 22.04 LTS)

2. **Install Docker:**
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker
```

3. **Clone and deploy:**
```bash
git clone https://github.com/saintgo7/ai-llm.git
cd ai-llm
cp .env.example .env
# Edit .env with production settings
docker-compose up -d
```

4. **Configure Nginx reverse proxy:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /auth/ {
        proxy_pass http://localhost:5001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **Enable SSL with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Kubernetes

**Create deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-llm-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-llm-api
  template:
    metadata:
      labels:
        app: ai-llm-api
    spec:
      containers:
      - name: api
        image: ai-llm:latest
        ports:
        - containerPort: 5000
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: ai-llm-secrets
              key: secret-key
```

**Create service:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: ai-llm-api-service
spec:
  selector:
    app: ai-llm-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

---

## Monitoring

### Health Checks

**API Health:**
```bash
curl http://localhost:5000/api/health
```

**Docker Health:**
```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Logs

**Application logs:**
```bash
tail -f app.log
```

**Docker logs:**
```bash
docker-compose logs -f api-server
docker-compose logs -f auth-server
```

### Metrics

**Install Prometheus:**
```yaml
# docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
```

---

## Backup

**Database backup:**
```bash
# SQLite
cp app.db backups/app_$(date +%Y%m%d).db

# With Docker volume
docker-compose exec database pg_dump -U appuser appdb > backup.sql
```

**Automated backup:**
```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
```

---

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process using port
lsof -i :5000
# Kill process
kill -9 <PID>
```

**Docker build fails:**
```bash
# Clear Docker cache
docker system prune -a
# Rebuild
docker-compose build --no-cache
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Performance Optimization

### Gunicorn (Production WSGI)

```bash
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 01_web_api.01_rest_api_server:app
```

### Caching

```bash
# Install Redis
docker run -d -p 6379:6379 redis:alpine

# Use in code
from redis import Redis
cache = Redis(host='localhost', port=6379)
```

---

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS in production
- [ ] Configure firewall rules
- [ ] Enable rate limiting
- [ ] Set up log rotation
- [ ] Regular security updates
- [ ] Use environment variables for secrets
- [ ] Enable CORS properly
- [ ] Implement API versioning
