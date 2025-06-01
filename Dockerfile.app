FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install OS-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl bash libssl-dev libstdc++6 ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements separately for better layer caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy the rest of the backend source code
COPY backend/ .

# Optional: Print contents for debugging (you can remove later)
# RUN ls -la /app

# Default command to run the app
CMD ["python", "run.py"]
