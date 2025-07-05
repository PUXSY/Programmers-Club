import sys
import threading
from SYNrequest import SYNrequest

def get_request_from_args(args):
    if len(args) <= 1:
        print("Usage: python main.py <url>")
        return None
    return SYNrequest(args[1])

def set_url():
    while True:
        print("Enter a URL (e.g., http://example.com or https://example.com)\nor type 'exit' to quit")
        url = input("URL ?> ").strip()
        if url.lower() == 'exit':
            print("Exiting...")
            return None
        return SYNrequest(url)

def send_request(request_obj):
    try:
        while True:
            thread = threading.Thread(target=request_obj.send)
            thread.start()
            thread.join()
    except KeyboardInterrupt:
        print("Stopped by user.")
    except Exception as e:
        print(f"Error: {e}")


    except Exception as e:
        print(f"Error: {e}")

def main():
    req = get_request_from_args(sys.argv)

    if req is None or not getattr(req, "url", None):
        req = set_url()
        if req is None:
            return  # User exited

    send_request(req)

if __name__ == "__main__":
    main()
