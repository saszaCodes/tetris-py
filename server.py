import socket
import constants
import threading
from tdp_protocol.parser import parser, tdp_packet


# CZY NIE POWINNO BYĆ JEDNAK TAK, ŻE SERWER PRZYPISUJE PO WĄTKU KAŻDEMU ADRESOWI ("POŁĄCZENIU")?
class tdp_server:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        print(f'Starting server on port {port}')
        self.listening_thread = threading.Thread(group=None, target=self.listen)
        self.sending_thread = threading.Thread(group=None, target=self.send)

    def start(self):
        self.listening_thread.start()
        self.sending_thread.start()

    def listen(self):
        while True:
            data, address = self.sock.recvfrom(constants.buffer_size)
            # CZY TO JEST DOBRY SPOSÓB NA ZABEZPIECZENIE SIĘ PRZED NIEKOMPLETNYMI PAKIETAMI?
            # CO JEŚLI KLIENT ZACZNIE DZIWNIE WYSYŁAĆ?
            if data.__len__() % constants.packet_length != 0:
                continue
            bytes_array = bytearray(data)
            while bytes_array.__len__() > 0:
                packet_bytes = bytes_array[:constants.packet_length]
                del bytes_array[:constants.packet_length]
                packet = parser.bytes_to_packet(packet_bytes)
                # Tutaj bez implementacji wielowątkowości, to się będzie działo w klasie-dziecku,
                # jeśli ona sobie nie zaimplementuje podziału na wątki, to będzie mieć problem,
                # gdy ktoś będzie złośliwie wysyłać bardzo dużo danych
                self.handle_incoming(packet, address)

    def send(self):
        while True:
            # This is expected to be blocking
            not_parsed_data, address = self.handle_outgoing()
            # TUTAJ DODAĆ walidację?
            bytes = parser.packet_to_bytes(not_parsed_data)
            while bytes.__len__() > 0:
                bytes_sent = self.sock.sendto(bytes, address)
                bytes = bytes[bytes_sent:]

    def handle_incoming(self):
        raise NotImplementedError("You have to override handle_data in a child class.")

    def handle_outgoing(self):
        raise NotImplementedError("You have to override handle_outgoing in a child class.")


class tetris_server(tdp_server):
    def __init__(self, host, port):
        # CZEMU EDYTOR AUTOMATYCZNIE DODAJE ARGUMENTY tetris_server, self DO WYWOŁANIA SUPER()?
        super().__init__(host, port)

    # CZY TO JEST PROBLEM, ŻE O TYM NIE WSPOMINAM W NADKLASIE (ZOBACZ UWAGĘ JAKĄ DAJE EDYTOR DO NAZWY KLASY)?
    def handle_incoming(self, parsed_data, address):
        print(f'Received from {address}: {parsed_data}')

    def handle_outgoing(self):
        while True:
            # TUTAJ BĘDZIE czekanie aż coś się pojawi w buforze zamiast user inputu, to tylko dla sprawdzenia
            type_input = input('Packet type: ')
            user_id_input = int(input('user_id: '))
            opponent_id_input = int(input('opponent_id: '))
            data_input = int(input('data: '))
            packet = tdp_packet(type_input, user_id_input, opponent_id_input, data_input)
            return packet, ('127.0.0.1', 20000)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

server = tetris_server('127.0.0.1', 20000)
server.start()
