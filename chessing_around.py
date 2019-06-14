import chess
import time
import os
import matplotlib.pyplot as plt

# from gui import ChessboardApp

white_best_turns = {}
dict_turns = {}
final_dict_turns = {}
counter_total_games = 0
start_time = 0


def read_games_to_dict_turns():
    global start_time

    # file_names = ["201301.pgn", "201302.pgn", "201303.pgn", "201304.pgn", "201305.pgn", "201306.pgn"]
    # file_names = ["/Users/Eliko/desktop/chessing around files/201301.pgn"]
    file_names = [os.getcwd() + "/../201308.pgn", os.getcwd() + "/../201309.pgn"]
    print("I will read all the next files:")
    for file_name in file_names:
        print(file_name)

    start_time = time.time()

    for file_name in file_names:
        file = open(file_name, "r")
        file.seek(0, os.SEEK_END)
        file.seek(0)

        print("Starting to read from file: " + file_name)
        read_in_files(file, file_name)

    # write_dict_turns_to_file()
    # get_best_moves_dict()
    # write_file2()


def read_in_files(file, file_name):
    global dict_turns
    global counter_total_games

    # for game_in_text in range(10_000_000): # Run for a specific range of games
    while True:
        # Create board
        board = chess.Board()

        # Skip to game
        while file.read(4) != "\n1. ":
            check = file.readline()  # Reading the next line and checking if it's end of file!
            if check is "":
                return

        # Get the game
        game = file.readline()

        # Remove games with time
        if '%' in game:
            continue

        # Count total games (not including games with time
        counter_total_games += 1

        # Kill eaten, checkmate, pawn to end and check
        kill_in_string = "x#=+"
        for char in kill_in_string:
            game = game.replace(char, "")

        # Kill "1. " for draw games and win/lose games
        if game[-8:-1] == "1/2-1/2":
            game = game[:-9]
        else:
            game = game[:-5]

        while True:
            # Copying the current board to send it for update after making the next step
            old_move = board.copy()

            # White's turn
            move = game.split(" ", 1)
            board.push_san(move[0])
            if len(move) != 2:
                break
            game = move[1]

            # add a note
            add_move_to_dict(old_move.__str__(), move[0])

            # Black's turn
            move = game.split(" ", 1)
            board.push_san(move[0])
            if len(move) != 2:
                break
            game = move[1]

            # Skip the "i. "
            move = game.split(" ", 1)
            game = move[1]

        # Print info
        if counter_total_games % 1000 == 0:
            print(str(counter_total_games) + " games // " + str((time.time() - start_time)/60)
                  + "minutes // file: " + file_name)

        # Skip to next game
        file.readline()


def add_move_to_dict(old_move, new_move):
    # The next 2 lines is necessary only to run in AWS-EC2 because it's not
    # reading the correct str func in the init file of the library 'chess'
    old_move = old_move.replace("\n", "")
    old_move = old_move.replace(" ", "")

    if old_move in dict_turns:
        if new_move in dict_turns.get(old_move):
            (dict_turns.get(old_move))[new_move] = dict_turns.get(old_move).get(new_move) + 1
        else:
            (dict_turns.get(old_move))[new_move] = 1
    else:
        dict_turns[old_move] = {new_move: 1}


def get_most_common(board):
    sorted_x = sorted(board.items(), key=lambda kv: kv[1])
    sorted_x.reverse()
    return sorted_x[0][0]


def get_best_moves_dict():
    global final_dict_turns
    print("num of keys in dict_turns: " + str(len(dict_turns.keys())))
    for move in dict_turns:
        final_dict_turns[move] = get_most_common(dict_turns.get(move))


def write_dict_turns_to_file():
    # dict_turns: {"board" : {e4: 14, d5: 9}}

    # file = open(os.getcwd() + "/../dict_turns.txt", "w")
    file = open(os.getcwd() + "/../dict_turns.txt", "w")
    file.write(str(len(dict_turns.keys())) + "\n")
    counter = 0
    for board in dict_turns:
        counter += 1
        if counter % 1000000 == 0:
            print("Wrote " + str(counter) + " boards to file")
        file.write(board + "\n" + str(len(dict_turns.get(board).keys())) + "\n")
        for move in dict_turns.get(board):
            file.write(move + "\n" + str(dict_turns.get(board).get(move)) + "\n")

    file.close()


def read_from_file_to_dict_turns():
    # file = open("dict_turns", "r")
    file = open(os.getcwd() + "/../dict_turns.txt", "r")
    dict_turns_length = int(file.readline())
    print("reading " + str(dict_turns_length) + " boards")
    for board in range(dict_turns_length):
        if board % 1000000 == 0:
            print(board)
        board_str = file.readline()
        moves_length = int(file.readline())
        temp_inside_dict_turn = {}
        for move in range(moves_length):
            the_key = file.readline()
            the_value = int(file.readline())
            temp_inside_dict_turn[the_key[:-1]] = the_value
        dict_turns[board_str[:-1]] = temp_inside_dict_turn

    file.close()


def write_file2():
    global dict_turns

    file2 = open("just_file.txt", "w")
    file2.write(str(len(dict_turns.keys())) + "\n")
    max_games = len(dict_turns.keys())
    count = 0
    print("starting writing to file. number of boards: " + str(max_games))
    writing_time = time.time()

    for move in dict_turns.keys():
        count += 1
        string3 = calc(dict_turns.get(move))
        file2.write(move + "\n" + string3 + "\n")

        if round(max_games*0.1) == count:
            print("10% of writing is complete. Time: " + str(((time.time() - writing_time)/60)) + " minutes")
        elif round(max_games*0.2) == count:
            print("20% of writing is complete. Time: " + str(((time.time() - writing_time)/60)) + " minutes")
        elif round(max_games*0.3) == count:
            print("30% of writing is complete. Time: " + str(((time.time() - writing_time)/60)) + " minutes")
        elif round(max_games*0.4) == count:
            print("40% of writing is complete. Time: " + str(((time.time() - writing_time)/60)) + " minutes")
        elif round(max_games*0.5) == count:
            print("50% of writing is complete. Time: " + str(((time.time() - writing_time)/60)) + " minutes")
        elif round(max_games*0.6) == count:
            print("60% of writing is complete. Time: " + str(((time.time() - writing_time)/60)) + " minutes")
        elif round(max_games*0.7) == count:
            print("70% of writing is complete. Time: " + str(((time.time() - writing_time)/60)) + " minutes")
        elif round(max_games*0.8) == count:
            print("80% of writing is complete. Time: " + str(((time.time() - writing_time)/60)) + " minutes")
        elif round(max_games*0.9) == count:
            print("90% of writing is complete. Time: " + str(((time.time() - writing_time)/60)) + " minutes")

    print("Done writing to file!")

    file2.close()


# Checks best move for dictionary of type: {board: "e4"}
# def check_best_move(board):
#     for move in white_best_turns.keys():
#         if move[:-1] == board:  # It's [:-1] because there is one more space in the original string
#             return white_best_turns.get(move)[:-1]
#     return -1


def check_specific_best_move(board):
    for move in final_dict_turns.keys():
        if move == board:
            best_move = final_dict_turns.get(move)
            print("best move: " + best_move)
            return best_move
    return -1


def read_file2():
    global white_best_turns

    file = open("just_file.txt", "r")

    loop_times = int(file.readline())
    print("Loop times: " + str(loop_times))

    for loop in range(loop_times):
        current_turn = ""

        for loop_first_turn in range(8):
            current_turn += file.readline()
        best_move = file.readline()
        white_best_turns[current_turn] = best_move


def write_final_file():
    file = open(os.getcwd() + "/../final_file.txt", "w")
    file.write(str(len(final_dict_turns.keys())) + "\n")
    for i in final_dict_turns.keys():
        file.write(i + "\n" + final_dict_turns.get(i) + "\n")
    file.close()


def read_final_file():
    global final_dict_turns

    file = open(os.getcwd() + "/../final_file.txt", "r")
    num_of_moves = int(file.readline())
    for i in range(num_of_moves):
        board = file.readline()
        move = file.readline()
        final_dict_turns[board] = move
    file.close()


if __name__ == '__main__':
    read_from_file_time_to_dict_turns = time.time()
    read_from_file_to_dict_turns()
    print(str(((time.time() - read_from_file_time_to_dict_turns) / 60)) + " minutes")

    read_from_file_time = time.time()
    read_games_to_dict_turns()
    print(str(((time.time() - read_from_file_time) / 60)) + " minutes")

    write_to_dict_turns_time = time.time()
    write_dict_turns_to_file()
    print(str(((time.time() - write_to_dict_turns_time) / 60)) + " minutes")

    print("Getting best moves")
    start_time2 = time.time()
    get_best_moves_dict()
    print(str(((time.time() - start_time2) / 60)) + " minutes")

    print("Writing to final file")
    write_final_file_start_time = time.time()
    write_final_file()
    print(str(((time.time() - write_final_file_start_time) / 60)) + " minutes")

    # print("Reading from final file")
    # read_final_file_start_time = time.time()
    # read_final_file()
    # print("Ended reading from file. details:")
    # print(str(((time.time() - read_final_file_start_time) / 60)) + " minutes")

    # read_from_file_to_dict_turns()
    # read_file2()
    # ChessboardApp().run()
