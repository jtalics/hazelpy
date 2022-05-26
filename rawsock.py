import signal,socket,websockets,string,threading,time
from types import FrameType

from enums import Mode

serverSocket: socket
stop: bool = False


def setSignals() -> None:
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGABRT, shutdown)

def handleClient(clientSocket: socket) -> None:
    global stop
    while not stop:
        data: bytes = clientSocket.recv(1024)
        print('Received: ', data)
        if not data: break
        echo: bytes = b'Server echoes: ' + data
        clientSocket.sendall(echo)
    clientSocket.close()
    print("Client closed connection.")


def shutdown(number: int, frame: FrameType) -> None:
    global stop, serverSocket
    stop = True
    print(signal.Signals(number), "received; stopping")
    serverSocket.close()
    #print(frame)


def serverMode(args: (), serverSocket: socket) -> None:
    (kind, mode, host, port, name) = args
    print(f'Starting server {name}')
    serverSocket.bind((host, port))
    serverSocket.listen(5)  # blocks
    while not stop:
        try:
            print('Waiting for a connection')
            (clientsocket, address) = serverSocket.accept()
            print('Connected by ', address)
            ct = threading.Thread(target=handleClient(clientsocket), args=(1,))
            ct.start()
        except socket.error:
            pass
    return None


def clientMode(args: (), serverSocket) -> None:
    (kind, mode, host, port, name) = args
    print(f'Starting client {name}, waiting to connect')
    serverSocket.connect((host, port))  # blocks
    print('Connected.')
    i: int = 0
    global stop
    while not stop:
        req = bytes("Request #" + str(i), 'ascii')
        i += 1
        serverSocket.sendall(req)
        data = serverSocket.recv(1024)
        print('Received ' + str(data))
        if not data:
            print("Connection to server closed.")
            break
        if i > 30:
            print('Complete')
            break
        time.sleep(5)
    return None


def rawsockKind(args: ()) -> None:
    (kind, mode, host, port, name) = args
    setSignals()
    global serverSocket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    match mode:
        case Mode.SERVER:
            serverMode(args, serverSocket)
        case Mode.CLIENT:
            clientMode(args, serverSocket)


