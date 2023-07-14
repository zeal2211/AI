#Importing Modules
import math, sys

#Checking the arguments given 
args = sys.argv[1:]

file_read = args[0]
file_write = args[1]
depth_to_be_checked = args[2]

board = []
#Opening the file and reading it
try:
    f = open(file_read, 'r')
except:
    print("No file found")  
content = f.read()
f.close()

#Adding the contents in the file to a list
for letter in content:
    board.append(letter)
   

#Generate all the possible moves for a given board postions
def generate_add(board):
    moves = []
    for i in range(len(board)):
        if board[i] == 'x':
            new_board = board.copy()
            new_board[i] = 'W'
            if close_mill(i, new_board):
                generate_remove(new_board, moves)
            else:
                moves.append(new_board)
    return moves

# If there is a closed mill after placing, 
# remove opponent's piece if possible
def generate_remove(board, moves):
    for i in range(len(board)):
        if board[i] == 'B':
            if not close_mill(i, board):
                new_board = board.copy()
                new_board[i] = 'x'
                moves.append(new_board)
    if len(moves) == 0:
        moves.append(board)

#Get the neighbors for a given location on the board
def get_neighbors(location):
    match location:
        case 0:
            return [1,6]
        case 1:
            return [0,11]
        case 2:
            return [3,7]
        case 3:
            return [2,10]
        case 4:
            return [5,8]
        case 5:
            return [4,9]
        case 6:
            return [0,7,18]
        case 7:
            return [8,6,15,2]
        case 8:
            return [7,12,4]
        case 9:
            return [10,14,5]
        case 10:
            return [9,17,3,11]
        case 11:
            return [10,20,1]
        case 12:
            return [8,13]
        case 13:
            return [12,14]
        case 14:
            return [9,13]
        case 15:
            return [7,16]
        case 16:
            return [15,19,17,13]
        case 17:
            return [16,10]
        case 18:
            return [6,19]
        case 19:
            return [18,20,16]
        case 20:
            return [11,19]
        
#Return a boolean value if there is a closed mill or not.
def close_mill(location, board):
    if board[location] != 'x':
        piece = board[location] 
        match location:
            case 0:
                return board[6] == piece and board[18] == piece
            case 1:
                return board[11] == piece and board[20] == piece
            case 2:
                return board[7] == piece and board[15] == piece
            case 3:
                return board[10] == piece and board[17] == piece
            case 4:
                return board[8] == piece and board[12] == piece
            case 5:
                return board[9] == piece and board[14] == piece
            case 6:
                return (board[7] == piece and board[8] == piece) or (board[0] == piece and board[18] == piece)
            case 7:
                return (board[6] == piece and board[8] == piece) or (board[15] == piece and board[2] == piece)
            case 8:
                return (board[6] == piece and board[7] == piece) or (board[4] == piece and board[12] == piece)
            case 9:
                return (board[11] == piece and board[10] == piece) or (board[5] == piece and board[14] == piece)
            case 10:
                return (board[9] == piece and board[11] == piece) or (board[17] == piece and board[3] == piece)
            case 11:
                return (board[9] == piece and board[10] == piece) or (board[1] == piece and board[20] == piece)
            case 12:
                return (board[4] == piece and board[8] == piece) or (board[14] == piece and board[13] == piece)
            case 13:
                return (board[19] == piece and board[16] == piece) or (board[14] == piece and board[12] == piece)
            case 14:
                return (board[9] == piece and board[5] == piece) or (board[12] == piece and board[13] == piece)
            case 15:
                return (board[2] == piece and board[7] == piece) or (board[17] == piece and board[16] == piece)
            case 16:
                return (board[17] == piece and board[15] == piece) or (board[19] == piece and board[13] == piece)
            case 17:
                return (board[3] == piece and board[10] == piece) or (board[15] == piece and board[16] == piece)
            case 18: 
                return (board[0] == piece and board[6] == piece) or (board[19] == piece and board[20] == piece)
            case 19:
                return (board[18] == piece and board[20] == piece) or (board[13] == piece and board[16] == piece)
            case 20:
                return (board[18] == piece and board[19] == piece) or (board[1] == piece and board[11] == piece)
    return False 


counter = 0 # Counter to check how many times static estimation gets called.
def static_estimation_opening(board, depth):
    global counter 
    counter += 1
    num_white_pieces = board.count('W')
    num_black_pieces = board.count('B')
    total_neighbors_value = 0
    white = 0
    black = 0
    for location,piece in enumerate(board):
        if piece == 'W':
            white += len(get_neighbors(location))
        elif piece == 'B':
            black += len(get_neighbors(location))
        total_neighbors_value = white - black
        
    return (1000*(num_white_pieces - num_black_pieces)) + total_neighbors_value

#Swap 'W' and 'B' pieces on the board
def swap_color(board):
    new_board = []
    for color in board:
        if color == 'W':
            new_board.append('B')
        elif color == 'B':
            new_board.append('W')
        else:
            new_board.append(color)
    return new_board

#Minimax algorithm implementaion for opening
def minimax(board, depth, maximizing_player):
    if depth == 0:     
        return static_estimation_opening(board,depth)

    if maximizing_player:
        max_eval = -math.inf
        boards = generate_add(board)
        for board in boards:
            new_score = minimax(board,depth - 1, False)
            max_eval = max(max_eval, new_score)    
        return max_eval
    else:
        min_eval = math.inf
        swapped_board = swap_color(board)
        boards = generate_add(swapped_board)
        for board in boards:
            new_board = swap_color(board)
            new_score = minimax(new_board,depth - 1,True)
            min_eval = min(min_eval,new_score )
        return min_eval 

#Intializing all the possible output board combinations for the given input
boards = generate_add(board)
best_move = []
max_score = -math.inf
for board in boards:
       score = minimax(board,(int(depth_to_be_checked) - 1),False) 
       if score > max_score:
           max_score = score
           best_move = board

#Writing into the file given in the sys argv.
move = ''.join(best_move)
f = open(file_write,'w')
f.write(f'Board Position: {move} \nPositions evaluated by static estimation: {counter}\nMINIMAX estimate: {max_score}')
f.close()