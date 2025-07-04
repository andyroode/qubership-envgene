#########################################
## Build envgene image based on qubership-base-module-dockerimage
FROM ghcr.io/netcracker/qubership-base-module-dockerimage:feature-optimize_dockerimage

USER root

# Copy dependency files
COPY build_envgene/build/requirements.txt /build/requirements.txt
COPY build_envgene/build/requirements.yml /build/requirements.yml

# Install additional system dependencies (including build dependencies)
RUN apk add --no-cache \
        git \
        openssh-client \
        sudo \
        zip \
        unzip \
        build-base \
        libxml2-dev \
        libxslt-dev \
        zlib-dev

# Install additional Python packages in the existing venv
RUN source /module/venv/bin/activate \
    && pip install --no-cache-dir -r /build/requirements.txt \
    && pip install ansible --upgrade \
    && ansible-galaxy collection install -r /build/requirements.yml -p /tmp/ansible-collections \
    && pip install PyYAML

# Install custom Python packages
COPY python /python
RUN source /module/venv/bin/activate \
    && pip install --no-cache-dir /python/jschon-sort \
    && pip install --no-cache-dir /python/envgene \
    && pip install --no-cache-dir /python/integration \
    && rm -rf /python

# Clean up build dependencies and cache
RUN apk del build-base libxml2-dev libxslt-dev zlib-dev \
    && rm -rf /var/cache/apk/* /var/tmp/* /tmp/* \
    && find /module/venv -name "*.pyc" -delete \
    && find /module/venv -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Copy application files (only necessary directories)
COPY build_envgene/ansible /module/ansible
COPY build_envgene/scripts /module/scripts
COPY build_envgene/workflows /workflows

# Copy other build files
COPY scripts /build_env/scripts
COPY env-builder /build_env/env-builder
COPY schemas /build_env/schemas

# Set environment variables
ENV ANSIBLE_LIBRARY=/module/ansible/library

# Ensure scripts are executable and owned by ci user
RUN chmod 754 /module/scripts/* && \
    chown -R ci:ci /module/scripts

USER ci

WORKDIR /module/ansible
