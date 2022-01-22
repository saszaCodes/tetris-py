from tdp_protocol.socket_handler import tdp_socket_handler
from tdp_protocol.parser import tdp_packet


class tetris_server(tdp_socket_handler):
    def __init__(self, host, port):
        # CZEMU EDYTOR AUTOMATYCZNIE DODAJE ARGUMENTY tetris_server, self DO WYWOŁANIA SUPER()?
        super().__init__(host, port)

    # CZY TO JEST PROBLEM, ŻE O TYM NIE WSPOMINAM W NADKLASIE (ZOBACZ UWAGĘ JAKĄ DAJE EDYTOR DO NAZWY KLASY)?
    def handle_incoming(self, parsed_data, address):
        print(f'Received from {address}: {parsed_data}')

    def handle_outgoing(self):
        # TUTAJ BĘDZIE czekanie aż coś się pojawi w buforze zamiast user inputu, to tylko dla sprawdzenia
        type_input = input('Packet type: ')
        user_id_input = int(input('user_id: '))
        opponent_id_input = int(input('opponent_id: '))
        data_input = int(input('data: '))
        packet = tdp_packet(type_input, user_id_input, opponent_id_input, data_input)
        return packet, ('127.0.0.1', 30000)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

server = tetris_server('127.0.0.1', 20000)
server.start_server()
