
import socket
import time
import threading
from tkinter import Tk, Label, Button, Entry, Text, Scrollbar, END, messagebox

def scan_port(host, port):
    """Fonction qui scanne un seul port"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result == 0
    except socket.error:
        return False

def scan_ports(host, start_port, end_port, output_text):
    """Fonction qui sacnne une plage de ports"""
    output_text.insert(END, f"Scanning ports {start_port}-{end_port} on {host}...\n")
    open_ports = []

    def scan_and_log(port):
        if scan_port(host, port):
            open_ports.append(port)
            output_text.insert(END, f"Port {port} is OPEN\n")
        else:
            output_text.insert(END, f"Port {port} is CLOSED\n")

    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_and_log, args=(port,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output_text.insert(END, f"\nScan completed. Open ports: {open_ports}\n")
    return open_ports

def close_ports(start_port, end_port, output_text):
    """Function to simulate closing ports."""
    output_text.insert(END, f"Closing ports {start_port}-{end_port}... (Simulation)\n")
    for port in range(start_port, end_port + 1):
        if port not in range(20, 25):  # Simulation de fermeture de ports 
            output_text.insert(END, f"Port {port} is now CLOSED (simulated).\n")
        else:
            output_text.insert(END, f"Port {port} remains OPEN (simulated).\n")

def start_scan():
    try:
        host = host_entry.get()
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
        output_text.delete(1.0, END)
        threading.Thread(target=scan_ports, args=(host, start_port, end_port, output_text)).start()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid port numbers.")

def start_close_ports():
    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
        output_text.delete(1.0, END)
        threading.Thread(target=close_ports, args=(start_port, end_port, output_text)).start()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid port numbers.")

# UI Setup
app = Tk()
app.title("Port Scanner")

Label(app, text="Host:").grid(row=0, column=0, padx=5, pady=5)
host_entry = Entry(app)
host_entry.grid(row=0, column=1, padx=5, pady=5)
host_entry.insert(0, "127.0.0.1")

Label(app, text="Start Port:").grid(row=1, column=0, padx=5, pady=5)
start_port_entry = Entry(app)
start_port_entry.grid(row=1, column=1, padx=5, pady=5)
start_port_entry.insert(0, "1")

Label(app, text="End Port:").grid(row=2, column=0, padx=5, pady=5)
end_port_entry = Entry(app)
end_port_entry.grid(row=2, column=1, padx=5, pady=5)
end_port_entry.insert(0, "1024")

Button(app, text="Scan Ports", command=start_scan).grid(row=3, column=0, padx=5, pady=5)
Button(app, text="Close Ports", command=start_close_ports).grid(row=3, column=1, padx=5, pady=5)

output_text = Text(app, wrap="word", height=20, width=50)
output_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

scrollbar = Scrollbar(app, command=output_text.yview)
scrollbar.grid(row=4, column=2, sticky="ns")
output_text["yscrollcommand"] = scrollbar.set

app.mainloop()