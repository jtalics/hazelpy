
import asyncio
import signal,string,threading,time
import sys
from types import FrameType

from websockets import serve, connect, WebSocketClientProtocol, ConnectionClosedOK, ConnectionClosedError

from enums import Mode

serverSocket: any
stop: bool = False

async def handleClient(clientSocket, unused) -> None:
    while not stop:
        try:
            data = await clientSocket.recv()
            print('Received: ', data)
            echo = b'Echo: {data}'
            await clientSocket.send(echo)
        except ConnectionClosedOK:
            print('Server closed connection OK')
        except ConnectionClosedError:
            print('Server closed connection with error')
    await clientSocket.close()
    print("Client closed connection.")


def shutdown(number: int, frame: FrameType) -> None:
    print(signal.Signals(number), "received; stopping")
    global stop
    stop = True
    serverSocket.close()
    #sys.exit(0)
    #print(frame)


async def runClient(host,port,stop) -> WebSocketClientProtocol:
    uri: string = f'ws://{host}:{port}'
    print('Connecting to server websocket at',uri)
    global serverSocket
    async with connect(uri) as serverSocket:  # blocks
        for i in range(30):
            if stop:
                await serverSocket.close()
                break
            req = bytes("Request #" + str(i), 'ascii')
            print('Sending',req)
            await serverSocket.send(req)
            try:
                data: string = await serverSocket.recv()
                print('Received from server:', data)
            except ConnectionClosedOK:
                print("Connection to server closed OK.")
                break
            except ConnectionClosedError:
                print("Connection to server closed with error.")
                break
            if i > 30:
                print('Complete')
                break
            time.sleep(5)
    return serverSocket


def runServer(host,port) -> WebSocketClientProtocol:
    global serverSocket
    while not stop:
        serverSocket=serve(handleClient, host, port)
    return serverSocket.


def serverMode(args: ()) -> None:
    # https://websockets.readthedocs.io/en/9.0.1/deployment.html
    # loop = asyncio.get_event_loop()
    # stop = loop.create_future()
    # add_signal_handlers not implemented by Windows python because
    # Windows does not use signals
    # loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    # loop.add_signal_handler(signal.SIGINT, stop.set_result, None)
    # loop.add_signal_handler(signal.SIGABRT, stop.set_result, None)

    (kind, mode, host, port, name) = args
    runServer(host,port)


def clientMode(args: ()) -> None:
    # https://websockets.readthedocs.io/en/stable/reference/client.html
    loop = asyncio.get_event_loop()
    stop = loop.create_future()
    # add_signal_handlers not implemented by Windows python because
    # Windows does not use signals
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    loop.add_signal_handler(signal.SIGINT, stop.set_result, None)
    loop.add_signal_handler(signal.SIGABRT, stop.set_result, None)

    (kind, mode, host, port, name) = args
    loop.run_until_complete(runClient(host,port,stop))


def setSignals() -> None:
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGABRT, shutdown)


def websockKind(args: ()) -> None:
    setSignals()
    (kind, mode, host, port, name) = args
    match mode:
        case Mode.SERVER:
            serverMode(args)
        case Mode.CLIENT:
            clientMode(args)


#EOF