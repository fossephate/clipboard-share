import pyperclip
import os
import time
import argparse

def read_clipboard_to_file(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    clipboard_content = pyperclip.paste()
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(clipboard_content)
    print(f"Clipboard content saved to {filename}")

def write_file_to_clipboard(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        file_content = f.read()
    pyperclip.copy(file_content)
    print(f"Content from {filename} copied to clipboard")

def read_file(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    with open(filename, 'r', encoding='utf-8') as f:
        file_content = f.read()
        return file_content

def monitor_clipboard(filename):
    last_clip_content = pyperclip.paste()
    # last_file_content = read_file(filename)
    print("Monitoring clipboard. Press Ctrl+C to stop.")
    try:
        while True:
            current_clip_content = pyperclip.paste().replace('\r\n', '\n')
            if current_clip_content != last_clip_content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(current_clip_content)
                print(f"New clipboard content saved to {filename}")
                last_clip_content = current_clip_content
            
            current_file_content = read_file(filename)
            if current_clip_content != current_file_content:
                write_file_to_clipboard(filename)
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("Clipboard monitoring stopped")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cross-platform clipboard sharing tool")
    parser.add_argument("filename", help="File to read from or write to")
    args = parser.parse_args()

    monitor_clipboard(args.filename)