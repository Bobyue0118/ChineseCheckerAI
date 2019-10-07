import random, re, datetime


class Agent(object):
    def __init__(self, game):
        self.game = game
        

    def getAction(self, state):
        raise Exception("Not implemented yet")


class RandomAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)


class SimpleGreedyAgent(Agent):
    # a one-step-lookahead greedy agent that returns action with max vertical advance
    def getAction(self, state):
        legal_actions = self.game.actions(state)

        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        if player == 1:  # playing from bottom to top, hence later vertical value is smaller
            max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[0][0] - action[1][0] == max_vertical_advance_one_step]
        else:  # playing from top to bottom, hence later vertical value is larger
            max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[1][0] - action[0][0] == max_vertical_advance_one_step]
        self.action = random.choice(max_actions)


class iRoboticAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        ### START CODE HERE ###

        global staticDepth, cnt, repeat  # store the initial value for depth for minimax
        depth = 2                        # starting from 2
        staticDepth = depth              # store original depth
        memory = 20                      # breadth for each layer, max is 42
        board = state[1]
        player_status = board.getPlayerPiecePositions(player)

        temp = (player_status in q)
        q.append(player_status)

        cnt += 1

        if cnt >= 3 and temp:            # in case of "stuck" situation, use "greedy"
            q.remove(q[0])
            repeat += 1
            if repeat == 2:              # in case of repeated "stuck" situation
                self.action = random.choice(legal_actions)
            else:
                if player == 1:          # playing from bottom to top, hence later vertical value is smaller
                    max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
                    max_actions = [action for action in legal_actions if
                                    action[0][0] - action[1][0] == max_vertical_advance_one_step]
                else:                    # playing from top to bottom, hence later vertical value is larger
                    max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
                    max_actions = [action for action in legal_actions if
                                    action[1][0] - action[0][0] == max_vertical_advance_one_step]
                self.action = random.choice(max_actions)

        else:
            if cnt >= 3:
                q.remove(q[0])
            repeat = 0
            v = -float('inf')

            order = PriorityQueue()      # search with preference
            for action in legal_actions:
                order.put((-(3 - 2 * player) * (action[0][0] - action[1][0]), action))
            order_next = PriorityQueue()

            while True:
                count = 0
                while (not order.empty()) and (memory > count):
                    action = order.get()[1]
                    if self.evaluation(self.game.succ(state, action), player) == 1000:
                        self.action = action
                        break
                    count += 1
                    v_next = self.minimaxValue(player, self.game, self.game.succ(state, action), depth, v, float('inf'),
                                            memory)
                    order_next.put((-v_next, action))
                    if v_next > v:
                        v = v_next
                        self.action = action

                depth += 1
                staticDepth = depth
                del order
                order = PriorityQueue()
                while not order_next.empty():
                    order.put(order_next.get())

    # minimax algorithm
    def minimaxValue(self, player, game, state, depth, alpha, beta, memory):

        if depth == 0:
            return self.evaluation(state, player)
        else:
            depth -= 1

        if (staticDepth - depth) % 2 == 1:
            if self.evaluation(state, player) == 1000:
                return 1000

            v = float('inf')
            order = PriorityQueue()
            for action in game.actions(state):
                order.put(((3 - 2 * player) * (action[0][0] - action[1][0]), action))

            count = 0
            while (not order.empty()) and memory > count:
                action = order.get()[1]
                count += 1
                v = min(v, self.minimaxValue(player, game, game.succ(state, action), depth, alpha, beta, memory))
                if v <= alpha: return v
                beta = min(beta, v)
            # print("depth:", depth)
            return v

        else:
            if self.evaluation(state, player) == -1000:
                return -1000

            v = -float('inf')
            order = PriorityQueue()
            for action in game.actions(state):
                order.put((-(3 - 2 * player) * (action[0][0] - action[1][0]), action))

            count = 0
            while (not order.empty()) and memory > count:
                action = order.get()[1]
                count += 1
                v = max(v, self.minimaxValue(player, game, game.succ(state, action), depth, alpha, beta, memory))
                if v >= beta: return v
                alpha = max(alpha, v)
            return v

    # heuristic evaluation
    def evaluation(self, state, player):  # this function returns a number as the evaluation value of a given state

        board = state[1]
        player_status = board.getPlayerPiecePositions(player)
        opponent_status = board.getPlayerPiecePositions(3 - player)

        # vertical dimension
        player_vertical_count = 0
        for position in player_status:
            player_vertical_count += position[0]

        opponent_vertical_count = 0
        for position in opponent_status:
            opponent_vertical_count += position[0]

        # horizon dimension
        player_horizontal_count = 0
        for position in player_status:
            if position[0] % 2 == 1:
                if position[1] == (position[0] + 1) / 2:
                    player_horizontal_count += 1
                else:
                    player_horizontal_count += abs(position[1] - (position[0] + 1) / 2) - 1
            else:
                if position[1] == (position[0] / 2) or (position[0] / 2 + 1):
                    player_horizontal_count += 0.5
                else:
                    player_horizontal_count += abs(position[1] - (position[0] + 1) / 2) - 1

        opponent_horizontal_count = 0
        for position in opponent_status:
            if position[0] % 2 == 1:
                if position[1] == (position[0] + 1) / 2:
                    opponent_horizontal_count += 1
                else:
                    opponent_horizontal_count += abs(position[1] - (position[0] + 1) / 2) - 1
            else:
                if position[1] == (position[0] / 2) or (position[0] / 2 + 1):
                    opponent_horizontal_count += 0.5
                else:
                    opponent_horizontal_count += abs(position[1] - (position[0] + 1) / 2) - 1

        # final calculation
        if player == 1:
            if player_vertical_count == 30:                                         # you win!
                return 1000
            if opponent_vertical_count == 170:                                      # you lose!
                return -1000
            else:
                return 400 - (player_vertical_count + opponent_vertical_count) + (  # the more the better
                        opponent_horizontal_count - player_horizontal_count) / 2
        else:
            if player_vertical_count == 170:
                return 1000
            if opponent_vertical_count == 30:
                return -1000
            else:
                return (player_vertical_count + opponent_vertical_count) + (        # the more the better
                        opponent_horizontal_count - player_horizontal_count) / 2

# three global variables( out of the class)
cnt = 0
repeat = 0
q = []

from queue import PriorityQueue

        ### END CODE HERE ###


class FakeNN(Agent): # fake neutral network
    def __init__(self,game):
        super(FakeNN, self).__init__(game)
        from loss_function import converse_state_to_board
        from  NNmodel import StateNet
        import torch
        
        self.judge_net = StateNet().cuda()
        self.judge_net = torch.nn.DataParallel(self.judge_net)
        weights = torch.load('NNmodel.pth.tar')
        self.judge_net.load_state_dict(weights)
        self.judge_net.eval()

        self.converse_state_to_board = converse_state_to_board
    def getAction(self, state):
        
        
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        ### START CODE HERE ###

        global staticDepth, cnt, repeat  # store the initial value for depth for minimax
        depth = 2                        # starting from 2
        staticDepth = depth              # store original depth
        memory = 20                      # breadth for each layer, max is 42
        board = state[1]
        player_status = board.getPlayerPiecePositions(player)

        temp = (player_status in q)
        q.append(player_status)

        cnt += 1

        if cnt >= 3 and temp:            # in case of "stuck" situation, use "greedy"
            q.remove(q[0])
            repeat += 1
            if repeat == 2:              # in case of repeated "stuck" situation
                self.action = random.choice(legal_actions)
            else:
                if player == 1:          # playing from bottom to top, hence later vertical value is smaller
                    max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
                    max_actions = [action for action in legal_actions if
                                    action[0][0] - action[1][0] == max_vertical_advance_one_step]
                else:                    # playing from top to bottom, hence later vertical value is larger
                    max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
                    max_actions = [action for action in legal_actions if
                                    action[1][0] - action[0][0] == max_vertical_advance_one_step]
                self.action = random.choice(max_actions)

        else:
            if cnt >= 3:
                q.remove(q[0])
            repeat = 0
            v = -float('inf')

            order = PriorityQueue()      # search with preference
            for action in legal_actions:
                order.put((-(3 - 2 * player) * (action[0][0] - action[1][0]), action))
            order_next = PriorityQueue()

            while True:
                count = 0
                while (not order.empty()) and (memory > count):
                    action = order.get()[1]
                    if self.evaluation(self.game.succ(state, action), player) == 1000:
                        self.action = action
                        break
                    count += 1
                    v_next = self.minimaxValue(player, self.game, self.game.succ(state, action), depth, v, float('inf'),
                                            memory)
                    order_next.put((-v_next, action))
                    if v_next > v:
                        v = v_next
                        self.action = action

                depth += 1
                staticDepth = depth
                del order
                order = PriorityQueue()
                while not order_next.empty():
                    order.put(order_next.get())

    # minimax algorithm
    def minimaxValue(self, player, game, state, depth, alpha, beta, memory):

        if depth == 0:
            return self.evaluation(state, player)
        else:
            depth -= 1

        if (staticDepth - depth) % 2 == 1:
            if self.evaluation(state, player) == 1000:
                return 1000

            v = float('inf')
            order = PriorityQueue()
            for action in game.actions(state):
                order.put(((3 - 2 * player) * (action[0][0] - action[1][0]), action))

            count = 0
            while (not order.empty()) and memory > count:
                action = order.get()[1]
                count += 1
                v = min(v, self.minimaxValue(player, game, game.succ(state, action), depth, alpha, beta, memory))
                if v <= alpha: return v
                beta = min(beta, v)
            # print("depth:", depth)
            return v

        else:
            if self.evaluation(state, player) == -1000:
                return -1000

            v = -float('inf')
            order = PriorityQueue()
            for action in game.actions(state):
                order.put((-(3 - 2 * player) * (action[0][0] - action[1][0]), action))

            count = 0
            while (not order.empty()) and memory > count:
                action = order.get()[1]
                count += 1
                v = max(v, self.minimaxValue(player, game, game.succ(state, action), depth, alpha, beta, memory))
                if v >= beta: return v
                alpha = max(alpha, v)
            return v

    # heuristic evaluation
    def evaluation(self, state, player):  # this function returns a number as the evaluation value of a given state

        board = self.converse_state_to_board((state[1]), self.game.player(state)) # [3,10,10]

        import torch
        board = (torch.from_numpy(board)).unsqueeze(0).float()

        result = self.judge_net(board)
        

        return result

        ### END CODE HERE ###