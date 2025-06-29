# Function to get PID based on port number
get_pid_by_port() {
    PORT=$1
    PID=$(lsof -t -i:$PORT)
    echo $PID
}

# Function to kill the process by PID
kill_process_by_port() {
    PORT=$1
    PID=$(get_pid_by_port $PORT)
    if [ ! -z "$PID" ]; then
        sudo kill -9 $PID
        echo "Process on port $PORT has been killed."
    else
        echo "No process found on port $PORT."
    fi
}

# Example usage
PORT=8128 # Replace with your desired port number
kill_process_by_port $PORT

/home/jacky/anaconda3/envs/vllm/bin/vllm serve JackyHoCL/whisper-large-v3-turbo-cantonese-yue-english \
  --gpu-memory-utilization 0.7 \
  --served-model-name whisper-3 \
  --port 8128 \
  --task transcription &