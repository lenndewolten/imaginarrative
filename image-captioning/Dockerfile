FROM ubuntu:jammy-20240111

RUN apt-get update && \
    apt-get install --no-install-recommends -y python3 && \
    apt-get install --no-install-recommends -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

ARG ENTRY_DIR="/app"
WORKDIR ${ENTRY_DIR}

# COPY download_models.py .
# RUN python3 download_models.py

COPY app.py .


CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:6000", "--log-level", "debug", "--timeout", "500", "app:app"]