"""
IS 211 Assignment 8 - Game of Pig with Factory, Proxy, and Computer Strategy
"""

import random
import time
import argparse

random.seed(0)

class Die:
    def roll(self):
        return random.randint(1, 6)

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_total = 0

    def add_to_turn_total(self, value):
        self.turn_total += value

    def reset_turn_total(self):
        self.turn_total = 0

    def bank_score(self):
        self.score += self.turn_total
        self.reset_turn_total()

    def decide_action(self):
        return input(f"{self.name}, your total score is {self.score}. Turn total is {self.turn_total}. Roll (r) or Hold (h)? ").strip().lower()

class ComputerPlayer(Player):
    def decide_action(self):
        threshold = min(25, 100 - self.score)
        if self.turn_total >= threshold:
            print(f"{self.name} decides to hold (turn total {self.turn_total} >= threshold {threshold}).")
            return 'h'
        else:
            print(f"{self.name} decides to roll.")
            return 'r'

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type.lower() == "computer":
            return ComputerPlayer(name)
        return Player(name)

class Game:
    def __init__(self, player1_type="human", player2_type="human"):
        self.players = [
            PlayerFactory.create_player(player1_type, "Player 1"),
            PlayerFactory.create_player(player2_type, "Player 2")
        ]
        self.die = Die()
        self.current_player_idx = 0

    def play_turn(self):
        player = self.players[self.current_player_idx]
        player.reset_turn_total()
        print(f"\n--- {player.name}'s Turn ---")

        while True:
            decision = player.decide_action()
            
            if decision == 'r':
                roll_val = self.die.roll()
                print(f"{player.name} rolled a {roll_val}.")
                
                if roll_val == 1:
                    print(f"Oops! Rolled a 1. {player.name} scores nothing this turn.")
                    player.reset_turn_total()
                    break
                else:
                    player.add_to_turn_total(roll_val)
                    print(f"Current turn total: {player.turn_total}")
            elif decision == 'h':
                player.bank_score()
                print(f"{player.name} holds. New total score: {player.score}")
                break
            else:
                print("Invalid input. Please enter 'r' to roll or 'h' to hold.")

    def check_winner(self):
        for player in self.players:
            if player.score >= 100:
                return player
        return None

    def start(self):
        print("=== Welcome to the Game of Pig! ===")
        while True:
            self.play_turn()
            
            winner = self.check_winner()
            if winner:
                print(f"\n*** {winner.name} wins with a score of {winner.score}! ***")
                return winner
                
            self.current_player_idx = 1 - self.current_player_idx

class TimedGameProxy:
    def __init__(self, player1_type="human", player2_type="human"):
        self.game = Game(player1_type, player2_type)
        self.start_time = None

    def start(self):
        print("=== Welcome to the Timed Game of Pig (1 Minute Limit) ===")
        self.start_time = time.time()
        
        while True:
            elapsed = time.time() - self.start_time
            if elapsed >= 60:
                print("\n⏰ Time's up! One minute has elapsed.")
                return self.get_timed_winner()

            player = self.game.players[self.game.current_player_idx]
            player.reset_turn_total()
            print(f"\n--- {player.name}'s Turn (Time elapsed: {int(elapsed)}s) ---")

            while True:
                if time.time() - self.start_time >= 60:
                    print("\n⏰ Time's up during turn!")
                    return self.get_timed_winner()

                decision = player.decide_action()
                
                if decision == 'r':
                    roll_val = self.game.die.roll()
                    print(f"{player.name} rolled a {roll_val}.")
                    
                    if roll_val == 1:
                        print(f"Oops! Rolled a 1. {player.name} scores nothing this turn.")
                        player.reset_turn_total()
                        break
                    else:
                        player.add_to_turn_total(roll_val)
                        print(f"Current turn total: {player.turn_total}")
                elif decision == 'h':
                    player.bank_score()
                    print(f"{player.name} holds. New total score: {player.score}")
                    break
                else:
                    print("Invalid input. Please enter 'r' to roll or 'h' to hold.")

            winner = self.game.check_winner()
            if winner:
                print(f"\n*** {winner.name} wins with a score of {winner.score}! ***")
                return winner
                
            self.game.current_player_idx = 1 - self.game.current_player_idx

    def get_timed_winner(self):
        p1, p2 = self.game.players[0], self.game.players[1]
        print(f"Final Scores -> {p1.name}: {p1.score}, {p2.name}: {p2.score}")
        if p1.score > p2.score:
            print(f"\n*** {p1.name} wins on points! ***")
            return p1
        elif p2.score > p1.score:
            print(f"\n*** {p2.name} wins on points! ***")
            return p2
        else:
            print("\n*** It's a tie! ***")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play the Game of Pig.")
    parser.add_argument("--player1", type=str, default="human", help="Player 1 type: human or computer")
    parser.add_argument("--player2", type=str, default="human", help="Player 2 type: human or computer")
    parser.add_argument("--timed", action="store_true", help="Activate timed game proxy (1 minute limit)")
    args = parser.parse_args()

    if args.timed:
        game_runner = TimedGameProxy(args.player1, args.player2)
    else:
        game_runner = Game(args.player1, args.player2)
        
    game_runner.start()
