class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0
        self.scores = [0, 0]
        
    def get_scores(self):
        return self.scores

    def update_scores(self, player):
        self.scores[player] += 1
        return self.scores
        

    def get_player_move(self, p):
        """

        :param p: [0, 1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        if p1 == p2:
            return -1

        winning_conditions = {
        "R": "S",  # Rock beats Scissors
        "S": "P",  # Scissors beats Paper
        "P": "R"   # Paper beats Rock
        }

         # Check if player 1 wins
        if winning_conditions.get(p1) == p2:  
            return 0  # Player 1 scores

        # Check if player 2 scores
        if winning_conditions.get(p2) == p1:
            return 1  # Player 2 scores


    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
        
    def check_winner(self):
        if self.scores[0] >= 3:
            return 0
        elif self.scores[1] >= 3:
            return 1
        else:
            return -1
        
    
