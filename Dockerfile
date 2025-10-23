FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

# (opcional) instalar compiladores para pacotes que precisem compilar
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && \
    python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc build-essential && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "run.py"]