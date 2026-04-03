#!/bin/bash
echo "Decrypting photos..."
cd "$(dirname "$0")/.."

mkdir -p static/img/protected

if [ -f "static/protected-photos.enc" ]; then
    if [ -z "$PHOTO_DECRYPTION_KEY" ]; then
        echo "WARNING: PHOTO_DECRYPTION_KEY environment variable is not set. Decryption will fail."
    fi
    
    # Decrypt and extract the tarball
    openssl enc -d -aes-256-cbc -salt -pbkdf2 -pass env:PHOTO_DECRYPTION_KEY -in static/protected-photos.enc | tar xzf - -C static/img/protected
    
    echo "Decryption successful!"
else
    echo "No encrypted photos found (static/protected-photos.enc), skipping decryption."
fi
