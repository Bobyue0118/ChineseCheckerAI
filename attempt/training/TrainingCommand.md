# Command for Training Model 

python3 train.py    --name my_test

## Some parameters:
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


# Command for Tensorboard

tensorboard --logdir=..

