#!/bin/bash

# Initialize counter
count=0

while pgrep -x cjdroute >/dev/null; do
    # If cjdroute is running, attempt to kill it
    sudo pkill cjdroute

    # Increment the counter
    ((count++))

    # If it exceeds 10 attempts, use a more forceful method
    if [[ $count -gt 10 ]]; then
        echo "Using forceful method to kill cjdroute."
        pkill -9 cjdroute
    fi

    # Wait for a second
    sleep 1
done

echo "cjdroute has been terminated."
