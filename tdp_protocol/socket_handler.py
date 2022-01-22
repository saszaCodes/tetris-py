import socket
import threading
from constants import constants
from tdp_protocol.parser import tdp_parser


# CZY NIE POWINNO BYĆ JEDNAK TAK, ŻE SERWER PRZYPISUJE PO WĄTKU KAŻDEMU ADRESOWI ("POŁĄCZENIU")?
# Parent class, no objects should be created directly from it. Instead, create a child class
# and implement handle_incoming and handle_outgoing methods.
# The class runs two threads.
# On one of them, it listens for incoming bytes, parses them udp packets and passes them to handle_incoming method.
# On the other one, it waits until handle_outgoing (which is expected to be blocking) returns data and address,
# parses the data (expected type: tdp_packet) into bytes and sends them to a returned address (expected type: tuple)
class tdp_socket_handler:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        print(f'Starting server on port {port}')
        self.listening_thread = threading.Thread(group=None, target=self.listen)
        self.sending_thread = threading.Thread(group=None, target=self.send)

    # CZY TAKIE DWIE METODY SĄ LEGIT? BO W SUMIE SERWER I KLIENT POWINNY NA POZIOMIE
    # SŁUCHANIA / WYSYŁANIA DZIAŁAĆ PRAKTYCZNIE TAK SAMO, JEDYNIE RÓŻNI JE TO, ŻE KLIENT NIE POTRZEBUJE BIND
    def start_server(self):
        self.listening_thread.start()
        self.sending_thread.start()

    def start_client(self):
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
                packet = tdp_parser.bytes_to_packet(packet_bytes)
                # Tutaj bez implementacji wielowątkowości, to się będzie działo w klasie-dziecku,
                # jeśli ona sobie nie zaimplementuje podziału na wątki, to będzie mieć problem,
                # gdy ktoś będzie złośliwie wysyłać bardzo dużo danych
                self.handle_incoming(packet, address)

    def send(self):
        while True:
            # This is expected to be blocking
            not_parsed_data, address = self.handle_outgoing()
            # TUTAJ DODAĆ walidację?
            bytes = tdp_parser.packet_to_bytes(not_parsed_data)
            while bytes.__len__() > 0:
                bytes_sent = self.sock.sendto(bytes, address)
                bytes = bytes[bytes_sent:]

    def handle_incoming(self):
        raise NotImplementedError("You have to override handle_data in a child class.")

    def handle_outgoing(self):
        raise NotImplementedError("You have to override handle_outgoing in a child class.")


