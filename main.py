from argparse import ArgumentParser, Namespace
from enum import Enum

from enums import Kind, Mode
from rawsock import rawsockKind
from rest import restKind
from websock import websockKind
from fastapi import FastAPI

def parseArgs() -> ():
    # https://docs.python.org/3/howto/argparse.html
    mode: Enum
    parser : ArgumentParser = ArgumentParser()
    parser.add_argument('kind',help='<RAWSOCK|WEBSOCK|REST>')
    parser.add_argument('mode',help='<SERVER|CLIENT>')
    parser.add_argument('host',help='network name of server host')
    parser.add_argument('port',type=int,help='network port of server host')
    parser.add_argument('name',help='user-supplied name')
    args: Namespace = parser.parse_args()
    print("Starting",args.kind,args.mode,args.name,"at",args.host,args.port)
    return (args.kind,args.mode,args.host,args.port,args.name)


if __name__ == '__main__':
    args=parseArgs()
    a = Kind[args[0]]
    b = Mode[args[1]]
    args = (a, b, args[2], args[3], args[4])
    match args[0]:
        case Kind.RAWSOCK:
            rawsockKind(args)
        case Kind.WEBSOCK:
            websockKind(args)
        case Kind.REST:
            restKind()
    print('N O R M A L   C O M P L E T I O N')
# EOF
