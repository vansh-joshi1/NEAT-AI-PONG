# Team: Vansh Joshi, Om Patel, Mathew Phan, Sarvvesh Vindokumar

from pong.game import Game
import pygame
import neat
import os
import time
import pickle


class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle

    def test_ai(self, net):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)  # 60 FPS game loop
            game_info = self.game.loop()

            # Handle quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            # AI decision making - uses paddle position, ball distance and ball height
            output = net.activate((self.right_paddle.y, abs(
                self.right_paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))

            # Move AI paddle based on neural network output
            if decision == 1:  # AI moves up
                self.game.move_paddle(left=False, up=True)
            elif decision == 2:  # AI moves down
                self.game.move_paddle(left=False, up=False)

            # Human paddle controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            elif keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)

            self.game.draw(draw_score=True)
            pygame.display.update()

    def train_ai(self, genome1, genome2, config, draw=False):
        run = True
        start_time = time.time()

        # Create neural networks from genomes
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1 = genome1
        self.genome2 = genome2

        max_hits = 50  # Maximum rally length before ending game

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            game_info = self.game.loop()
            self.move_ai_paddles(net1, net2)

            if draw:
                self.game.draw(draw_score=False, draw_hits=True)

            pygame.display.update()

            # End conditions: point scored or max hits reached
            duration = time.time() - start_time
            if game_info.left_score == 1 or game_info.right_score == 1 or game_info.left_hits >= max_hits:
                self.calculate_fitness(game_info, duration)
                break

        return False

    def move_ai_paddles(self, net1, net2):
        # Move both AI paddles based on their neural network outputs
        players = [(self.genome1, net1, self.left_paddle, True), (self.genome2, net2, self.right_paddle, False)]
        for (genome, net, paddle, left) in players:
            # Neural network input: paddle Y position, distance to ball, ball Y position
            output = net.activate(
                (paddle.y, abs(paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))

            # Apply fitness penalties for actions
            valid = True
            if decision == 0:  # Don't move - slightly discourage inaction
                genome.fitness -= 0.01
            elif decision == 1:  # Move up
                valid = self.game.move_paddle(left=left, up=True)
            else:  # Move down
                valid = self.game.move_paddle(left=left, up=False)

            # Penalize invalid moves (hitting screen boundaries)
            if not valid:
                genome.fitness -= 1

    def calculate_fitness(self, game_info, duration):
        # Calculate fitness scores for both genomes based on hits and game duration
        self.genome1.fitness += game_info.left_hits + duration
        self.genome2.fitness += game_info.right_hits + duration


def eval_genomes(genomes, config):
    # Evaluate all genomes by having them play against each other.
    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")

    # Each genome plays against all genomes that come after it
    for i, (genome_id1, genome1) in enumerate(genomes):
        # Progress indicator
        print(round(i / len(genomes) * 100), end = " ")  
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i + 1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            pong = PongGame(win, width, height)

            force_quit = pong.train_ai(genome1, genome2, config, draw=True)
            if force_quit:
                quit()


def run_neat(config):
    # Run the NEAT algorithm to train the AI
    # Load from checkpoint or create new population
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-25')  # Load from checkpoint
    # p = neat.Population(config)  # Start new training

    # Add reporters for training progress
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    # Run for 50 generations and save the winner
    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):
    # Load and test the best trained network against a human player
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")
    pong = PongGame(win, width, height)
    pong.test_ai(winner_net)


if __name__ == '__main__':
    # Load NEAT config and either train or test the AI
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # run_neat(config)  # Train AI
    test_best_network(config)  # Play against trained AI