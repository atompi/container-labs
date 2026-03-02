FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    chromium \
    chromium-sandbox \
    curl \
    fonts-liberation \
    fonts-noto-color-emoji \
    fonts-noto-cjk \
    git \
    jq \
    novnc \
    python3 \
    socat \
    websockify \
    x11vnc \
    xvfb \
  && rm -rf /var/lib/apt/lists/*

COPY scripts/sandbox-browser-entrypoint.sh /usr/local/bin/openclaw-sandbox-browser
RUN chmod +x /usr/local/bin/openclaw-sandbox-browser

RUN useradd --create-home --shell /bin/bash sandbox
USER sandbox
WORKDIR /home/sandbox

EXPOSE 9222 5900 6080

CMD ["openclaw-sandbox-browser"]
