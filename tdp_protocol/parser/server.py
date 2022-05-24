from constants import constants
from tdp_protocol.parser import common


class tdp_metadata:
    def __init__(self, type, player_id, opponent_id, undecoded_data):
        self.type = type
        self.player_id = player_id
        self.opponent_id = opponent_id
        self.undecoded_data = undecoded_data


def bytes_to_metadata(provided_bytes):
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
    packet_types = constants.packet_types
    for key in packet_types:
        if packet_types[key].code == code_int:
            type_str = packet_types[key].name
    # ## Parse player_id and opponent_id
    player_id_int = common.bytes_to_player_id(player_id_bytes)
    opponent_id_int = common.bytes_to_opponent_id(opponent_id_bytes)
    return tdp_metadata(type_str, player_id_int, opponent_id_int, data_bytes)


def metadata_to_bytes(metadata):
    if not isinstance(metadata, tdp_metadata):
        error_message = 'Incorrect data type of packet. Use provided tdp_metadata type.'
        raise TypeError(error_message)
    metadata_code = constants.packet_types[metadata.type].code
    code_bytes = common.code_to_bytes(metadata_code)
    buffer_bytes = int.to_bytes(0, constants.buffer_length, constants.byteorder)
    player_id_bytes = common.player_id_to_bytes(metadata.player_id)
    opponent_id_bytes = common.opponent_id_to_bytes(metadata.opponent_id)
    return code_bytes + player_id_bytes + buffer_bytes + opponent_id_bytes + metadata.undecoded_data
