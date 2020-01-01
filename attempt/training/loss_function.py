import torch
from torch.autograd import Variable

import torch.nn as nn

# heuristic evaluation
def Vertical_loss(board):  # this function returns a number as the evaluation value of a given state
    b,_,_,_ = board.size()
    board_judgement = []
    for i in range(0,b):# very stupid method but i dont have time to find a better way
        # print(board.size())
        state = converse_board_to_state(board[i,:,:,:])
        player_vertical_count = 0
        opponent_vertical_count = 0

        # print(state)
        
        for location, chess in state.items():
            # print(location)
            if chess is 2:
                player_vertical_count += location[0]
            if chess is 1:
                opponent_vertical_count += location[0]
            

        # final calculation

        if player_vertical_count == 170:
            player_vertical_count =  1000
        if opponent_vertical_count == 30:
            opponent_vertical_count =  -1000
        
        board_judgement.append(torch.tensor(player_vertical_count+opponent_vertical_count))
        

    return torch.cat((board_judgement[0].unsqueeze(0),
                    board_judgement[1].unsqueeze(0),
                    board_judgement[2].unsqueeze(0),
                    board_judgement[3].unsqueeze(0))
                    ,0)

    


def converse_state_to_board(state,OurPlayer = 2):
    # 默认我们是第二个下的，如果我们第一个下的话，将our_board与opponent_board交换
    def converse_one_by_one(location,player):
        if player is 1:
            if location[0] >10:
                x,y = -location[1]+10, location[0]+location[1]-11
            else :
                x,y = location[0]-location[1], location[1]-1
            opponent_board[x, y] = 1
            blank_board[x, y] = 0
            
        if player is 2 :
            if location[0] >10:
                x,y = -location[1]+10, location[0]+location[1]-11
            else :
                x,y = location[0]-location[1], location[1]-1
            our_board[x, y] = 1
            blank_board[x, y] = 0
            
    board = state
    our_board = np.zeros((10,10))
    opponent_board = np.zeros((10,10))
    blank_board = np.ones((10,10))
    for location, player in board.board_status.items() :
        converse_one_by_one(location, player)
    
    if OurPlayer is 1:
        return np.concatenate((opponent_board[np.newaxis,:,:],our_board[np.newaxis,:,:],blank_board[np.newaxis,:,:]),axis=0)
    else :
        return np.concatenate((our_board[np.newaxis,:,:],opponent_board[np.newaxis,:,:],blank_board[np.newaxis,:,:]),axis=0)


def converse_board_to_state(board):
    """
    return a dic as (x,y):1/2/0
    """
    state = {}
    our_board = board[0,:,:]
    opponent_board = board[1,:,:]

    for a in range(0,10):
        for b in range(0,10):
            if a+b<10:
                x = a+b+1
                y = b+1
            else :
                x = a+b+1
                y = 10-a
            if abs(our_board[a,b].item() - 1)<0.1:
                state[(x,y)] = 2

            if abs(opponent_board[a,b].item()-1)<0.1:
                state[(x,y)] = 1

    # print(len(state)) 20
            
    return state
