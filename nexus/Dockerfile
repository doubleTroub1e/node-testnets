# Use a minimal base image
FROM ubuntu:22.04

# Define build-time variables
ARG DEBIAN_FRONTEND=noninteractive

# ===================================================
# Environment Configuration
# ===================================================
ENV HOME=/root \
    PATH=/root/.cargo/bin:$PATH \
    NEXUS_HOME=/root/.nexus \
    NONINTERACTIVE=true

# Install necessary dependencies and clean up to reduce image size
RUN apt update && \
    apt install -y --no-install-recommends \
        wget \
        curl \
        cmake \
        build-essential \
        ca-certificates \
        pkg-config \
        unzip \
        libssl-dev \
        git && \
    rm -rf /var/lib/apt/lists/*

# Install Rust and add RISC-V target
RUN curl -sSf https://sh.rustup.rs | sh -s -- -y && \
    rustup target add riscv32i-unknown-none-elf && \
    rm -rf /root/.cargo/registry /root/.cargo/git && \
    echo 'source $HOME/.cargo/env' >> $HOME/.bashrc

RUN apt update && \
    apt install -y --no-install-recommends \
    protobuf-compiler       && \
    rm -rf /var/lib/apt/lists/*



# Set working directory
WORKDIR $HOME

# Download and set up entrypoint script
RUN curl -L https://cli.nexus.xyz/install.sh -o /root/entrypoint.sh && \
    chmod +x /root/entrypoint.sh

# Define a volume
VOLUME [$NEXUS_HOME]

# Define the default entrypoint
ENTRYPOINT ["/bin/bash", "/root/entrypoint.sh"]

