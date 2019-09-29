import random, re, datetime
from queue import PriorityQueue
from queue import Queue

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
        else:            # playing from top to bottom, hence later vertical value is larger
            max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[1][0] - action[0][0] == max_vertical_advance_one_step]
        self.action = random.choice(max_actions)


cnt = 0
repeat = 0
q = Queue()


class TeamNameMinimaxAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        ### START CODE HERE ###


        # implement minimax
        global staticDepth       # store the initial value for depth for minimax
        depth = 2                # starting from 2
        staticDepth = depth

        global cnt, repeat
        if cnt >= 4:
            if q.get() == state:  # in case of "stuck" situation, use "greedy"
                player = self.game.player(state)
                repeat += 1
                if repeat == 2:
                    self.action = random.choice(legal_actions)# in case of repeated "stuck" situation
                else:
                    if player == 1:  # playing from bottom to top, hence later vertical value is smaller
                        max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
                        max_actions = [action for action in legal_actions if
                                   action[0][0] - action[1][0] == max_vertical_advance_one_step]
                    else:  # playing from top to bottom, hence later vertical value is larger
                        max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
                        max_actions = [action for action in legal_actions if
                                   action[1][0] - action[0][0] == max_vertical_advance_one_step]
                    self.action = random.choice(max_actions)



            else:
                repeat = 0
                memory = 50  # breadth for each layer, max is 42
                v = -float('inf')

                order = PriorityQueue()  # search with preference
                for action in legal_actions:
                    order.put((-(3 - 2 * player) * (action[0][0] - action[1][0]), action))
                order_next = PriorityQueue()

                while True:
                    count = 0
                    while (not order.empty()) and (memory > count):
                        action = order.get()[1]
                        if evaluation(self.game.succ(state, action), player) == 1000:
                            self.action = action
                            break
                        count += 1
                        v_next = minimaxValue(player, self.game, self.game.succ(state, action), depth, v, float('inf'),
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

        q.put(state)
        cnt += 1


def minimaxValue(player, game, state, depth, alpha, beta, memory):
    if depth == 0:
        return evaluation(state, player)
    else:
        depth -= 1

    if (staticDepth - depth) % 2 == 1:
        if evaluation(state, player) == 1000:
            return 1000

        v = float('inf')
        order = PriorityQueue()
        for action in game.actions(state):
            order.put(((3 - 2 * player) * (action[0][0] - action[1][0]), action))

        count = 0
        while (not order.empty()) and memory > count:
            action = order.get()[1]
            count += 1
            v = min(v, minimaxValue(player, game, game.succ(state, action), depth, alpha, beta, memory))
            if v <= alpha: return v
            beta = min(beta, v)
        return v

    else:
        if evaluation(state, player) == -1000:
            return -1000

        v = -float('inf')
        order = PriorityQueue()
        for action in game.actions(state):
            order.put((-(3 - 2 * player) * (action[0][0] - action[1][0]), action))

        count = 0
        while (not order.empty()) and memory > count:
            action = order.get()[1]
            count += 1
            v = max(v, minimaxValue(player, game, game.succ(state, action), depth, alpha, beta, memory))
            if v >= beta: return v
            alpha = max(alpha, v)
        return v


def evaluation(state, player):  # this function returns a number as the evaluation value of a given state
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
                player_horizontal_count += abs((position[1] - (position[0] + 1) / 2)) - 1
        else:
            if position[1] == (position[0] / 2) or (position[0] / 2 + 1):
                player_horizontal_count += 0.5
            else:
                player_horizontal_count += abs(position[1] - (position[0] + 1) / 2) - 1

    opponent_horizontal_count = 0
    for position in opponent_status:
        if position[0] % 2 == 1:
            if position[1] == (position[0] + 1) / 2:
                player_horizontal_count += 1
            else:
                player_horizontal_count += abs((position[1] - (position[0] + 1) / 2)) - 1
        else:
            if position[1] == (position[0] / 2) or (position[0] / 2 + 1):
                player_horizontal_count += 0.5
            else:
                player_horizontal_count += abs(position[1] - (position[0] + 1) / 2) - 1

    # final calculation
    if player == 1:
        if player_vertical_count == 30:  # you win!
            return 1000
        if opponent_vertical_count == 170:  # you lose!
            return -1000
        else:
            return 400 - (player_vertical_count + opponent_vertical_count) + ( # the more the better
                        opponent_horizontal_count - player_horizontal_count) / 2
    else:
        if player_vertical_count == 170:
            return 1000
        if opponent_vertical_count == 30:
            return -1000
        else:
            return (player_vertical_count + opponent_vertical_count) + (       # the more the better
                        opponent_horizontal_count - player_horizontal_count) / 2

        ### END CODE HERE ###
