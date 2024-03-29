#!/usr/bin/env python3
from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
import math
import time



class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):
    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()
        self.start_time = 0
        self.cache = dict()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            self.start_time = time.time()
            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        """
        Find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: Either "stay", "left", "right", "up" or "down"
        :rtype: str
        """


        # Geting the next childern in the node tree
        children = initial_tree_node.compute_and_get_children()

        output_list = []
        depth = 0

        # try to go as deep into the game tree as possible(time allows us)
        while True:
            try:
                for child in children:
                    output = self.minimax(
                        child, depth + 1, float("-inf"), float("inf"), "B"
                    )

                    output_list.append(output)

            except Exception as _:
                break
        
        # Get the move that leads to the maximum child(node)
        max_socre = max(output_list)
        move = children[output_list.index(max_socre)].move

        return ACTION_TO_STR[move]

    def minimax(self, tree_node, depth, alpha, beta, player):
        """
        minimax algo with alpha beta pruning.
        :param tree_node: The current game tree node
        :type tree_node: game_tree.Node
        :param depth: The depth that the minimax algo look into
        :type depth: int
        :param alpha: The current best value achievable for player A
        :param beta: The current best value achievable for player B
        :type alpha, beta: float
        :param player: The current player
        :type player: char
        :param start_time: The time recorded when the function is called
        :return: minimax value of state
        :rtype: float
        """
        if time.time() - self.start_time > 0.061:
            raise TimeoutError

        hook_pos = tree_node.state.get_hook_positions()
        fish_pos = tree_node.state.get_fish_positions()
        
        # use hook position and fish position as a key of hash table. 
        # TODO also include the depth of the interation in the key
        key = str(hook_pos) + str(fish_pos)

        if self.cache.get(key) != None:
            return self.cache[key]

        # get the next possible states
        next_children = tree_node.compute_and_get_children()
        # check for the terminal state
        if depth == 0 or len(next_children) == 0:
            return self.heuristic(tree_node.state)

        elif player == "A":
            v = float("-inf")
            for child in next_children:
                v = max(
                    v,
                    self.minimax(child, depth - 1, alpha, beta, "B"),
                )
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
        else:
            v = float("inf")
            for child in next_children:
                v = min(
                    v,
                    self.minimax(child, depth - 1, alpha, beta, "A"),
                )
                beta = min(beta, v)
                if beta <= alpha:
                    break

        self.cache[key] = v

        return v

    def heuristic(self, state):
        """
        Heuristic function that calculates the sum of difference scores between player 0 and 1 and
        the best distance to the most valuable fish
        :param state: current game state
        :type state: game_tree.State
        """
        

        # This heuristic may look unusual, since it calculates the score difference base on the palyer's turn.
        # I could not explain why but this heuristic gave a better score on kattis(+2) than the one that 
        # only calcuates max_player_score - min_player_score.

        # some values were chosen to maximize the requred score on kattis (e.x. math.pow(dis, 12))

        hook_pos = state.get_hook_positions()[state.get_player()]

        fish_scores = []
        all_fish = state.get_fish_positions()
        keys = all_fish.keys()
        scores = state.get_fish_scores()

        max_player, min_player = state.get_player_scores()
        if state.get_player() == 0:
            score_diff = max_player - min_player
        else:
            score_diff = min_player - max_player
        for key in keys:

            current_fish_score = scores[key]
            dis = self.distance(hook_pos, all_fish[key])

            if dis == 0 and state.fish_scores[key] > 0:
                return float("inf")

            if len(all_fish) == 1:
                return current_fish_score / math.pow(dis, 12)

            fish_scores.append(current_fish_score / math.pow(dis, 12))

        if len(fish_scores) == 0:
            best_fish = 0
        else:
            best_fish = max(fish_scores)

        return 10 * score_diff + best_fish

    def distance(self, cor1, cor2):
        """
        Helper function for calculating the distance betweeb two coordinates
        :param cor1: tuple of x,y coordinate
        :param cor2: tuple of x,y coordinate
        """
        x = cor2[0] - cor1[0]
        x = min(x, 20 - x)
        answer = math.sqrt(math.pow(x, 2) + math.pow(cor2[1] - cor1[1], 2))
        return answer

