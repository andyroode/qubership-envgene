#########################################
## Stage 1: Build dependencies
FROM ghcr.io/netcracker/qubership-base-module-dockerimage:v2.0.0 AS builder
USER root

# Copy only dependency files first for better caching
COPY build_envgene/build/pip.conf /etc/pip.conf
COPY build_envgene/build/requirements.txt /build/requirements.txt
COPY build_envgene/build/requirements.yml /build/requirements.yml

# Install system dependencies in a single layer with cleanup
RUN apk update \
    && apk add --no-cache \
        git \
        python3 \
        py3-pip \
        py3-cryptography \
        py3-openssl \
        openssh-client \
        ca-certificates \
        coreutils \
        curl \
        sudo \
        zip \
        unzip \
        build-base \
        libxml2-dev \
        libxslt-dev \
        zlib-dev \
        jq \
    && curl --retry 3 --retry-connrefused --retry-delay 5 -LO https://github.com/mozilla/sops/releases/download/v3.9.0/sops-v3.9.0.linux.amd64 \
    && chmod +x sops-v3.9.0.linux.amd64 \
    && mv sops-v3.9.0.linux.amd64 /usr/local/bin/sops \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /build/requirements.txt \
    && pip install ansible --upgrade \
    && rm -rf /usr/lib/python3.12/site-packages/ansible_collections/* \
    && ansible-galaxy collection install -r /build/requirements.yml -p /tmp/ansible-collections \
    && pip install PyYAML \
    && apk del build-base libxml2-dev libxslt-dev zlib-dev \
    && rm -rf /var/cache/apk/* /var/tmp/* \
    && find /usr/lib/python3.12 -name "*.pyc" -delete \
    && find /usr/lib/python3.12 -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Install Python packages
COPY python /python
RUN pip install --no-cache-dir /python/jschon-sort \
    && pip install --no-cache-dir /python/envgene \
    && pip install --no-cache-dir /python/integration \
    && rm -rf /python

#########################################
## Stage 2: Runtime image - using Alpine for smaller size
FROM alpine:3.18 AS runtime

# Install only runtime dependencies
RUN apk add --no-cache \
        python3 \
        py3-pip \
        git \
        curl \
        jq \
        zip \
        unzip \
        sudo \
        openssh-client \
        ca-certificates \
    && rm -rf /var/cache/apk/*

# Copy Python packages and dependencies from builder
COPY --from=builder /usr/lib/python3.12 /usr/lib/python3.12

# Copy only necessary binaries
COPY --from=builder /usr/local/bin/sops /usr/local/bin/sops

# Copy application files
COPY build_envgene/build/pip.conf /etc/pip.conf
COPY build_envgene/ansible /module/ansible
COPY build_envgene/scripts /module/scripts
COPY build_envgene/workflows /workflows

COPY build_* create_* produce_* sort* /build_env/
COPY scripts /build_env/scripts
COPY env-builder /build_env/env-builder
COPY schemas /build_env/schemas

# Set environment variables
ENV ANSIBLE_LIBRARY=/module/ansible/library
ENV PYTHONPATH=/usr/lib/python3.12/site-packages
ENV PATH=/usr/local/bin:$PATH

# Set permissions
RUN chmod 754 /module/scripts/*

WORKDIR /module/ansible
