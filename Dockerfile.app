FROM python:3.10-slim

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    git curl bash libssl-dev libstdc++6 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements first to leverage Docker caching
COPY backend/requirements.txt .

# Install Python dependencies in one step
RUN pip install --upgrade pip && pip install -r requirements.txt

# Now copy the rest of the code
COPY backend/ /app/

# (Optional) Debug output
RUN echo "Listing contents of /app:" && ls -la /app

CMD ["python", "run.py"]
