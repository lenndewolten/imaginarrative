FROM ubuntu:jammy-20240111

RUN apt-get update && \
    apt-get install --no-install-recommends -y python3 && \
    apt-get install --no-install-recommends -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ARG ENTRY_DIR="/app"
WORKDIR ${ENTRY_DIR}

COPY app.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]