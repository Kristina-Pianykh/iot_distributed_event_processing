#!/usr/bin/env bash

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

# Launch your commands in the background
python3 joystick.py & PIDS+=($!)
python3 humidity_temp_pressure.py & PIDS+=($!)
python3 accelerator.py & PIDS+=($!)
# uvicorn server.http_server:app --reload --host 0.0.0.0 & PIDS+=($!)

# Wait for all background commands to complete
wait
