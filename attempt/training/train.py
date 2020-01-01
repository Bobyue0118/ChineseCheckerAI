import argparse
import sys
import os

import random
import numpy as np
from collections import deque
import torch
from torch.autograd import Variable
from tqdm import tqdm

import torch.nn as nn
from  NNmodel import StateNet
from dataloader import RandomDataset
from tensorboardX import SummaryWriter
from loss_function import Vertical_loss
from path import Path


parser = argparse.ArgumentParser(description='Chinese Checker model training',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--lr', '--learning-rate', default=2e-4, type=float,
                    metavar='LR', help='initial learning rate')
parser.add_argument('--momentum', default=0.9, type=float, metavar='M',
                    help='momentum for sgd, alpha parameter for adam')
parser.add_argument('--beta', default=0.999, type=float, metavar='M',
                    help='beta parameters for adam')
parser.add_argument('--weight-decay', '--wd', default=0, type=float,
                    metavar='W', help='weight decay')
parser.add_argument('--epochs', default=20000, type=int, metavar='N',
                    help='number of total epochs to run')
parser.add_argument('--DataNum', default=1000, type=int, metavar='N',
                    help='number of total epochs to run')
parser.add_argument('--seed', default=0, type=int, help='seed for random functions, and network initialization')
parser.add_argument('-b', '--batch-size', default=4, type=int,
                    metavar='N', help='mini-batch size')
parser.add_argument('-j', '--workers', default=4, type=int, metavar='N',
                    help='number of data loading workers')

parser.add_argument('--pretrained-net', dest='pretrained_net', default=None, metavar='PATH',
                    help='path to pre-trained net model')
parser.add_argument('--name', dest='name', type=str, default='demo', required=True,
                    help='name of the experiment, checpoints are stored in checpoints/name')

def main():
    global args
    args = parser.parse_args() 
    save_path = Path(args.name)
    save_path = 'checkpoints'/save_path #/timestamp
    save_path.makedirs_p()

    training_writer = SummaryWriter(save_path)
    

    judge_net = StateNet().cuda()
    judge_net = torch.nn.DataParallel(judge_net)
    if args.pretrained_net:
        print("=> using pre-trained weights for StateNet")
        weights = torch.load(args.pretrained_net)
        judge_net.load_state_dict(weights)
    else:
        judge_net.init_weights()


    parameters = StateNet().parameters()
    optimizer = torch.optim.Adam(parameters, args.lr,
                                 betas=(args.momentum, args.beta),
                                 weight_decay=args.weight_decay)
    
    train_set = RandomDataset(num_of_states=args.DataNum, seed=args.seed)
    data_set = torch.utils.data.DataLoader(
        train_set, batch_size=args.batch_size, shuffle=True,  
        num_workers=args.workers, pin_memory=True, drop_last=True)
        
    for epoch in tqdm(range(args.epochs)): #每一轮训练：
        loss = train (judge_net, optimizer, data_set)
        # print('666666666666666666')
        training_writer.add_scalar('loss', loss.item(), epoch)
        if(epoch % 50 is 0):
            torch.save(judge_net.state_dict(), save_path/'checkpoint.pth.tar') 

def train(judge_net, optimizer, data_set):
    global args
    judge_net.train()

    for i ,board_state in enumerate(data_set):
        

        board_state = Variable(board_state.type(torch.FloatTensor) .cuda())
        state_value = judge_net(board_state)
        
        traditional_value = (Vertical_loss(board_state)).cuda()

        loss =( torch.abs(state_value.float()-traditional_value.float())).mean()

        # print(loss)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    return loss





if __name__ == '__main__':

    main()