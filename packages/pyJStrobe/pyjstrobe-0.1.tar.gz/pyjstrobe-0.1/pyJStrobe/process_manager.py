import subprocess
import threading
import os



class ProcessManager:
    def __init__(self, callback=None):
        build_mode = os.getenv('BUILD_MODE', 'Release')  # Default to 'release' if not set
        print(build_mode)
        if build_mode=='Debug':
            path_to_exe = r"C:\source\jStrobe\jsApp\Debug\jStrobe.exe"
        else:
            path_to_exe = r"C:\Program Files\jStrobe\jStrobe\jStrobe.exe"



        self.process = subprocess.Popen(
            [path_to_exe, '--from-python'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        self.callback = callback  # Custom callback for processing messages
        self.keep_reading = True  # Flag to control the reading loop
        self.reader_thread = threading.Thread(target=self.read_messages)
        self.reader_thread.daemon = True  # Allow thread to exit when main program exits
        self.reader_thread.start()

    def write_message(self, message):
        """Write a message to the process's stdin."""
        self.process.stdin.write(message + "\n")
        self.process.stdin.flush()

    def read_messages(self):
        """Read messages from the process's stdout."""
        while self.keep_reading:
            response = self.process.stdout.readline().strip()
            if response:
                if response == "COMPLETE":
                    print("Process completed.")
                    self.keep_reading = False  # Stop reading messages
                    break
                if self.callback:
                    response_message = self.callback(response)
                    if response_message:
                        self.write_message(response_message)

    def cleanup(self):
        """Clean up the process and close streams."""
        print("Cleaning up resources...")
        self.keep_reading = False  # Signal the thread to stop reading
        self.running = False  
        self.reader_thread.join()  # Wait for the thread to finish
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.stderr.close()
        if self.process:
            self.process.terminate()  # Try to terminate the process gracefully
            try:
                return self.process.wait(timeout=5)  # Wait up to 5 seconds for it to finish
            except subprocess.TimeoutExpired:
                print("Process did not terminate, force killing it...")
                self.process.kill()  # Force kill the process if it doesn't terminate in time
                return self.process.wait()  # Ensure it finishes
