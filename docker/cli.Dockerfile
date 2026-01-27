FROM node:20-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip \
    git ca-certificates bash curl \
  && rm -rf /var/lib/apt/lists/*

# Install PyYAML (break-system-packages is safe in a dev container)
RUN python3 -m pip install --no-cache-dir --break-system-packages pyyaml

# Download docker compose v2 standalone binary
RUN curl -SL https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-linux-x86_64 \
    -o /usr/local/bin/docker-compose \
  && chmod +x /usr/local/bin/docker-compose

WORKDIR /workspace
CMD ["bash"]
