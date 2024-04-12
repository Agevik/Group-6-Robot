import tkinter as tk
import socket

def send_command(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to EV3 robot; replace 'ev3dev.local' with the IP address if needed
            sock.connect(('192.168.0.1', 8080))
            sock.sendall(command.encode('utf-8'))
            print("Sent command:", command)
    except ConnectionError as e:
        print("Failed to send command:", e)

# Create the main window
window = tk.Tk()
window.title("EV3 Robot Controller")

# Create and place buttons
btn_forward = tk.Button(window, text="Pick up", command=lambda: send_command("pick"))
btn_forward.pack(pady=5)

btn_backward = tk.Button(window, text="Release", command=lambda: send_command("release"))
btn_backward.pack(pady=5)

btn_stop = tk.Button(window, text="Stop", command=lambda: send_command("stop"))
btn_stop.pack(pady=5)

# Start the GUI event loop
window.mainloop()
