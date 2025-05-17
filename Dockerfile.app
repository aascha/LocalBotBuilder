FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    git curl bash libssl-dev libstdc++6 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/ /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN echo "Listing contents of /app:" && ls -la /app

CMD ["python", "run.py"]
