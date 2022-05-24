import random
random.seed()


def print_game_state_pretty():
    for (index, row) in enumerate(state):
        row_s = ""
        separator = "_____________________________________________________________"
        for column in row:
            row_s += f'{column}\t'
        print(row_s)
        if index == no_of_rows - 1:
            print(separator)


def convert(int1, int2):
    int_final = int1 + 16*int2
    print(f'Converted {int1}, {int2} to {int_final}')
    return int_final


def deconvert(int_final):
    int1 = int_final % 16
    int2 = int_final // 16
    print(f'Converted {int_final} to {int1}, {int2}')
    return int1, int2


no_of_rows = 5
no_of_columns = 4

state = []
for i in range(0, no_of_rows):
    row = []
    for j in range(0, no_of_columns):
        row.append(random.randint(0,15))
    state.append(row)

def gamestate_to_bytes(gamestate):
    gamestate_bytes = bytes()
    for row in gamestate:
        for column_index in range(0, no_of_columns, 2):
            field_1 = row[column_index]
            field_2 = row[column_index + 1]
            encoded_fields_int = field_1 + field_2 * 16
            encoded_fields_byte = encoded_fields_int.to_bytes(1, byteorder='big')
            gamestate_bytes += encoded_fields_byte
    return gamestate_bytes


def bytes_to_gamestate(bytes_array):
    gamestate_ints = []
    for row_index in range(no_of_rows):
        row_ints = []
        for row_element_index in range(int(no_of_columns/2)):
            encoded_fields_int = bytes_array[row_index*int(no_of_columns/2)+row_element_index]
            field_1 = encoded_fields_int % 16
            field_2 = encoded_fields_int // 16
            row_ints.extend((field_1, field_2))
        gamestate_ints.append(row_ints)
    return gamestate_ints

print_game_state_pretty()
state_bytes = gamestate_to_bytes(state)
new_state = bytes_to_gamestate(state_bytes)
identical = True
for (row_index, row) in enumerate(state):
    for (col_index, col) in enumerate(row):
        if col != new_state[row_index][col_index]:
            print('Something doesn\'t match')
            identical = False
            break
state = new_state
print_game_state_pretty()
if identical:
    print('Lists are identical')
