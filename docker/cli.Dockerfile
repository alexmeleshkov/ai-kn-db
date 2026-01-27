FROM node:20-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip \
    git ca-certificates bash \
    docker.io docker-compose-plugin \
  && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir pyyaml

WORKDIR /workspace
CMD ["bash"]
