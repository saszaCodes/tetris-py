import constants
# TUTAJ DODAĆ (tzn. w całym pliku) komentarze, żeby było wiadomo co się dzieje

# TUTAJ DODAĆ jeszcze sprawdzenie, że player_id i opponent_id nie są takie same
# Class creating a tdp packet. Its main purpose is to validate data in the packet to avoid bugs.
# It doesn't let one create a new packet unless passed arguments are
# string, int, int and a list of lists containing Cell_State objects respectively
class tdp_packet:
    def __init__(self, type, player_id, opponent_id, data):
        self._type = None
        self._player_id = None
        self._opponent_id = None
        self._data = None
        self.type = type
        self.player_id = player_id
        self.opponent_id = opponent_id
        self.data = data

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if type(value) != str:
            raise TypeError('type has to be a string')
            # CZY POWINNAM TU DODAĆ RETURN?
        valid_type = False
        for const in constants.packet_types.__dict__:
            # CZY TO JEST DOBRY SPOSÓB SPRAWDZENIA? BO SPRAWDZAM PO NAZWIE WŁASNOŚCI, A NIE PO JEJ ATRYBUCIE .NAME
            if value == const:
                valid_type = True
                break
        if not valid_type:
            raise ValueError('type has to be a name of one of the types specified in constants.packet_types')
            # PODOBNIE TUTAJ, CZY POWINNAM DODAĆ RETURN?
        self._type = value

    @property
    def player_id(self):
        return self._player_id

    @player_id.setter
    def player_id(self, value):
        if type(value) != int:
            raise TypeError('player_id has to be an integer')
            # CZY POWINNAM TU DODAĆ RETURN?
        max_int = 2**(constants.player_id_length*8)
        if value not in range(max_int):
            raise ValueError(f'player_id has to be a number between 0 and {max_int - 1}')
            # PODOBNIE TUTAJ, CZY POWINNAM DODAĆ RETURN?
        self._player_id = value

    @property
    def opponent_id(self):
        return self._opponent_id

    @opponent_id.setter
    def opponent_id(self, value):
        if type(value) != int:
            raise TypeError('opponent_id has to be an integer')
            # CZY POWINNAM TU DODAĆ RETURN?
        max_int = 2**(constants.player_id_length*8)
        if value not in range(max_int):
            raise ValueError(f'opponent_id has to be a number between 0 and {max_int - 1}')
            # PODOBNIE TUTAJ, CZY POWINNAM DODAĆ RETURN?
        self._opponent_id = value

    @property
    def data(self):
        return self._data

    @data.setter
    # TUTAJ DODAĆ setter dla data
    def data(self, value):
        self._data = value

# Class parsing bytes into tdp_packet objects and vice versa
class tdp_parser:
    # MOŻE DAŁOBY SIĘ ZROBIĆ PODZIAŁ NA PARSER SERWEROWY I KLIENCKI, ŻEBY SERWEROWY NIE MUSIAŁ
    # ODTWARZAĆ CAŁEJ WIADOMOŚCI?

    # TA METODA JEST CHYBA W OGÓLE NIEPOTRZEBNA
    @staticmethod
    def data_to_packet(data):
        return

    # TA METODA JEST CHYBA W OGÓLE NIEPOTRZEBNA
    @staticmethod
    def packet_to_data(packet):
        # PYTANIE TAKIE JAK W PACKET_TO_BYTES
        if not isinstance(packet, tdp_packet):
            error_message = 'Incorrect data type of packet. Use provided tdp_packet type.'
            raise TypeError(error_message)
        if type == constants.packet_types.play:
            return
        if type == constants.packet_types.now_playing:
            return
        if type == constants.packet_types.game_data:
            return
        if type == constants.packet_types.end_game:
            return

    @staticmethod
    def bytes_to_packet(provided_bytes):
        # ## Validate passed argument. If it is not of type bytearray or it is a bytearray but
        # ## its length doesn't match expected tdp packet length, throw an error
        if not isinstance(provided_bytes, bytearray):
            raise TypeError('provided_bytes has to be a bytearray object')
            # CZY TU POWINNO BYĆ RETURN?
        elif provided_bytes.__len__() != constants.packet_length:
            raise ValueError(f'provided_bytes length is incorrect; it should be {constants.packet_length}')
            # CZY TU POWINNO BYĆ RETURN?
        else:
            # TUTAJ POPRAWIĆ sprawdzanie (w constants powinien być two-way dictionary albo coś)
            # ## Split received bytearray into individual variables corresponding to the fields of a tdp packet
            code_bytes = provided_bytes[:constants.header_length]
            del provided_bytes[:constants.header_length]
            del provided_bytes[:constants.buffer_length]
            player_id_bytes = provided_bytes[:constants.player_id_length]
            del provided_bytes[:constants.player_id_length]
            opponent_id_bytes = provided_bytes[:constants.opponent_id_length]
            del provided_bytes[:constants.opponent_id_length]
            data_bytes = provided_bytes[:]
            del provided_bytes[:]
            # ## Parse packet code
            code_int = int.from_bytes(code_bytes, constants.byteorder)
            # CZY TU POWINNAM WYWALAĆ ERROR JEŚLI NIE MA TEGO W ZDEFINIOWANYCH TYPACH? PEWNIE TAK
            for const in constants.packet_types.__dict__:
                if constants.packet_types.__dict__[const].code == code_int:
                    type_str = constants.packet_types.__dict__[const].name
            # ## Parse player_id and opponent_id
            player_id_int = int.from_bytes(player_id_bytes, constants.byteorder)
            opponent_id_int = int.from_bytes(opponent_id_bytes, constants.byteorder)
            # ## Parse data
            # TUTAJ DODAĆ parsowanie danych w odpowiedni sposób, teraz placeholder
            data_int = int.from_bytes(data_bytes, constants.byteorder)
            # ## Create a new tdp_packet using parsed data
            return tdp_packet(type_str, player_id_int, opponent_id_int, data_int)

    # CZY PAKIET W OGÓLE POWINIEN ZAWIERAĆ OPPONENT ID?
    # CHYBA NIE, LEPIEJ ŻEBY SERWER DECYDOWAŁ Z KIM GRACZ GRA NA PODSTAWIE JEGO ID I TYLE
    @staticmethod
    def packet_to_bytes(packet):
        # CZY POTRZEBA SPRAWDZAĆ, ŻE PAKIET MA WSZYSTKIE ATRYBUTY? CHĘTNIE BYM ZAŁOŻYŁA, ŻE SKORO KLASA WYMAGA PODANIA ARGUMENTÓW DLA WSZYSTKICH ATRYBUTÓW PRZY TWORZENIU OBIEKTU, TO WYSTARCZY
        # ## Validate passed argument. If its type is a tdp_packet object, throw an error
        if not isinstance(packet, tdp_packet):
            error_message = 'Incorrect data type of packet. Use provided tdp_packet type.'
            raise TypeError(error_message)
            # CZY TO POWINNAM DAĆ RETURN?
        # ## If packet's type is 'play', look up its type's code and parse it to bytes.
        # ## Fill other fields of the packet with 0s (they are irrelevant for this type)
        elif packet.type == constants.packet_types.play.name:
            code_int = constants.packet_types.play.code
            code_bytes = int.to_bytes(code_int, constants.header_length, constants.byteorder)
            buffer_bytes = int.to_bytes(0, constants.buffer_length, constants.byteorder)
            # This type of packet needs no user ids and no data, so fill the data with 0
            other_bytes = int.to_bytes(0,
                                       constants.player_id_length + constants.opponent_id_length + constants.data_length,
                                       constants.byteorder)
            packet = code_bytes + buffer_bytes + other_bytes
            return packet
        # ## If packet's type is 'now_playing', look up its type's code and parse it to bytes.
        # ## Parse player_id and opponent_id to bytes. Fill other fields with 0s
        elif packet.type == constants.packet_types.now_playing.name:
            code_int = constants.packet_types.now_playing.code
            code_bytes = int.to_bytes(code_int, constants.header_length, constants.byteorder)
            buffer_bytes = int.to_bytes(0, constants.buffer_length, constants.byteorder)
            player_id_int = packet.player_id
            opponent_id_int = packet.opponent_id
            player_id_bytes = int.to_bytes(player_id_int, constants.player_id_length, constants.byteorder)
            opponent_id_bytes = int.to_bytes(opponent_id_int, constants.opponent_id_length, constants.byteorder)
            data_bytes = int.to_bytes(0, constants.data_length, constants.byteorder)
            packet = code_bytes + buffer_bytes + player_id_bytes + opponent_id_bytes + data_bytes
            return packet
        # TUTAJ DODAĆ parsowanie game data
        elif packet.type == constants.packet_types.game_data.name:
            return
        # ## If packet's type is 'end_game', look up its type's code and parse it to bytes.
        # ## Parse player_id and opponent_id to bytes. Fill other fields with 0s
        elif packet.type == constants.packet_types.end_game.name:
            code_int = constants.packet_types.end_game.code
            code_bytes = int.to_bytes(code_int, constants.header_length, constants.byteorder)
            buffer_bytes = int.to_bytes(0, constants.buffer_length, constants.byteorder)
            player_id_int = packet.player_id
            opponent_id_int = packet.opponent_id
            player_id_bytes = int.to_bytes(player_id_int, constants.player_id_length, constants.byteorder)
            opponent_id_bytes = int.to_bytes(opponent_id_int, constants.opponent_id_length, constants.byteorder)
            data_bytes = int.to_bytes(0, constants.data_length, constants.byteorder)
            packet = code_bytes + buffer_bytes + player_id_bytes + opponent_id_bytes + data_bytes
            return packet
