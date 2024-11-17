# Heminetwork Setup

This guide will help you configure the Heminetwork node by setting up your keys and environment variables.

## Steps to Configure

1. **Save Your Keys**  
   If you already have your keys, save them in the following format under `./heminetwork-key/popm-address.json`:

   ```json
   {
     "ethereum_address": "0x441c6CCfb4Da48d9ea145Bcdc06d8D05eCDFDAA5",
     "network": "testnet",
     "private_key": "500d4b1ca3e4afd9cc5b94667ec7b41bcb6XXXXXXXXXXXXXXXXXXXXXXXXXX",
     "public_key": "03bdfbd12bba4ee73a808afa01fb9db57a3322ecfff44415e62eb91538eb394f2e",
     "pubkey_hash": "msdbkTZHQ9hhaXyXxKmvERhJFPRjQ3XKsZ"
   }

2. **Set the `HEMI_POPM_BTC_PRIVKEY` Variable**
    You will need to provide the `HEMI_POPM_BTC_PRIVKEY` in your `.env` file. To do this:

    Open  `.env` file in the root of your project.
    Set the `HEMI_POPM_BTC_PRIVKEY` variable:

    `HEMI_POPM_BTC_PRIVKEY=your_private_key_here`

3. **If you do not have the private key**:
 Start the Docker Compose. Run the following command to automatically generate the necessary private key:

        ````bash
        docker compose up -d heminetwork
    
    Once the private key is generated, locate the private_key in the `./key/popm-address.json` file, and update the `.env` file 

4. **Force-Recreate the Containers**
    After updating the `.env` file, force-recreate the Docker containers with this command:

        ````bash
        docker compose up -d heminetwork --force-recreate

## Faucet Tokens
    You  need to get faucet tokens for your address. This will help you test your node and interact with the network.

    Check the following article for more information on how to obtain faucet tokens:
    [Hemi Network Node Guide - Medium](https://medium.com/@fmusicmc/hemi-networke-guide-node