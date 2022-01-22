from tdp_protocol.socket_handler import tdp_socket_handler
from tdp_protocol.parser import tdp_packet


# print(constants.packet_types)
#
#
# messages = ['how', 'are', 'u']
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# for message in messages:
#     bytes = message.encode(constants.string_encoding)
#     sock.sendto(bytes, ('127.0.0.1', 20000))

class tetris_client(tdp_socket_handler):
    def __init__(self, host, port):
        super().__init__(host, port)

    def handle_incoming(self, packet, address):
        print(f'Received from {address}: {packet}')

    def handle_outgoing(self):
        # TUTAJ BĘDZIE czekanie aż coś się pojawi w buforze zamiast user inputu, to tylko dla sprawdzenia
        type_input = input('Packet type: ')
        user_id_input = int(input('user_id: '))
        opponent_id_input = int(input('opponent_id: '))
        data_input = int(input('data: '))
        packet = tdp_packet(type_input, user_id_input, opponent_id_input, data_input)
        return packet, ('127.0.0.1', 20000)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# client = tetris_client('127.0.0.1', 30000)
# client.start_client()
