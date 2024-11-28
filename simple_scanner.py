import socket
import threading
from queue import Queue
from colorama import init, Fore
import os
import argparse


init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX


N_THREADS = 200
q = Queue()
print_lock = threading.Lock()


open_ports = []


def port_scan(host, port):
    try:
        s = socket.socket()
        s.settimeout(1)  
        s.connect((host, port))
        with print_lock:
            print(f"{GREEN}{host:15}:{port:5} is open    {RESET}")
            open_ports.append((host, port))
    except:
        with print_lock:
            print(f"{GRAY}{host:15}:{port:5} is closed  {RESET}", end='\r')
    finally:
        s.close()


def threader(host):
    while True:
        port = q.get()
        port_scan(host, port)
        q.task_done()


def main(host):
    print(f"\nScanning host: {host}\n")
    for x in range(N_THREADS):
        t = threading.Thread(target=threader, args=(host,))
        t.daemon = True
        t.start()

    for port in range(1, 1025):
        q.put(port)

    q.join()


def saving_file(host, open_ports, catalog):
    if not os.path.exists(catalog):
        os.makedirs(catalog)
    dir = os.path.join(catalog, f"{host}_port.txt")
    with open(dir, 'w') as f:
        f.write(f"Open ports for {host}: \n")
        for host, port in open_ports:
            f.write(f"{host}:{port} \n")
    return dir


def detect_os():

    os_info = os.name
    if os_info == "nt":
        return "Windows"
    elif os_info == "posix":
        return "Linux/Unix"
    else:
        return "Unknown OS"


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument('-oS', action='store_true', help="Detect operating system")
    parser.add_argument('target', type=str, help="IP Address or hostname")
    args = parser.parse_args()


    if args.oS:
        os_info = detect_os()
        print(f"Detected operating system: {os_info}")

  
    main(args.target)

    saved_file = saving_file(args.target, open_ports, catalog=os.getcwd())
    print(f"\nScan results saved in: {saved_file}")
