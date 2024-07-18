import pyperclip
import os
import time
import argparse

def read_clipboard_to_file(filename):
    clipboard_content = pyperclip.paste()
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(clipboard_content)
    print(f"Clipboard content saved to {filename}")

def write_file_to_clipboard(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        pyperclip.copy(file_content)
        print(f"Content from {filename} copied to clipboard")
    else:
        print(f"File {filename} not found")

def monitor_clipboard(filename):
    last_content = pyperclip.paste()
    print("Monitoring clipboard. Press Ctrl+C to stop.")
    try:
        while True:
            current_content = pyperclip.paste()
            if current_content != last_content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(current_content)
                print(f"New clipboard content saved to {filename}")
                last_content = current_content
            time.sleep(1)
    except KeyboardInterrupt:
        print("Clipboard monitoring stopped")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cross-platform clipboard sharing tool")
    parser.add_argument("filename", help="File to read from or write to")
    args = parser.parse_args()

    monitor_clipboard(args.filename)