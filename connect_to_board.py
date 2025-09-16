import re
import subprocess
import sys
from pathlib import Path


# List of files to copy to the Pico (local -> remote)
FILE_NAMES = ["main.py", "sensors.py", "storage.py", "audio.py", "tests.py"]

files_to_copy = []
for file_name in FILE_NAMES:
    files_to_copy.append({"local": file_name, "remote": file_name})


def run(cmd: list[str], check=True, capture=True):
    """Run a command. If rshell is missing, print a friendly hint."""
    try:
        # Ensure rshell is installed
        return subprocess.run(
            cmd,
            check=check,
            text=True,
            capture_output=capture,
        )
    except FileNotFoundError:
        # If rshell is missing, raise an error with a friendly hint
        if cmd and "rshell" in cmd[0]:
            sys.exit("ERROR: `rshell` not found. Install it with:\n  python3 -m pip install rshell")
        raise


def find_pico_port() -> str:
    # Find the Pico's serial port
    """Use `rshell -l` to find the Pico's serial port (prefer /dev/cu.* on macOS)."""
    res = run(["rshell", "-l"], check=False)
    out = (res.stdout or "") + (res.stderr or "")

    # Try to match a line that mentions MicroPython, e.g. ... vendor 'MicroPython' ... @/dev/cu.usbmodem101
    m = re.search(r"vendor 'MicroPython'.+?@(/dev/(?:cu|tty)\.usbmodem[^\s]*)", out)
    if not m:
        # Fallback: just grab the first usbmodem device
        m = re.search(r"@(/dev/(?:cu|tty)\.usbmodem[^\s]*)", out)
    if not m:
        print(out)
        sys.exit("ERROR: Could not find a Pico serial device via `rshell -l`.")

    port = m.group(1)
    # Prefer /dev/cu.* variant if we matched /dev/tty.*
    if port.startswith("/dev/tty"):
        port = port.replace("/dev/tty", "/dev/cu")
    print(f"Found Pico on: {port}")
    return port


def copy_files(port: str):
    """Copy each (local -> remote) file in files_to_copy to /pyboard/ on the Pico."""
    # Copy each file
    for item in files_to_copy:
        local = Path(item["local"])
        remote = item["remote"]
        if not local.exists():
            print(f"WARNING: Skipping missing file: {local}")
            continue
        cmd = [
            "rshell", "-p", port, "cp",
            str(local),
            f"/pyboard/{remote}",
        ]
        res = run(cmd, check=False)
        if res.returncode == 0:
            print(f"✓ Copied {local} -> /pyboard/{remote}")
        else:
            print(res.stdout, res.stderr)
            sys.exit("ERROR: rshell copy failed.")

def open_repl(port: str):
    """Open the MicroPython REPL. Exit REPL with Ctrl-X."""
    print("Opening REPL... (press Ctrl-X to exit)")
    # Don’t capture output so you can interact with >>> directly.
    subprocess.run(["rshell", "-p", port, "repl"], check=True, capture_output=False)

def main():
    port = find_pico_port()
    copy_files(port)
    open_repl(port)

if __name__ == "__main__":
    main()