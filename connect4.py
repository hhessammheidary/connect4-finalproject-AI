import random
import numpy as np
import pygame
import sys
import math
from tkinter import *
from tkinter import messagebox


row_count = 6
column_count = 7
blue = (0, 100, 170)
black = (0, 0, 0)
red = (200, 35, 0)
yellow = (210,210, 0)



def creat_board():
    board = np. zeros((row_count, column_count))
    return board

def put_discs(board, row, column, disc):
    board[row][column] = disc

def is_valid_choice(board, column):
    return board[row_count - 1][column] == 0

def get_valid_choices(board):
    valids = []
    for column_index in range(column_count):
        if is_valid_choice(board, column_index):
            valids.append(column_index)

    return valids


def get_next_open_row(board, column):
    for i in range(row_count):
        if board[i][column] == 0:
            return i
        
def check_win(board, player):
    #check columns
    for row_index in range(row_count):
        for column_index in range(column_count - 3):
            if all(board[row_index][column_index+i] == player for i in range(4)):
                return True
    
    # Check row
    for row_index in range(row_count - 3):
        for column_index in range(column_count):
            if all(board[row_index+i][column_index] == player for i in range(4)):
                return True
    
    # Check diagonals
    for row_index in range(row_count - 3):
        for column_index in range(column_count - 3):
            if all(board[row_index+i][column_index+i] == player for i in range(4)):
                return True
            if all(board[row_index+3-i][column_index+i] == player for i in range(4)):
                return True
    
    # No winning combination found
    return False

def calc_h(part, player= 2):
    h = 0
    if part.count(player) == 4:
        h += 1000
    elif part.count(player) == 3 and part.count(0) == 1:
        h += 15
    elif part.count(player) == 2 and part.count(0) == 2:
        h += 10
    elif part.count(player) == 2 and part.count(0) == 1:
        h += 3
    elif part.count(player) == 1 and part.count(0) == 3:
        h += 5
    elif part.count(player) == 1 and part.count(0) == 2:
        h += 1
    elif part.count(player) == 0 and part.count(0) == 2:
        h -= 3
    elif part.count(player) == 0 and part.count(0) == 1:
        h -= 15

    return h

def heuristic(board, player= 2):
    h = 0

    for row_index in range(row_count):
        single_row = board[row_index, :]
        # single_row = [int(i) for i in list(board[row_index,:])]
        for column_index in range(column_count - 3):
            temp = list(single_row[column_index:column_index + 4])
            h += calc_h(temp)

    for row_index in range(row_count - 3):
        for column_index in range(column_count):
            single_col = board[:, column_index]
            # single_col = [int(i) for i in list(board[:,column_index])]
            temp = list(single_col[row_index:row_index + 4])
            h += calc_h(temp)

    for row_index in range(row_count - 3):
        for column_index in range(column_count - 3):
            temp = list(board[row_index + i][column_index + i] for i in range(4))
            h += calc_h(temp)
            temp = list(board[row_index + 3 - i][column_index + i] for i in range(4))
            h += calc_h(temp)

    return h


def is_end(board):
    return check_win(board , 1) or check_win(board ,2) or len(get_valid_choices(board)) == 0

def minmax(board ,depth ,alpha , beta ,maxPlayer):
    valid_choices = get_valid_choices(board)
    isEnd = is_end(board)
    if(depth == 0 or isEnd):
        if isEnd:
            if check_win(board ,2):
                return None,100000
            elif check_win(board ,1):
                return None,-100000
            # there is no more valid move
            else:
                return None,0
        else:
            return None,heuristic(board, 2)
    if maxPlayer:
        h_value = -math.inf #current score
        column = random.choice(valid_choices)
        for col in valid_choices:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            put_discs(board_copy, row ,col ,2)
            new_h = minmax(board_copy, depth-1,alpha ,beta , False)[1]
            if new_h > h_value:
                h_value = new_h
                column = col
            alpha = max(h_value ,alpha)
            if(alpha >= beta):
                break  #beta cut_off
        return column,h_value
    #min palyer
    else:
        h_value = math.inf #current score
        column = random.choice(valid_choices)
        for col in valid_choices:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            put_discs(board_copy, row ,col ,1)
            new_h = minmax(board_copy, depth-1 , alpha , beta, True)[1] #true and false help us switch between min and max
            if new_h < h_value:
                h_value = new_h
                column = col
            beta = min(h_value , beta)
            if alpha >= beta :
                break #alpha cut_off
        return column,h_value


        
def draw_board(board):
    temp = np.flip(board, 0)
    for i in range(row_count):
        for j in range(column_count):
            pygame.draw.rect(window, blue, (j * box_size, i * box_size + box_size, box_size, box_size))
            if temp[i][j] == 0:
                pygame.draw.circle(window, black, (j * box_size + int(box_size / 2), i * box_size + box_size + int(box_size / 2)), circle_rad)
            elif temp[i][j] == 1:
                pygame.draw.circle(window, red, (j * box_size + int(box_size / 2), i * box_size + box_size + int(box_size / 2)), circle_rad)
            elif temp[i][j] == 2:
                pygame.draw.circle(window, yellow, (j * box_size + int(box_size / 2), i * box_size + box_size + int(box_size / 2)), circle_rad)
    
            

        
board = creat_board()
print(board)
game_over = False
turn = 0

pygame.init()

box_size = 100
circle_rad = int(box_size / 2 - 2)

window_width = box_size * column_count
window_hight = box_size * (row_count + 1)
window_size = (window_width, window_hight)

window = pygame.display.set_mode(window_size)
draw_board(board)
pygame.display.update()

Tk().wm_withdraw() 




while not game_over:
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(window, blue, (0, 0, window_width, box_size))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(window, red, (posx, int(box_size/2)), circle_rad)
        pygame.display.update()


        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == 0:
                posx = event.pos[0]
                column = math.floor(posx / box_size)

                if is_valid_choice(board, column):
                    row = get_next_open_row(board, column)
                    put_discs(board, row, column, 1) ## disc player1 = 1
                    if check_win(board, 1):
                        game_over =True
                        messagebox.showinfo('yooo!!!', 'player 1 won:D')
                draw_board(board)
                turn = (turn + 1) % 2
                
    if turn == 1 and not is_end(board):
        column,minmax_value = minmax(board , 4, -math.inf , math.inf, True)
        if is_valid_choice(board, column):
            row = get_next_open_row(board, column)
            put_discs(board, row, column, 2) ## disc player2 = 2
            if check_win(board, 2):
                game_over =True
                messagebox.showinfo('yooo!!!', 'player 2 won:D')
        draw_board(board)
        turn = (turn + 1) % 2

    if game_over:
        pygame.time.wait(3000)
        break






# def connect4_heuristic(board, player):
#     # Define weights for different types of combinations
#     weights = {
#         'horizontal': 1,
#         'vertical': 2,
#         'diagonal': 3
#     }
    
#     # Evaluate the board for the specified player
#     count = 0
#     num_pieces = 0
#     proximity_score = 0
#     for row in range(len(board)):
#         for col in range(len(board[0])):
#             if board[row][col] == player:
#                 num_pieces += 1
#                 # Check for horizontal four-in-a-row
#                 if col <= len(board[0]) - 4:
#                     if board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player:
#                         count += weights['horizontal']
#                 # Check for vertical four-in-a-row
#                 if row <= len(board) - 4:
#                     if board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
#                         count += weights['vertical']
#                 # Check for diagonal four-in-a-row (bottom-left to top-right)
#                 if row >= 3 and col <= len(board[0]) - 4:
#                     if board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
#                         count += weights['diagonal']
#                 # Check for diagonal four-in-a-row (top-left to bottom-right)
#                 if row <= len(board) - 4 and col <= len(board[0]) - 4:
#                     if board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
#                         count += weights['diagonal']
                
#                 # Calculate proximity score
#                 for i in range(-2, 3):
#                     for j in range(-2, 3):
#                         if row+i >= 0 and row+i < len(board) and col+j >= 0 and col+j < len(board[0]):
#                             if board[row+i][col+j] == player:
#                                 proximity_score += 1 / (abs(i) + abs(j) + 1)
    
#     # Return a weighted sum of the count, number of pieces, and proximity score
#     return count + num_pieces + proximity_score
