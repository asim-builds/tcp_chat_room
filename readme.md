# TCP Chat Room

A simple multi-user TCP chat room with both **command-line** and **GUI** clients, built in Python.

---

## Features

- Multiple clients can join and chat in real time.
- Each user has a unique username (randomly assigned if left blank).
- GUI client with modern look (Tkinter).
- System messages for user join/leave events.
- Shows "People in this room" to new joiners.
- Timestamps for all messages.
- Sent messages appear as "You: ..." in your own chat window.

---

## Getting Started

### 1. Clone or Download

Download or clone this repository to your computer.

### 2. Requirements

- Python 3.7+
- No external dependencies (Tkinter is included with standard Python on Windows).

### 3. Run the Server

Open a terminal and run:

```
python server.py
```

### 4. Run the Client

You can use either the CLI or GUI client.

#### Command-Line Client

```
python client.py
```

#### GUI Client

```
python client_gui.py
```

You can run multiple clients (in separate terminals or by launching the GUI multiple times) to simulate a chat room.

---

## How It Works

- **Usernames:**  
  On startup, each client is prompted for a username. If left blank, a random one is assigned.
- **Messaging:**  
  Messages you send appear as `You: ...` in your window. Other users see your username.
- **User List:**  
  When you join, you see a list of users already in the room.
- **System Messages:**  
  Join/leave events are shown in a highlighted style.

---

## Customization

- **Colors and Fonts:**  
  You can adjust the color scheme and fonts in `client_gui.py` by editing the constants at the top of the file.
- **Random Usernames:**  
  Add or change the random usernames in the `RANDOM_USERNAMES` list.

---

## Troubleshooting

- If the GUI does not appear, ensure you are running Python with Tkinter support.

---

## License

This project is for educational purposes. Feel free to use and modify!

---