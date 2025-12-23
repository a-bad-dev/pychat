import socket, _thread, time
from tkinter.simpledialog import askstring as ask

def main() -> None:
    ip   = input("enter server IP: ")
    port = int(input("enter server port: "  ) or 6667)
    
    name = input("enter your username: ") or "none"
    nick = input("enter your nick: "    ) or "user"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    time.sleep(5) # wait for server to be ready
    sock.send(f"USER {name} * * :{nick}\r\n".encode("utf-8"))

    time.sleep(1) # wait for server to process
    sock.send(f"NICK {nick}\r\n".encode("utf-8"))

    time.sleep(1) # wait for server to process

    _thread.start_new_thread(receive_messages, (sock,))

    while True:
        msg = ask("message to send", "enter a message to send:")
        if not msg or msg == "":
            break

        if msg.startswith("/nick"):
            nick = msg.split(" ")[1]
            msg = f"NICK {nick}"

        elif msg.startswith("/msg"):
            parts = msg.split(" ", 2)
            if len(parts) < 3:
                print("Usage: /msg <target> <message>")
                continue
            target, message = parts[1], parts[2]
            msg = f"PRIVMSG {target} :{message}"

        elif msg.startswith("/join"):
            channel = msg.split(" ")[1]
            msg = f"JOIN {channel}"
            current_channel = channel

        else:
            if "current_channel" not in locals():
                print("You must join a channel first using /join <channel>")
                continue
            msg = f"PRIVMSG {current_channel} :{msg}"

        sock.send((msg.strip() + "\r\n").encode("utf-8"))

def receive_messages(sock) -> None:
    while True:
        data = sock.recv(1024)
        if not data:
            break

        response = data.decode("utf-8")
        print(response)


if __name__ == "__main__":
    main()
