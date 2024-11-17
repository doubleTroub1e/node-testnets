# Use an official Ubuntu base image
FROM ubuntu:22.04

# Update and install dependencies
RUN apt update && apt upgrade -y && \
    apt install -y curl wget tar jq && \
    rm -rf /var/lib/apt/lists/*

# Use GitHub API to get the latest version of heminetwork

# Set environment variables for POPM
ENV POPM_BTC_PRIVKEY=your_private_key_here
ENV POPM_STATIC_FEE=110
ENV POPM_BFG_URL=wss://testnet.rpc.hemi.network/v1/ws/public

WORKDIR /POP

# Download and extract the heminetwork files
RUN VERSION=$(curl -sLX GET "https://api.github.com/repos/hemilabs/heminetwork/releases/latest" | jq --raw-output '.tag_name') && \
    mkdir -p /POP/heminetwork_latest_linux_amd64 && \
    curl -fsSL https://github.com/hemilabs/heminetwork/releases/download/${VERSION}/heminetwork_${VERSION}_linux_amd64.tar.gz | tar -xz --strip-components=1 -C /POP/heminetwork_latest_linux_amd64


COPY entrypoint.sh /POP/entrypoint.sh

WORKDIR /POP/heminetwork_latest_linux_amd64

# Start the popmd process when the container runs
ENTRYPOINT ["/bin/bash", "/POP/entrypoint.sh"]

CMD ["./popmd"]
