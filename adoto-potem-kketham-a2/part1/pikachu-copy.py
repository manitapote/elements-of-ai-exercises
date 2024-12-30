#
# pikachu.py : Play the game of Pikachu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
#
# Based on skeleton code by D. Crandall, March 2021
#
import sys
import time
import copy
import math

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def tabular_board(board, N):
    i = 0
    j = 0
    tabular = [[0 for i in range(N)] for j in range(N)]

    for index in range(0, len(board)):
        tabular[i][j] = board[index]

        j = j + 1

        if j == N:
            j = 0
            i = i + 1

    return tabular

def print_string(board):
    k = ''
    for row in board:
        # print(''.join(row))
        k = k + ''.join(row)
    print(k)
    # return k

# Gets all the location of pichu and pikachu location
def current_piece_location(N, tabular, turn):
    current_pichu_location = []
    current_pikachu_location = []

    pikachu = 'W' if turn == 'w' else 'B'

    for row in range(N):
        for col in range(N):
            if tabular[row][col] == turn:
                current_pichu_location.append((row, col))

            if tabular[row][col] == pikachu:
                current_pikachu_location.append((row, col))

    return current_pichu_location, current_pikachu_location


def moves_for_pichu(locations, N, turn, board):
    move = []
    opposite = ['w', 'W'] if turn == 'b' else ['b', 'B']
    pikachu = 'B' if turn == 'b' else 'W'

    for row, col in locations:
        # move left
        if (col - 1 >= 0) and (board[row][col - 1] == '.'):
            # print('left')
            new_board = copy.deepcopy(board)
            new_board[row][col] = '.'
            new_board[row][col - 1] = turn
            move.append(((row, col - 1), new_board))
            # print_string(new_board)

        # move right
        if col + 1 < N and board[row][col + 1] == '.':
            # print('right')
            new_board = copy.deepcopy(board)
            new_board[row][col] = '.'
            new_board[row][col + 1] = turn
            move.append(((row, col + 1), new_board))
            # print_string(new_board)

        # move forward for white
        if turn == 'w' and row + 1 < N and board[row + 1][col] == '.':
            # print('forward')
            new_board = copy.deepcopy(board)
            new_board[row][col] = '.'

            new_value = pikachu if row + 1 == N - 1 else turn

            new_board[row + 1][col] = new_value
            move.insert(0, ((row + 1, col), new_board))
            # print_string(new_board)

        # move forward for black
        if turn == 'b' and row - 1 >= 0 and board[row - 1][col] == '.':
            # print('black forward 1')
            new_board = copy.deepcopy(board)
            new_board[row][col] = '.'

            new_value = pikachu if row - 1 == 0 else turn

            new_board[row - 1][col] = new_value
            move.insert(0, ((row - 1, col), new_board))
            # print_string(new_board)

        #move two squares forward, left and  right if opposite piece at two square distance
        move_left = col - 2 >= 0 and \
                    board[row][col - 1] in  opposite and \
                    board[row][col - 2] == '.'
                    # and \
                    # board[row][col - 3] in opposite and \
                    # board[row][col - 4] == '.'

        if move_left:
            # print('move left two \n')
            new_board = copy.deepcopy(board)
            new_board[row][col] = '.'
            new_board[row][col - 1] = '.'
            # new_value = pikachu if row - 4 == 0 else turn
            new_board[row][col - 2] = turn
            move.insert(0, ((row, col - 2), new_board))
            # print_string(new_board)


        move_right = col + 2 < N and \
                     board[row][col + 1] in opposite and \
                     board[row][col + 2] == '.' \
                     # and \
                     # board[row][col + 3] in opposite and \
                     # board[row][col + 4] == '.'

        if move_right:
            new_board = copy.deepcopy(board)
            new_board[row][col] = '.'
            new_board[row][col + 1] = '.'

            # new_value = pikachu if col + 4 == N-1 else turn
            new_board[row][col + 2] = turn
            move.insert(0, ((row, col + 2), new_board))
            # print_string(new_board)


        #move 2 forward for black
        move_forward = turn == 'b' and \
                       row - 2 >= 0 and \
                       board[row - 1][col] in opposite and \
                       board[row - 2][col] == '.'
                       # and \
                       # board[row - 3][col] in opposite and \
                       # board[row - 4][col] == '.'

        if move_forward:
            # print('move 2 forward')
            new_board = copy.deepcopy(board)
            new_board[row][col] = '.'
            new_board[row - 1][col] = '.'
            new_value = 'B' if row - 2 == 0 else 'b'
            new_board[row - 2][col] = new_value

            move.insert(0, ((row - 2, col), new_board))
            # print_string(new_board)

        #move 2 forward for white
        move_forward = turn == 'w' and \
                       row + 2 < N and \
                       board[row + 1][col] in opposite and \
                       board[row + 2][col] == '.' \
                       # and \
                       # board[row + 3][col] in opposite and \
                       # board[row + 4][col] == '.'

        if move_forward:
            # print('move 2 forward white')
            new_board = copy.deepcopy(board)
            new_board[row][col] = '.'
            new_board[row + 1][col] = '.'
            new_value = 'W' if row + 2 == N-1 else 'w'
            new_board[row + 2][col] = new_value

            move.insert(0, ((row + 2, col), new_board))
            # print_string(new_board)


    return move


def moves_for_pikachu(locations, N, turn, board):
    # print('########### pikachu start ####### \n')
    move = []
    opposite = ['w', 'W'] if turn == 'b' else ['b', 'B']
    same_group = ['w', 'W'] if turn == 'w' else ['b', 'B']
    pikachu = 'B' if turn == 'b' else 'W'
    # print(print_string(board))

    for row, col in locations:
        # move left
        # print('pikachu Moving left ## \n')

        # #left moves
        for j in range(col-1, -1, -1):
            if board[row][j] in same_group:
                break
            if board[row][j] in opposite and j - 1 >= 0 and board[row][j - 1] != '.':
                break

            if board[row][j] == '.':
                # print('moving left \n')
                new_board = copy.deepcopy(board)
                new_board[row][col] = '.'
                new_board[row][j] = pikachu
                move.append(((row, j), new_board))
                # print(print_string(board))
                # print_string(new_board)

            if board[row][j] in opposite and j - 1 >= 0 and board[row][j-1] == '.':
                # print('Eating pichu ... \n')
                for k in range(j - 1, -1, -1):
                    if board[row][k] != '.':
                        break

                    new_board = copy.deepcopy(board)
                    new_board[row][j] = '.'
                    new_board[row][col] = '.'
                    new_board[row][k] = pikachu
                    move.insert(0, ((row, k), new_board))
                    # print(row, k)
                    # print('Jumping over \n')
                    # print(print_string(board))
                    # print_string(new_board)

                break

        # #Right moves
        for j in range(col + 1, N):
            if board[row][j] in same_group:
                break
            if board[row][j] in opposite and j + 1 < N and board[row][j+1] != '.':
                break

            if board[row][j] == '.':
                # print('moving Right \n')
                new_board = copy.deepcopy(board)
                new_board[row][col] = '.'
                new_board[row][j] = pikachu
                move.append(((row, j), new_board))
                # print(print_string(board))
                # print_string(new_board)

            if board[row][j] in opposite and j + 1 < N and board[row][j + 1] == '.':
                # print('Eating pichu right... \n')
                # print(board[row][j+1])
                # print(row, j + 1)
                for k in range(j + 1, N):
                    if board[row][k] != '.':
                        break

                    new_board = copy.deepcopy(board)
                    new_board[row][j] = '.'
                    new_board[row][col] = '.'
                    new_board[row][k] = pikachu
                    move.insert(0, ((row, k), new_board))
                    # print(row, k)
                    # print('Jumping over right \n')
                    # print(print_string(board))
                    # print_string(new_board)

                break


        #Move forward for black
        # if pikachu == 'B':
        for i in range(row -1, -1, -1):
            if board[i][col] in same_group:
                break
            if board[i][col] in opposite and i - 1 >= 0 and board[i -1][col] != '.':
                break

            if board[i][col] == '.':
                # print('moving forward \n')
                new_board = copy.deepcopy(board)
                new_board[row][col] = '.'
                new_board[i][col] = pikachu
                move.append(((i, col), new_board))
                # print(print_string(board))
                # print_string(new_board)

            if board[i][col] in opposite and i - 1 >= 0 and board[i - 1][col] == '.':
                # print('Moving forward... \n')
                for k in range(i - 1, -1, -1):
                    if board[k][col] != '.':
                        break

                    new_board = copy.deepcopy(board)
                    new_board[i][col] = '.'
                    new_board[row][col] = '.'
                    new_board[k][col] = pikachu
                    move.insert(0, ((row, k), new_board))
                    # print(row, k)
                    # print('Jumping over forward \n')
                    # print(print_string(board))
                    # print_string(new_board)

                break

        # if pikachu == 'W':
        for i in range(row + 1, N):
            if board[i][col] in same_group:
                break

            if board[i][col] == '.':
                # print('moving forward \n')
                new_board = copy.deepcopy(board)
                new_board[row][col] = '.'
                new_board[i][col] = pikachu
                move.append(((i, col), new_board))
                # print(print_string(board))
                # print_string(new_board)

            if board[i][col] in opposite and i + 1 < N and board[i + 1][col] == '.':
                # print('Moving forward... \n')
                for k in range(i + 1, N):
                    if board[k][col] != '.':
                        break

                    new_board = copy.deepcopy(board)
                    new_board[i][col] = '.'
                    new_board[row][col] = '.'
                    new_board[k][col] = pikachu
                    move.insert(0, ((row, k), new_board))
                    # print(row, k)
                    # print('Jumping over forward\n')
                    # print(print_string(board))
                    # print_string(new_board)

                break
    return move

def score(board, turn, N):
    score = 0
    pikachu = 'B' if turn == 'b' else 'W'
    opposite = 'w' if turn == 'b' else 'b'
    opposite_pikachu = 'W' if turn == 'b' else 'B'
    opposite_score = 0

    for i in range(N):
        score = score + board[i].count(turn)
        score = score + 2 * board[i].count(pikachu)
        opposite_score = opposite_score + board[i].count(opposite)
        opposite_score = opposite_score + board[i].count(opposite_pikachu)

    if opposite_score == 0:
        return math.inf

    return score


def successors(board, N, turn):
    pichu_states, pikachu_states = current_piece_location(N, board, turn)
    # print(pichu_states)
    # new_board = copy.deepcopy(board)
    moves = moves_for_pichu(pichu_states, N, turn, board)
    pikachu_moves = moves_for_pikachu(pikachu_states, N, turn, board)

    if len(pikachu_moves) != 0:
        pikachu_moves.extend(moves)
        return pikachu_moves

    return moves


def min_max_value(board, depth, target_depth, turn, N, turn_max):
    if depth == target_depth:
        # print('turn ', turn, ' depth ', depth, ' score ', score(board, turn, N), 'max turn', turn_max)
        # print(print_string(board))
        return score(board, turn, N)

    if turn_max:
        v = -math.inf
        min_turn = 'w' if turn == 'b' else 'b'
        # print('############# Maxs turn ############ \n')
        for state, child_board in successors(board, N, turn):
            copy_board = copy.deepcopy(child_board)
            # print('###### parent ######### \n')
            # print(print_string(board))
            # print('######### child ######### \n')
            # print(print_string(copy_board))

            v = max(v, min_max_value(copy_board,
                                 depth + 1,
                                 target_depth,
                                 min_turn,
                                 N,
                                 False))
            # print(' max current value ', v)
        # print('max score', v, ' depth ', depth)
        # print(print_string(copy_board))
        return v
    else:
        v = math.inf
        # print('############# Mins turn ############ \n')
        for state, child_board in successors(board, N, turn):
            copy_board = copy.deepcopy(child_board)
            # print('###### parent ######### \n')
            # print(print_string(board))
            # print('##### child ###### \n')
            # print(print_string(copy_board))
            max_turn = 'w' if turn == 'b' else 'b'

            v = min(v, min_max_value(copy_board,
                                 depth + 1,
                                 target_depth,
                                 max_turn,
                                 N,
                                 True))
            # print(' min current value ', v)
        # print('min score', v, ' depth ', depth)
        # print(print_string(copy_board))
        return v

def find_best_move(board, N, player, timelimit):
    max_initial = -math.inf
    # print('error')
    # print(successors(tabular_board(board, N), N, player))
    for state, new_board in successors(tabular_board(board, N), N, player):
        # print(state)
        # print_string(new_board)
        # print(' ##### succesor ######## \n')
        # print_string(new_board)
        # print('-----------------')
        copy_board = copy.deepcopy(new_board)
        new_player = 'b' if player == 'w' else 'w'
        current_value = min_max_value(copy_board, 1, 4, new_player, N, False)
        # tabular_board(board)
        # print('max initial', max_initial)
        # print('current value ', current_value)
        if current_value >= max_initial:
            # print('######### solution for now ############ \n')
            print_string(new_board)
            # print('max initial', max_initial)
            # print('current value ', current_value)
            max_initial = current_value


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: pikachu.py N player board timelimit")

    (_, N, player, board, timelimit) = sys.argv

    N = int(N)
    timelimit = int(timelimit)

    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N * N or 0 in [c in "wb.WB" for c in board]:
        raise Exception("Bad board string.")
    # print(board_to_string(board, N))
    # print(successors(tabular_board(board, N), N, player))

    # find_best_move(tabular_board(board, N), N, player, timelimit)

    # print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    # print("Here's what I decided:")

    find_best_move(board, N, player, timelimit)

