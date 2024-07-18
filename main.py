import os
import sys
import time

# Platform-specific imports
if sys.platform == 'darwin':
    use_carbon = True
    if use_carbon:
        from MacSharedClipboard import *
    else:
        from CarbonSharedClipboard import *
elif sys.platform == 'win32':
    from WindowsSharedClipboard import *

def monitorClipboard(clipboard_file):
    prev_data = ''
    while True:
        time.sleep(1)
        try:
            openClipboard()
        except:
            print('OpenClipboard() failed')
            continue
        
        try:
            try:
                data = getClipboardData()
                if data and data != prev_data:
                    open(clipboard_file, 'w').write(data)
                    print('writing %s to file' % data)
                    prev_data = data
            except Exception as e:
                print(e)
                pass
        finally:
            closeClipboard()
        
        try:
            data = open(clipboard_file, 'r').read()
            if data != prev_data:
                setClipboardData(data)
                print('putting %s in clipboard' % data)
                prev_data = data
        except Exception as e:
            print(e)
            pass

def main():
    usage = """
    Usage: python SharedClipboard.py <filename>
    The filename should refer to a writable existing file. The file
    should be on a shared location visible and writable to all the
    shared clipboard instances on all machines.
    """

    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print(usage)
        sys.exit(1)

    clipboard_file = sys.argv[1]
    monitorClipboard(clipboard_file)

if __name__ == '__main__':
    main()
