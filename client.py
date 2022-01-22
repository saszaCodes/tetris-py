import socket
from constants import constants

print(constants.packet_types)


messages = ['how', 'are', 'u']

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for message in messages:
    bytes = message.encode(constants.string_encoding)
    sock.sendto(bytes, ('127.0.0.1', 20000))

