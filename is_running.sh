#!/bin/bash

# Use the ps command piped to grep to check if cjdroute is running
if ps -A | grep -q 'cjdroute'; then
    # If the previous command returns a non-zero status, it means cjdroute is running
    echo "cjdroute is running."
else
    # If the previous command returns a zero status, it means cjdroute is not running
    echo "cjdroute is not running."
fi
