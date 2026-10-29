"""
GoLo AI Assistant — Local Development Launcher
=============================================
Runs both the FastAPI backend and the primary web frontend.

Usage:
    python run.py
"""

import os
import sys
import time
import subprocess
import signal

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

def main():
    print("=" * 65)
    print("  🤖 Starting GoLo AI Assistant")
    print("=" * 65)
    
    # 1. Start FastAPI Backend (Port 8000)
    print("  -> Starting Backend API server on http://localhost:8000...")
    backend_cmd = [sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]
    backend_proc = subprocess.Popen(backend_cmd, cwd=BACKEND_DIR)

    # 2. Start Frontend Server (Port 3000)
    print("  -> Starting Frontend Web server on http://localhost:3000...")
    frontend_cmd = [sys.executable, "-m", "http.server", "3000", "--directory", FRONTEND_DIR]
    frontend_proc = subprocess.Popen(frontend_cmd)

    time.sleep(2)
    print("\n" + "=" * 65)
    print("  🚀 All services running successfully!")
    print("=" * 65)
    print("  🌐 Main Web App:       http://localhost:3000")
    print("  📑 API Docs (Swagger): http://localhost:8000/docs")
    print("  🩺 Backend Health:     http://localhost:8000/health")
    print("  📄 Documentation:      ./docs/")
    print("=" * 65)
    print("  Press Ctrl+C to stop both servers...\n")

    def shutdown(sig, frame):
        print("\nStopping GoLo AI servers...")
        backend_proc.terminate()
        frontend_proc.terminate()
        print("Done.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        backend_proc.wait()
    except KeyboardInterrupt:
        shutdown(None, None)

if __name__ == "__main__":
    main()
