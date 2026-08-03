FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN --mount=type=cache,id=openclaw-sandbox-bookworm-apt-cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,id=openclaw-sandbox-bookworm-apt-lists,target=/var/lib/apt,sharing=locked \
  sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
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
    xvfb

COPY --chmod=755 scripts/sandbox-browser-entrypoint.sh /usr/local/bin/openclaw-sandbox-browser

RUN useradd --create-home --shell /bin/bash sandbox
USER sandbox
WORKDIR /home/sandbox

EXPOSE 9222 5900 6080

CMD ["openclaw-sandbox-browser"]
