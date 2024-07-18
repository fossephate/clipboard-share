import pyperclip
import time
import argparse
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# JSONbin.io API
API_KEY = os.getenv("JSONBIN_API_KEY")
BIN_ID = os.getenv("JSONBIN_BIN_ID")
BASE_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

headers = {
    "Content-Type": "application/json",
    "X-Master-Key": API_KEY
}



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
    
def monitor_clipboard_file(filename):
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

def read_clipboard_to_api():
    clipboard_content = pyperclip.paste().replace('\r\n', '\n')
    data = {"content": clipboard_content}
    response = requests.put(BASE_URL, json=data, headers=headers)
    if response.status_code == 200:
        print("Clipboard content saved to JSONbin.io")
    else:
        print("Failed to save clipboard content")

def write_api_to_clipboard():
    response = requests.get(BASE_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        content = data["record"]["content"]
        pyperclip.copy(content)
        print("Content from JSONbin.io copied to clipboard")
    else:
        print("Failed to retrieve content from JSONbin.io")

def read_api():
    response = requests.get(BASE_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["record"]["content"]
    else:
        print("Failed to retrieve content from JSONbin.io")
        return None
    


def monitor_clipboard_api():
    last_clip_content = pyperclip.paste().replace('\r\n', '\n')
    print("Monitoring clipboard. Press Ctrl+C to stop.")
    try:
        while True:
            current_clip_content = pyperclip.paste().replace('\r\n', '\n')
            if current_clip_content != last_clip_content:
                data = {"content": current_clip_content}
                response = requests.put(BASE_URL, json=data, headers=headers)
                if response.status_code == 200:
                    print("New clipboard content saved to JSONbin.io")
                    last_clip_content = current_clip_content
                else:
                    print("Failed to save clipboard content")
            
            api_content = read_api()
            if api_content and current_clip_content != api_content:
                pyperclip.copy(api_content)
                print("Content from JSONbin.io copied to clipboard")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("Clipboard monitoring stopped")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cross-platform clipboard sharing tool")
    parser.add_argument("filename", help="File to read from or write to", nargs="?")
    args = parser.parse_args()
    if args.filename:
        monitor_clipboard_file(args.filename)
    else:
        monitor_clipboard_api()