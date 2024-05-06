import socket
import threading
from queue import Queue
from colorama import init, Fore
import os

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
    for x in range(N_THREADS):
        t = threading.Thread(target=threader, args=(host,))
        t.daemon = True
        t.start()

    for port in range(1, 1025):
        q.put(port)

    q.join()


def saving_file(host, open_ports, catalog):
    dir = os.path.join(catalog, f"{host}_port.txt")
    with open(dir, 'w') as f:
        f.write(f"Open ports for {host}: \n")
        for host, port in open_ports:
            f.write(f"{host}:{port} \n")
    return dir


if __name__ == '__main__':
    host = input("Enter the host: ")
    main(host)
    saved_file = saving_file(host, open_ports, catalog=os.getcwd())
    print("Scan results saved in:", saved_file)
