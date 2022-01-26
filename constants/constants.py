import types

# SERVER CONSTANTS
# Buffer size for incoming data (in bytes)
buffer_size = 1024
string_encoding = 'utf-8'

# PARSER CONSTANTS
class packet_type:
    def __init__(self, name, code):
        self.name = name
        self.code = code
packet_types = types.SimpleNamespace(
    play=packet_type('play', 0),
    now_playing=packet_type('now_playing', 1),
    game_data=packet_type('game_data', 2),
    end_game=packet_type('end_game', 3),
)
byteorder = 'big'
# Packet section sizes in bytes
header_length = 1
buffer_length = 1
# 108 for game fields and 4 for players' ids
player_id_length = 2
opponent_id_length = 2
data_length = 108
packet_length = header_length + buffer_length + player_id_length + opponent_id_length + data_length

# GAME AND PARSER CONTSTANTS
# no_of_rows and no_of_columns need to be multiples o 2
no_of_rows = 12
no_of_columns = 18
