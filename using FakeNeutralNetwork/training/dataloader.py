import torch.utils.data as data
import numpy as np
from scipy.misc import imread
from path import Path
import random



class RandomDataset(data.Dataset):


    def __init__(self, num_of_states=200, seed=None): 
        np.random.seed(seed)
        random.seed(seed)
        self.board_states = []
        for state in range(0,num_of_states):
            our_board = np.zeros((10,10))
            opponent_board = np.zeros((10,10))
            blank_board = np.ones((10,10))
            for i in range(0,10): # our piece
                row = np.random.randint(0,10)
                col = np.random.randint(0,10)
                while abs(blank_board[row,col] - 0) < 0.1:
                    row = np.random.randint(0,10)
                    col = np.random.randint(0,10)

                blank_board[row,col] = 0
                our_board[row,col] = 1

            for i in range(0,10): # opponent piece
                row = np.random.randint(0,10)
                col = np.random.randint(0,10)
                while abs(blank_board[row,col] - 0) < 0.1:
                    row = np.random.randint(0,10)
                    col = np.random.randint(0,10)

                blank_board[row,col] = 0
                opponent_board[row,col] = 1
            
            self.board_states.append(np.concatenate((our_board[np.newaxis,:,:],opponent_board[np.newaxis,:,:],blank_board[np.newaxis,:,:]),axis=0))

            

        

    def __getitem__(self, index):

        return self.board_states[index]

    def __len__(self):
        return len(self.board_states)
