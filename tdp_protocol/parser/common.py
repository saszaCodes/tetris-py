from constants import constants


class tdp_packet:
    def __init__(self, type, player_id, opponent_id, data):
        self.type = type
        self.player_id = player_id
        self.opponent_id = opponent_id
        self.data = data


def bytes_to_code(received_bytes):
    return int.from_bytes(received_bytes, constants.byteorder)


def code_to_bytes(code):
    return int.to_bytes(code, constants.header_length, constants.byteorder)


def bytes_to_player_id(received_bytes):
    return int.from_bytes(received_bytes, constants.byteorder)


def player_id_to_bytes(id):
    return int.to_bytes(id, constants.player_id_length, constants.byteorder)


def bytes_to_opponent_id(received_bytes):
    return int.from_bytes(received_bytes, constants.byteorder)


def opponent_id_to_bytes(id):
    return int.to_bytes(id, constants.opponent_id_length, constants.byteorder)
