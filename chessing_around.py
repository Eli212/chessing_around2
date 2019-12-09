import sys

import calc as calc
import chess
import time
import os
import matplotlib.pyplot as plt
import pandas as pd
import pymongo
import mysql.connector
import threading
import multiprocessing

# from gui import ChessboardApp

white_best_turns = {}
dict_turns = {}
final_dict_turns = {}
counter_total_games = 0
start_time = 0

global_file_name = ""
running_threads = 0
current_turn = 0
thread_num = 1
final_num_of_games = -1
many_inserts = []
db = []
mySql_insert_query = "INSERT INTO moves (old_move, new_move) " \
                         "VALUES (%s, %s) ON DUPLICATE KEY UPDATE count = count + 1"
exit_num_of_games = 500

mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '123456789',
        database = 'testdb'
    )
mycurser = mydb.cursor()
# mycurser.execute("SHOW columns FROM moves")


# def always_running():
#     global dbz
#     global running_threads
#     global counter_total_games
#     global final_num_of_games
#
#     inini = time.time()
#     while True:
#         if len(dbz) != 0:
#             # print(multiprocessing.cpu_count())
#             dbz[0].start()
#             dbz[0].join()
#             del dbz[0]  # Maybe move this to inside the thread
#         if counter_total_games == final_num_of_games and len(dbz) == 0:
#             print((time.time() - inini) / 60)
#             break


def always_running2():
    global many_inserts
    global mySql_insert_query

    inini = time.time()
    while True:
        if len(many_inserts) != 0:
            hey = many_inserts.copy()
            many_inserts = []
            mycurser.executemany(mySql_insert_query, hey)
            mydb.commit()
        if counter_total_games == final_num_of_games and len(many_inserts) == 0:
            print((time.time() - inini) / 60)
            break


def print_info():
    global global_file_name
    global many_inserts

    while True:
        time.sleep(2)
        print(str(counter_total_games) + " games // " + str((time.time() - start_time)/60)
              + "minutes // file: " + global_file_name + "\nRunning threads: " + str(threading.active_count()) +
              "\nmany_inserts: " + str(len(many_inserts)) + "ctg:" + str(counter_total_games)
              + "fnog: " + str(final_num_of_games))

        if counter_total_games == final_num_of_games and len(many_inserts) == 0:
            break


def resetDB():
    sql_formula = f"DROP TABLE moves"
    mycurser.execute(sql_formula)
    mydb.commit()

    sql_formula2 = f"CREATE TABLE moves (old_move CHAR(64) NOT NULL, new_move VARCHAR(5) NOT NULL," \
                   f" count INTEGER (2) DEFAULT 1, CONSTRAINT PK_Move PRIMARY KEY (old_move, new_move))"
    mycurser.execute(sql_formula2)
    mydb.commit()


def mysql_func():
    pass
    # global many_inserts
    # sql_formula = f"INSERT INTO moves (old_move, new_move) " \
    #               f"VALUES ('a', 'b') ON DUPLICATE KEY UPDATE count = count + 1"
    # many_inserts.append(sql_formula)
    # sql_formula = f"INSERT INTO moves (old_move, new_move) " \
    #               f"VALUES ('aa', 'bb') ON DUPLICATE KEY UPDATE count = count + 1"
    # many_inserts.append(sql_formula)
    # asdf = ('a', 'b')
    # many_inserts.append(asdf)
    # asdf = ('a', 'bb')
    # many_inserts.append(asdf)
    # asdf = ('a', 'bb')
    # many_inserts.append(asdf)
    # mycurser.executemany(mySql_insert_query, many_inserts)
    #
    # mydb.commit()
    # new_formula2 = f"UPDATE moves SET num_k = num_k + 1, num_p = num_p + 1 WHERE old_move = 'asd'"
    # mycurser.execute(new_formula2)
    # mydb.commit()
    # Set data to DB
    # sqlFormula = "INSERT INTO students (id) VALUES (%s)"
    # student1 = [("Racahel", 22),
    #             ("Rachel2", 223),
    #             ("Rachel3", 224),
    #             ("Rachel4", 225)]
    # mycurser.executemany(sqlFormula, student1)
    # mycurser.execute("INSERT INTO moves VALUES ('asd', 0, 0, 0, 0, 0)")
    # mydb.commit()
    # mycurser.execute("SHOW TABLES")
    # mycurser.execute("CREATE TABLE moves (old_move VARCHAR(255), num_r INTEGER(6), num_q INTEGER(6), num_b INTEGER(6), num_p INTEGER(6), num_k INTEGER(6))")
    # mydb.commit()
    # Get data from DB
    # mycurser.execute("SELECT * FROM students WHERE age > 223")
    # mycurser.execute("UPDATE students SET age = age + 100 WHERE name = 'Rachel4'")
    # mydb.commit()
    # mycurser.execute("ALTER TABLE students ADD id2 VARCHAR(100)")
    # mycurser.execute("DROP TABLE moves")
    # mydb.commit()
    # mycurser.execute("UPDATE students SET familyName = 'hi'")

    # mydb.commit()
    # mycurser.execute("SELECT * FROM students WHERE age = 7232")
    # myresult = mycurser.fetchall()
    # if not mycurser.fetchone():
    #     print("AAAAA")
    # for row in mycurser:



    # for db in mycurser:
    #     print(db)
    # mycurser.execute('CREATE DATABASE testdb')

def reading_test():
    global db
    inini = time.time()
    file = open(os.getcwd() + "/../201301.pgn", "r")
    while True:
        check = file.readline()  # Reading the next line and checking if it's end of file!
        if check is "":
            break
        if check[0] == '1':
            db.append(check)
            count = 0
    # print(db)
    print((time.time() - inini) / 60)
    read_in_files2()


def read_games_to_dict_turns():
    global start_time
    global global_file_name

    # file_names = ["201301.pgn", "201302.pgn", "201303.pgn", "201304.pgn", "201305.pgn", "201306.pgn"]
    # file_names = [os.getcwd() + "/../201301.pgn", os.getcwd() + "/../201302.pgn"]
    file_names = [os.getcwd() + "/../201301.pgn"]

    print("I will read all the next files:")
    for file_name in file_names:
        print(file_name)
    global_file_name = file_name
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

def read_in_files3():
    global db
    global counter_total_games

    for game in db:
        board = chess.Board()

        if '%' in game:
            continue
        # print("aa:" + game)
        counter_total_games += 1

        kill_in_string = "x#=+"

        for char in kill_in_string:
            game = game.replace(char, "")

        if game[-7:] == "1/2-1/2":
            game = game[:-8]
        else:
            game = game[:-4]

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
            ### start of move_to_dict here ###
            # The next 2 lines is necessary only to run in AWS-EC2 because it's not
            # reading the correct str func in the init file of the library 'chess'
            old_move = old_move.__str__().replace("\n", "")
            old_move = old_move.__str__().replace(" ", "")
            many_inserts.append((old_move, move[0]))
            ### end of move_to_dict here ###
            # add_move_to_dict(old_move.__str__(), move[0])
            # x = threading.Thread(target=add_move_to_dict, args=[old_move.__str__(), move[0]])
            # dbz.append(x)

            # Black's turn
            move = game.split(" ", 1)
            board.push_san(move[0])
            if len(move) != 2:
                break
            game = move[1]

            # Skip the "i. "
            move = game.split(" ", 1)
            game = move[1]


def read_in_files2():
    global counter_total_games
    global many_inserts
    global db

    start_time = time.time()
    with open(os.getcwd() + "/../201302.pgn", 'r') as file:
        data = file.read()

    while True:
        # Create board
        board = chess.Board()

        # Skip to game
        while data[:4] != "\n1. ":
            check = data.split('\n', 1)
            if check[0] is "":
                return
            data = check[1]

        # print(data)
        split_data = data.split('\n', 1)
        split_data = split_data[1].split('\n', 1)
        game = split_data[0]
        if '%' in game:
            continue
        # print("aa:" + game)
        counter_total_games += 1

        kill_in_string = "x#=+"

        for char in kill_in_string:
            game = game.replace(char, "")

        if game[-7:] == "1/2-1/2":
            game = game[:-8]
        else:
            game = game[:-4]

        game = game.split(" ", 1)[1]

        while True:
            # Copying the current board to send it for update after making the next step
            old_move = board.copy()

            # White's turn
            move = game.split(" ", 1)
            # print("move: " + move)
            board.push_san(move[0])
            if len(move) != 2:
                break
            game = move[1]

            # reading the correct str func in the init file of the library 'chess'
            old_move = old_move.__str__().replace("\n", "")
            old_move = old_move.__str__().replace(" ", "")
            many_inserts.append((old_move, move[0]))
            ### end of move_to_dict here ###

            # Black's turn
            move = game.split(" ", 1)
            board.push_san(move[0])
            if len(move) != 2:
                break
            game = move[1]

            # Skip the "i. "
            move = game.split(" ", 1)
            game = move[1]

        if counter_total_games % 500 == 0:
            print("asd")
            print(str(counter_total_games) + " games // " + str((time.time() - start_time)/60)
                  + "minutes")

        split_data = split_data[1].split('\n', 1)
        data = split_data[1]

a = 0
b = 0
def read_in_files(file, file_name):
    global dict_turns
    global counter_total_games
    global many_inserts
    global a
    global b


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
            a += 1
        else:
            game = game[:-5]
            b += 1

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
            ### start of move_to_dict here ###
            # The next 2 lines is necessary only to run in AWS-EC2 because it's not
            # reading the correct str func in the init file of the library 'chess'
            old_move = old_move.__str__().replace("\n", "")
            old_move = old_move.__str__().replace(" ", "")
            many_inserts.append((old_move, move[0]))
            ### end of move_to_dict here ###
            # add_move_to_dict(old_move.__str__(), move[0])
            # x = threading.Thread(target=add_move_to_dict, args=[old_move.__str__(), move[0]])
            # x.start()
            # dbz.append(x)

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
        # print(counter_total_games)
        # if counter_total_games == 2000:
        #     print("time: " + str(time.time() - aa))
        # if counter_total_games % exit_num_of_games == 0:
        #     print(str(counter_total_games) + " games // " + str((time.time() - start_time)/60)
        #           + "minutes // file: " + file_name)
            # sys.exit()
        # Skip to next game
        file.readline()


def add_move_to_dict(old_move, new_move):
    global running_threads
    global many_inserts

    # while True:
    #     if running_threads < 4:
    running_threads += 1

    # The next 2 lines is necessary only to run in AWS-EC2 because it's not
    # reading the correct str func in the init file of the library 'chess'
    old_move = old_move.replace("\n", "")
    old_move = old_move.replace(" ", "")

    # mydb.cursor(buffered=True)

    # sql_formula = f"INSERT INTO moves (old_move, new_move) " \
    #               f"VALUES ('{old_move}', '{new_move}') ON DUPLICATE KEY UPDATE count = count + 1"

    many_inserts.append((old_move, new_move))

    running_threads -= 1
    return
    # mycurser.execute(sql_formula)

    # mydb.commit()


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
    file = open("final_file.txt", "w")
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


def final_dict_to_excel():
    global final_dict_turns
    # output_df = pd.DataFrame(columns=['current board', 'move'])
    df = pd.DataFrame()
    df['Current Board'] = final_dict_turns.keys()
    df['Move'] = final_dict_turns.values()
    df.to_csv('hi.csv')


if __name__ == '__main__':

    y = threading.Thread(target=always_running2, args=())
    y.start()

    time_thread = threading.Thread(target=print_info, args=())
    time_thread.start()
    # print("a")
    # mysql_func()
    # print("aa")

    print("Reseting DB..")
    resetDB()
    print("DB Restarted")

    # reading_test()

    # fbase()

    # read_from_file_time_to_dict_turns = time.time()
    # read_from_file_to_dict_turns()
    # print(str(((time.time() - read_from_file_time_to_dict_turns) / 60)) + " minutes")

    read_from_file_time = time.time()
    read_games_to_dict_turns()
    print(str(((time.time() - read_from_file_time) / 60)) + " minutes")
    final_num_of_games = counter_total_games
    print("num of games: " + str(counter_total_games))

    # read_from_file_time2 = time.time()
    # read_in_files2()
    # print(str(((time.time() - read_from_file_time2) / 60)) + " minutes")
    # final_num_of_games = counter_total_games
    # print("num of games: " + str(counter_total_games))

    # write_to_dict_turns_time = time.time()
    # write_dict_turns_to_file()
    # print(str(((time.time() - write_to_dict_turns_time) / 60)) + " minutes")

    # print("Getting best moves")
    # start_time2 = time.time()
    # get_best_moves_dict()
    # print(str(((time.time() - start_time2) / 60)) + " minutes")
    #
    # print("Putting into excel")
    # start_time3 = time.time()
    # final_dict_to_excel()
    # print(str(((time.time() - start_time3) / 60)) + " minutes")

    # print("Writing to final file")
    # write_final_file_start_time = time.time()
    # write_final_file()
    # print(str(((time.time() - write_final_file_start_time) / 60)) + " minutes")

    # print("Reading from final file")
    # read_final_file_start_time = time.time()
    # read_final_file()
    # print("Ended reading from file. details:")
    # print(str(((time.time() - read_final_file_start_time) / 60)) + " minutes")

    # read_from_file_to_dict_turns()
    # read_file2()
    # ChessboardApp().run()
    print("a: " + str(a))
    print("b: " + str(b))