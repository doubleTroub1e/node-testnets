#!/bin/bash

# Define the path to the address JSON file
ADDRESS_FILE=/key/popm-address.json

# Check if the address file exists
if [ ! -f "$ADDRESS_FILE" ]; then
    echo "$ADDRESS_FILE not found. Generating a new key pair..."
    # Run the keygen command to generate the key pair if the file doesn't exist
    /POP/heminetwork_latest_linux_amd64/keygen -secp256k1 -json -net="testnet" > "$ADDRESS_FILE"
fi

# Check if the file is empty
if [ ! -s "$ADDRESS_FILE" ]; then
    echo "$ADDRESS_FILE is empty. Sleeping for 10 minutes before exiting..."
    sleep 10m
    exit 1
fi

# Extract the private key from the JSON file using jq
POPM_BTC_PRIVKEY_FILE=$(jq -r '.private_key' "$ADDRESS_FILE")

# Check if the private key was successfully parsed
if [ -z "$POPM_BTC_PRIVKEY_FILE" ]; then
    echo "Failed to parse private_key from $ADDRESS_FILE. Exiting..."
    exit 1
fi

# Get the current POPM_BTC_PRIVKEY environment variable value
CURRENT_POPM_BTC_PRIVKEY=${POPM_BTC_PRIVKEY:-$(grep -E '^POPM_BTC_PRIVKEY=' /etc/environment | cut -d '=' -f2)}

# Compare the values
if [ "$POPM_BTC_PRIVKEY_FILE" != "$CURRENT_POPM_BTC_PRIVKEY" ]; then
    echo "The POPM_BTC_PRIVKEY in $ADDRESS_FILE differs from the environment variable. Values are different!"
    echo "Expected: ${POPM_BTC_PRIVKEY_FILE:0:-45}***************"
    echo "Found in env: $CURRENT_POPM_BTC_PRIVKEY"

    # Sleep for 10 minutes and then exit with code 1
    sleep 10m
    exit 1
fi

# Print that the private key matches
echo "POPM_BTC_PRIVKEY values match. Proceeding to start the service."

# Execute the original command passed to the container (starting popmd)
exec "$@"