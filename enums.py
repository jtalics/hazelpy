from enum import Enum


class Kind(Enum):
    RAWSOCK = 1
    WEBSOCK = 2
    REST = 3


class Mode(Enum):
    SERVER = 1
    CLIENT = 2


