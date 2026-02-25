FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl \
        git \
        nmap \
        netcat-openbsd \
        dnsutils \
        whois \
        iputils-ping \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY kali_mcp_server.py /app/kali_mcp_server.py

RUN python3 -m pip install --break-system-packages --no-cache-dir "mcp>=1.0.0,<2.0.0"

CMD ["python3", "/app/kali_mcp_server.py"]
