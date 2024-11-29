# Nexus Prover Setup

This guide helps you configure your Nexus Prover after the first start. 

## Prerequisite 

1. Visit the official Nexus webpage: [https://beta.nexus.xyz/](https://beta.nexus.xyz/). Note that no referral code is required.
2. In the bottom left corner, click on the account icon and link your email.
3. Check your email inbox and confirm your email address.
4. Return to [https://beta.nexus.xyz/](https://beta.nexus.xyz/). Your linked Prover ID will now appear in the bottom left corner. This ID is associated with your email. 
   - Copy the Prover ID by tapping the copy icon and waiting for the "Copied!" confirmation message.
5. Save the Prover ID in a file located at `./nexus/prover-id`.
6. Proceed with the startup steps below.

## How to Start

   ```bash
   docker compose up -d
   ```
   To stop
   ```bash
   docker compose down
   ```

## Steps to Configure

1. **Start the Prover**  
   Run the Nexus Prover as specified in your setup instructions.

2. **Check the Logs**  
   After starting, check the logs to find your assigned `prover-id`. Save this ID under `./nexus/prover-id`.

3. **Save the `prover-id`**  
   Create a file named `prover-id` in the `./nexus` directory and paste your `prover-id` there.  
   Example:
   ```plaintext
   ./nexus/prover-id
   ```

## Example Log Output

Here’s an example of how the logs will look during the first run:

````plaintext
 Compiling uuid v1.10.0
 Compiling jsonrpsee v0.23.2
 Compiling home v0.5.9
 Finished release profile [optimized] target(s) in 1m 50s
 Running target/release/prover beta.orchestrator.nexus.xyz
 Could not read prover-id file: No such file or directory (os error 2)
     Failed to create .nexus directory: File exists (os error 17)
     Connecting to wss://beta.orchestrator.nexus.xyz:443/prove...
     Connected.
     Your assigned prover identifier is XXXX
````

Replace `XXXX` with the actual `prover-id` from the logs.

## Notes
This is a temporary solution until the development team fixes the issue with auto-creation and auto-saving of the prover-id.

For further assistance, please refer to the official documentation or contact support.

