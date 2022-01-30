from constants import constants
from tdp_protocol.parser import common


def _bytes_to_data(received_bytes):
    data_list = []
    for row_index in range(0, constants.no_of_rows):
        row_ints = []
        for column_index in range(int(constants.no_of_columns / 2)):
            index_one_dimension = row_index * int(constants.no_of_columns / 2) + column_index
            # CZEMU TO MI AUTOMATYCZNIE ROBI INT Z BAJTÓW W BYTEARRAY?
            encoded_fields_int = received_bytes[index_one_dimension]
            field_1 = encoded_fields_int % 16
            field_2 = encoded_fields_int // 16
            row_ints.extend((field_1, field_2))
        data_list.append(row_ints)
    return data_list


def _data_to_bytes(data):
    data_bytes = bytes()
    for row in data:
        for column_index in range(0, constants.no_of_columns, 2):
            field_1 = row[column_index]
            field_2 = row[column_index + 1]
            encoded_fields_int = field_1 + field_2 * 16
            encoded_fields_byte = encoded_fields_int.to_bytes(1, byteorder=constants.byteorder)
            data_bytes += encoded_fields_byte
    return data_bytes


def bytes_to_packet(provided_bytes):
    # ## Validate passed argument. If it is not of type bytearray or it is a bytearray but
    # ## its length doesn't match expected tdp packet length, throw an error
    if not isinstance(provided_bytes, bytearray):
        raise TypeError('provided_bytes has to be a bytearray object')
    elif len(provided_bytes) != constants.packet_length:
        raise ValueError(f'provided_bytes length is incorrect; it should be {constants.packet_length}')
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
        code_int = common.bytes_to_code(code_bytes)
        # ZMIENIĆ W CONSTANTS NA SŁOWNIK
        for const in constants.packet_types.__dict__:
            if constants.packet_types.__dict__[const].code == code_int:
                type_str = constants.packet_types.__dict__[const].name
        # ## Parse player_id and opponent_id
        player_id_int = common.bytes_to_player_id(player_id_bytes)
        opponent_id_int = common.bytes_to_opponent_id(opponent_id_bytes)
        # ## Parse data
        # TUTAJ DODAĆ wyjaśnienie co się dzieje
        data_list = _bytes_to_data(data_bytes)
        # ## Create a new tdp_packet using parsed data
        return common.tdp_packet(type_str, player_id_int, opponent_id_int, data_list)


def packet_to_bytes(packet):
    # OPAKOWAĆ W TRY EXCEPT w razie gdyby nie było jakiejś property
    # ## Validate passed argument. If its type is a tdp_packet object, throw an error
    if not isinstance(packet, common.tdp_packet):
        error_message = 'Incorrect data type of packet. Use provided tdp_packet type.'
        raise TypeError(error_message)
    code_bytes = common.code_to_bytes(packet.code)
    if packet.type == constants.packet_types.play.name:
        other_bytes = int.to_bytes(0, constants.packet_length - constants.header_length)
        return code_bytes + other_bytes
    buffer_bytes = int.to_bytes(0, constants.buffer_length, constants.byteorder)
    player_id_bytes = common.player_id_to_bytes(packet.player_id)
    opponent_id_bytes = common.opponent_id_to_bytes(packet.opponent_id)
    if packet.type in (constants.packet_types.now_playing.name, constants.packet_types.end_game.name):
        other_bytes = int.to_bytes(0, constants.data_length)
        return code_bytes + player_id_bytes + buffer_bytes + opponent_id_bytes + other_bytes
    data_bytes = _data_to_bytes(packet.data)
    return code_bytes + player_id_bytes + buffer_bytes + opponent_id_bytes + data_bytes

    # # ## If packet's type is 'play', look up its type's code and parse it to bytes.
    # # ## Fill other fields of the packet with 0s (they are irrelevant for this type)
    # elif packet.type == constants.packet_types.play.name:
    #     code_int = constants.packet_types.play.code
    #     code_bytes = int.to_bytes(code_int, constants.header_length, constants.byteorder)
    #     buffer_bytes = int.to_bytes(0, constants.buffer_length, constants.byteorder)
    #     # This type of packet needs no user ids and no data, so fill the data with 0
    #     other_bytes = int.to_bytes(0,
    #                                constants.player_id_length + constants.opponent_id_length + constants.data_length,
    #                                constants.byteorder)
    #     packet = code_bytes + buffer_bytes + other_bytes
    #     return packet
    # # ## If packet's type is 'now_playing', look up its type's code and parse it to bytes.
    # # ## Parse player_id and opponent_id to bytes. Fill other fields with 0s
    # elif packet.type == constants.packet_types.now_playing.name:
    #     code_int = constants.packet_types.now_playing.code
    #     code_bytes = int.to_bytes(code_int, constants.header_length, constants.byteorder)
    #     buffer_bytes = int.to_bytes(0, constants.buffer_length, constants.byteorder)
    #     player_id_int = packet.player_id
    #     opponent_id_int = packet.opponent_id
    #     player_id_bytes = int.to_bytes(player_id_int, constants.player_id_length, constants.byteorder)
    #     opponent_id_bytes = int.to_bytes(opponent_id_int, constants.opponent_id_length, constants.byteorder)
    #     data_bytes = int.to_bytes(0, constants.data_length, constants.byteorder)
    #     packet = code_bytes + buffer_bytes + player_id_bytes + opponent_id_bytes + data_bytes
    #     return packet
    # # TUTAJ DODAĆ wyjaśnienie co się dzieje
    # elif packet.type == constants.packet_types.game_data.name:
    #     code_int = constants.packet_types.now_playing.code
    #     code_bytes = int.to_bytes(code_int, constants.header_length, constants.byteorder)
    #     buffer_bytes = int.to_bytes(0, constants.buffer_length, constants.byteorder)
    #     player_id_int = packet.player_id
    #     opponent_id_int = packet.opponent_id
    #     player_id_bytes = int.to_bytes(player_id_int, constants.player_id_length, constants.byteorder)
    #     opponent_id_bytes = int.to_bytes(opponent_id_int, constants.opponent_id_length, constants.byteorder)
    #     # samo w zaleźności od tego ile bitów zajmują dane o 1 polu (powinno być zdefiniowane w constants)
    #     data_bytes = bytes()
    #     for row in packet.data:
    #         for column_index in range(0, constants.no_of_columns, 2):
    #             field_1 = row[column_index]
    #             field_2 = row[column_index + 1]
    #             encoded_fields_int = field_1 + field_2 * 16
    #             encoded_fields_byte = encoded_fields_int.to_bytes(1, byteorder=constants.byteorder)
    #             data_bytes += encoded_fields_byte
    #     packet = code_bytes + buffer_bytes + player_id_bytes + opponent_id_bytes + data_bytes
    #     return packet
    # # ## If packet's type is 'end_game', look up its type's code and parse it to bytes.
    # # ## Parse player_id and opponent_id to bytes. Fill other fields with 0s
    # elif packet.type == constants.packet_types.end_game.name:
    #     code_int = constants.packet_types.end_game.code
    #     code_bytes = int.to_bytes(code_int, constants.header_length, constants.byteorder)
    #     buffer_bytes = int.to_bytes(0, constants.buffer_length, constants.byteorder)
    #     player_id_int = packet.player_id
    #     opponent_id_int = packet.opponent_id
    #     player_id_bytes = int.to_bytes(player_id_int, constants.player_id_length, constants.byteorder)
    #     opponent_id_bytes = int.to_bytes(opponent_id_int, constants.opponent_id_length, constants.byteorder)
    #     data_bytes = int.to_bytes(0, constants.data_length, constants.byteorder)
    #     packet = code_bytes + buffer_bytes + player_id_bytes + opponent_id_bytes + data_bytes
    #     return packet