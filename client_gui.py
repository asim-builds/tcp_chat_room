import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, font
import random

HOST = '127.0.0.1'
PORT = 65432

BG_COLOR = "#222831"
CHAT_AREA_BG = "#31363b"    # Improved chat area color
TEXT_COLOR = "#eeeeee"
ENTRY_BG = "#f5f6fa"        # Lighter white for entry box
BUTTON_BG = "#00adb5"
BUTTON_FG = "#ffffff"
SYSTEM_MSG_COLOR = "#ffd369"
USER_MSG_COLOR = "#eeeeee"
FONT_FAMILY = "Segoe UI"

RANDOM_USERNAMES = [
    "BlueTiger", "GreenLeaf", "RedFox", "SilverWolf", "GoldenEagle",
    "NightOwl", "SwiftFalcon", "MightyBear", "SilentShadow", "LuckyStar"
]

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("TCP Chat Room")
        self.master.configure(bg=BG_COLOR)
        self.master.resizable(False, False)

        # Header
        header = tk.Label(master, text="TCP Chat Room", bg=BG_COLOR, fg=BUTTON_BG,
                          font=(FONT_FAMILY, 18, "bold"), pady=10)
        header.pack(fill=tk.X)

        # Chat area
        self.text_area = scrolledtext.ScrolledText(
            master, state='disabled', width=50, height=20, bg=CHAT_AREA_BG, fg=TEXT_COLOR,
            font=(FONT_FAMILY, 11), wrap=tk.WORD, bd=0, padx=10, pady=10
        )
        self.text_area.pack(padx=10, pady=(0,10))

        # Bottom frame for entry and button
        bottom_frame = tk.Frame(master, bg=BG_COLOR)
        bottom_frame.pack(fill=tk.X, padx=10, pady=(0,10))

        self.entry = tk.Entry(bottom_frame, width=40, bg=ENTRY_BG, fg="#222831",
                              font=(FONT_FAMILY, 11), insertbackground="#222831", bd=0)
        self.entry.pack(side=tk.LEFT, padx=(0,10), pady=0, ipady=6, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(bottom_frame, text="Send", command=self.send_message,
                                     bg=BUTTON_BG, fg=BUTTON_FG, font=(FONT_FAMILY, 11, "bold"),
                                     activebackground=SYSTEM_MSG_COLOR, activeforeground=BG_COLOR, bd=0, padx=16, pady=6)
        self.send_button.pack(side=tk.LEFT)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            master.destroy()
            return

        # Hide window before username dialog to avoid flicker, then restore after
        self.master.withdraw()
        username = simpledialog.askstring("Username", "Enter your username:", parent=master)
        if not username:
            username = random.choice(RANDOM_USERNAMES)
            messagebox.showwarning(
                "No Username Entered",
                f"Since you have entered no username, '{username}' has been assigned to you."
            )
        self.username = username
        self.sock.sendall(self.username.encode())
        self.master.deiconify()  # Restore window after dialog

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                msg = self.sock.recv(1024)
                if not msg:
                    break
                decoded = msg.decode()
                self.text_area.config(state='normal')
                # Color system messages
                if decoded.startswith("***"):
                    self.text_area.insert(tk.END, decoded + "\n", "system")
                else:
                    self.text_area.insert(tk.END, decoded + "\n", "user")
                self.text_area.yview(tk.END)
                self.text_area.config(state='disabled')
                # Tag config for colors
                self.text_area.tag_config("system", foreground=SYSTEM_MSG_COLOR, font=(FONT_FAMILY, 11, "italic"))
                self.text_area.tag_config("user", foreground=USER_MSG_COLOR, font=(FONT_FAMILY, 11))
            except:
                break

    # def send_message(self, event=None):
    #     message = self.entry.get()
    #     if message:
    #         self.sock.sendall(message.encode())
    #         self.entry.delete(0, tk.END)

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            # Show in sender's chat area as "You: ..."
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"You: {message}\n", "self")
            self.text_area.yview(tk.END)
            self.text_area.config(state='disabled')
            self.text_area.tag_config("self", foreground="#7fffd4", font=(FONT_FAMILY, 11, "bold"))
            self.sock.sendall(message.encode())
            self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()