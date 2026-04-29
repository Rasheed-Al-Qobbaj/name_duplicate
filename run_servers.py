import subprocess
import time
import sys

def main():
    # We assume this script is run with the correct python environment (activated in batch file)
    python_exe = sys.executable
    print(f"Using Python environment: {python_exe}")

    processes = []
    
    try:
        print("--- Starting Flask Backend ---")
        # backend.py needs to be in the current directory or addressed correct
        p1 = subprocess.Popen([python_exe, "backend.py"])
        processes.append(p1)

        print("--- Starting HTTP Server ---")
        p2 = subprocess.Popen([python_exe, "-m", "http.server", "8000"])
        processes.append(p2)

        print("\nBoth servers are running. Logs will appear below.")
        print("Press Ctrl+C to stop all servers cleanly.\n")

        # Keep the script running to monitor child processes
        while True:
            time.sleep(1)
            # Check if any process has exited unexpectedly
            if p1.poll() is not None:
                print("Backend process stopped.")
                break
            if p2.poll() is not None:
                print("HTTP Server stopped.")
                break

    except KeyboardInterrupt:
        print("\n\nStopping servers...")
    finally:
        # Terminate all started processes
        for p in processes:
            if p.poll() is None:
                p.terminate()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
