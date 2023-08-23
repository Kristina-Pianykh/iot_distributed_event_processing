#!/usr/bin/env bash

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Error: No argument provided."
  echo "Usage: ./launch.sh [DEVICE_ID]"
  exit 1
fi

# Access the argument
DEVICE_ID="$1"

# Array to store the PIDs of background processes
PIDS=()

# Function to handle the SIGINT signal
handle_sigint() {
    echo "Ctrl+C detected. Killing child processes..."
    # Send SIGTERM to all background processes
    for pid in "${PIDS[@]}"; do
        kill "$pid"
    done
    exit
}

# Register the SIGINT handler function
trap handle_sigint SIGINT

# Remove the old configuration
rm -rf .config/sense_hat

# Check if all pi servers are healthy
python3 check_server_health.py

if [ "$DEVICE_ID" == "pi_3" ]; then
    # Launch in the background
    python3 joystick.py & PIDS+=($!)
    python3 humidity_temp_pressure.py & PIDS+=($!)
    python3 accelerator.py & PIDS+=($!)
else
    # Launch in the background
    python3 sound.py & PIDS+=($!)
fi

# Wait for all background commands to complete
wait
