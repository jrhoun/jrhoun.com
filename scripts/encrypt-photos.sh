#!/bin/bash
echo "Encrypting photos..."
cd "$(dirname "$0")/.."

# Check if directory exists
if [ ! -d "static/img/protected" ]; then
    echo "Directory static/img/protected does not exist. Nothing to encrypt."
    exit 0
fi

# Use tar to compress the directory directly to stdout, then pipe it to openssl for encryption
tar czf - -C static/img/protected . | openssl enc -aes-256-cbc -salt -pbkdf2 -iter 100000 -md sha256 -out static/protected-photos.enc

echo "Done! The encrypted archive 'static/protected-photos.enc' is ready to be committed."
