# papa.py
import subprocess
import signal
import sys

# Start frontend
frontend = subprocess.Popen(["streamlit", "run", "frontend.py"])

# Start backend
backend = subprocess.Popen(["python", "backend.py"])

def cleanup(sig, frame):
    print("Stopping processes...")
    frontend.terminate()
    backend.terminate()
    sys.exit(0)

# Handle Ctrl+C to kill both
signal.signal(signal.SIGINT, cleanup)

# Wait for processes
frontend.wait()
backend.wait()
