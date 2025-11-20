#!/bin/bash
# Auto-restart wrapper for fit_pymc.py when PyTensor cache errors occur

# --- CONFIG ---
CMD="python fit_pymc.py all 2000 1000 4"
MAX_RETRIES=15  # how many times to retry before giving up
SLEEP=5         # seconds to wait before restarting

# --- MAIN LOOP ---
for ((i=1; i<=MAX_RETRIES; i++)); do
    echo "-----------------------------"
    echo "Run $i of $MAX_RETRIES: $CMD"
    echo "-----------------------------"
    
    # Run your command
    $CMD
    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        echo "Fit finished successfully on attempt $i."
        exit 0
    else
        echo "Crash detected (exit code $EXIT_CODE)."
        echo "Purging PyTensor cache..."
        pytensor-cache purge

        echo "Waiting $SLEEP seconds before retry..."
        sleep $SLEEP
    fi
done

echo "Max retries ($MAX_RETRIES) reached. Exiting."
exit 1
