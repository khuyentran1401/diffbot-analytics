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

# Copy project configuration first for better caching
COPY pyproject.toml .

# Install Python dependencies using uv
RUN uv sync --no-dev

# Copy application code
COPY . .

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application using uv
CMD ["uv", "run", "streamlit", "run", "analytics_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]