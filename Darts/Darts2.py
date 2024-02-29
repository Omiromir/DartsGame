import pygame
import random
import sys
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_RED = (255, 100, 100)
LIGHT_GREEN = (100, 255, 100)
LIGHT_BLUE = (100, 100, 255)
YELLOW = (255, 255, 0)
DARK_YELLOW = (236, 181, 0)

class DartGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Darts Game")

        # Load background music
        pygame.mixer.music.load("resources/bg_music.mp3")
        pygame.mixer.music.set_volume(0.009)

        # Load congratulation sound
        self.congratulation_sound = pygame.mixer.Sound("resources/congrat.mp3")

        self.players = ["Player 1", "Player 2"]
        self.current_player = 0
        self.total_scores = [0, 0]
        self.round_score = 0
        self.remaining_moves = 3
        self.target_score = 50
        self.new_round_button_enabled = False

        self.font = pygame.font.SysFont(None, 30)

        # Load hearts image and adjust its size
        self.heart_image = pygame.transform.scale(pygame.image.load("resources/heart.png"), (30, 30))

        self.reset_round_button = pygame.Rect(50, 500, 150, 50)
        self.reset_game_button = pygame.Rect(600, 500, 160, 50)
        self.easy_button = pygame.Rect(200, 500, 100, 50)
        self.medium_button = pygame.Rect(325, 500, 100, 50)
        self.hard_button = pygame.Rect(450, 500, 100, 50)
        self.back_button = pygame.Rect(700, 20, 70, 35)

        self.create_scoring_zones()

        # Dart throwing variables
        self.dart_start_x = 400
        self.dart_start_y = 550
        self.dart_x = self.dart_start_x
        self.dart_y = self.dart_start_y
        self.dart_angle = 45
        self.power_meter = 0
        self.accuracy = 10

        self.throwing_dart = False

        # Dartboard movement variables
        self.dartboard_speed = 3
        self.dartboard_direction = -1
        self.dartboard_range = 80
        self.dartboard_x = 400

        # Difficulty levels
        self.difficulty = "medium"
        self.difficulty_speeds = {"easy": 4, "medium": 8, "hard": 12}
        self.dartboard_speed = self.difficulty_speeds[self.difficulty]


        pygame.mixer.music.play(loops=-1)

        self.welcome_bg = pygame.transform.scale(pygame.image.load("resources/bg_welcome1.jpg"), (800, 600))
        self.main_bg = pygame.transform.scale(pygame.image.load("resources/bg_main.jpg"), (800, 600))
        self.end_bg = pygame.transform.scale(pygame.image.load("resources/bg_ending.jpg"), (800, 600))

    def create_scoring_zones(self):
        self.scoring_zones = [
            (150, LIGHT_RED),
            (100, LIGHT_GREEN),
            (50, LIGHT_BLUE),
            (15, DARK_YELLOW),
        ]

    def welcome_screen(self):
        # Display welcome message
        self.screen.blit(self.welcome_bg, (0, 0))
        welcome_text = self.font.render("Welcome to Darts Game!", True, DARK_YELLOW)
        instructions_text = self.font.render("Click to choose difficulty level and start the game", True, DARK_YELLOW)
        self.screen.blit(welcome_text, (250, 250))
        self.screen.blit(instructions_text, (140, 300))

        # Draw difficulty level buttons
        pygame.draw.rect(self.screen, YELLOW, self.easy_button)
        pygame.draw.rect(self.screen, YELLOW, self.medium_button)
        pygame.draw.rect(self.screen, YELLOW, self.hard_button)

        easy_text = self.font.render("Easy", True, BLACK)
        medium_text = self.font.render("Medium", True, BLACK)
        hard_text = self.font.render("Hard", True, BLACK)

        self.screen.blit(easy_text, (self.easy_button.x + 25, self.easy_button.y + 15))
        self.screen.blit(medium_text, (self.medium_button.x + 15, self.medium_button.y + 15))
        self.screen.blit(hard_text, (self.hard_button.x + 25, self.hard_button.y + 15))




        pygame.display.flip()

        # Wait for the user to click to start the game
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.easy_button.collidepoint(x, y):
                        self.difficulty = "easy"
                        self.dartboard_speed = self.difficulty_speeds[self.difficulty]
                        waiting = False
                    elif self.medium_button.collidepoint(x, y):
                        self.difficulty = "medium"
                        self.dartboard_speed = self.difficulty_speeds[self.difficulty]
                        waiting = False
                    elif self.hard_button.collidepoint(x, y):
                        self.difficulty = "hard"
                        self.dartboard_speed = self.difficulty_speeds[self.difficulty]
                        waiting = False


    def throw_dart(self):
        if self.remaining_moves > 0:
            dart_result = self.calculate_dart_result(self.dart_x, self.dart_y)

            self.round_score += dart_result

            self.remaining_moves -= 1

            if self.remaining_moves == 0:
                self.new_round_button_enabled = True

        # Reset dart position to start position
        self.dart_x = self.dart_start_x
        self.dart_y = self.dart_start_y

    def calculate_dart_result(self, x, y):
        # Calculate the distance between the dart and the center of the dartboard
        distance_to_center = ((x - self.dartboard_x) ** 2 + (y - 300) ** 2) ** 0.5

        if distance_to_center <= 15:
            return 15
        # Determine the points based on the distance from the center
        if distance_to_center <= 50:
            points = random.randint(7, 9)  # Blue zone
        elif distance_to_center <= 100:
            points = random.randint(4, 6)  # Green zone
        elif distance_to_center <= 150:
            points = random.randint(1, 3)  # Red zone
        else:
            points = 0

        return points

    def reset_round(self):
        self.total_scores[self.current_player] += self.round_score

        if self.total_scores[self.current_player] >= self.target_score:
            self.end_game()
        else:
            self.round_score = 0
            self.remaining_moves = 3
            self.switch_player()
            self.new_round_button_enabled = False
            self.dart_x = self.dart_start_x
            self.dart_y = self.dart_start_y

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def reset_game(self):
        self.current_player = 0
        self.total_scores = [0, 0]
        self.round_score = 0
        self.remaining_moves = 3
        self.new_round_button_enabled = False

    def end_game(self):
        winner = max(enumerate(self.total_scores), key=lambda x: x[1])[0]
        print(winner)

        winner_text = f"Player {winner + 1} wins!"
        self.font_large = pygame.font.SysFont(None, 50)

        congrats_text = self.font_large.render(winner_text, True, DARK_YELLOW)

        pygame.mixer.music.stop()

        self.congratulation_sound.play()

        play_again_button = pygame.Rect(200, 400, 150, 50)
        quit_button = pygame.Rect(450, 400, 150, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if play_again_button.collidepoint(x, y):
                        self.congratulation_sound.stop()
                        self.reset_game()
                        pygame.mixer.music.play(loops=-1)
                        return  # Return to the main loop
                    elif quit_button.collidepoint(x, y):
                        sys.exit()

            self.screen.blit(self.end_bg, (0, 0))
            self.screen.blit(congrats_text, (280, 300))

            pygame.draw.rect(self.screen, YELLOW, play_again_button)
            pygame.draw.rect(self.screen, YELLOW, quit_button)

            play_again_text = self.font.render("Play Again", True, BLACK)
            quit_text = self.font.render("Quit", True, BLACK)

            self.screen.blit(play_again_text, (220, 415))
            self.screen.blit(quit_text, (500, 415))

            pygame.display.flip()

    def draw(self):
        self.screen.blit(self.main_bg, (0, 0))

        # Update dartboard position
        self.dartboard_x += self.dartboard_speed * self.dartboard_direction
        if self.dartboard_x <= 400 - self.dartboard_range:
            self.dartboard_direction = 1
        elif self.dartboard_x >= 400 + self.dartboard_range:
            self.dartboard_direction = -1

        # Draw scoring zones with different colors
        for i, (zone_radius, zone_color) in enumerate(self.scoring_zones):
            pygame.draw.circle(self.screen, zone_color, (self.dartboard_x, 300), zone_radius)

        if self.new_round_button_enabled:
            pygame.draw.rect(self.screen, YELLOW, self.reset_round_button)
        else:
            pygame.draw.rect(self.screen, LIGHT_RED, self.reset_round_button)

        pygame.draw.rect(self.screen, YELLOW, self.reset_game_button)

        text = self.font.render("New Round", True, BLACK)
        self.screen.blit(text, (self.reset_round_button.x + 25, self.reset_round_button.y + 15))

        text = self.font.render("Reset Game", True, BLACK)
        self.screen.blit(text, (self.reset_game_button.x + 25, self.reset_game_button.y + 15))

        text = self.font.render(f"Player: {self.players[self.current_player]}", True, BLACK)
        self.screen.blit(text, (20, 20))

        text = self.font.render(f"Round Score: {self.round_score}", True, BLACK)
        self.screen.blit(text, (20, 50))

        text = self.font.render(f"Total Score {self.players[0]}: {self.total_scores[0]}", True, BLACK)
        self.screen.blit(text, (20, 80))

        text = self.font.render(f"Total Score {self.players[1]}: {self.total_scores[1]}", True, BLACK)
        self.screen.blit(text, (20, 110))

        # Draw hearts representing remaining moves under the total scores
        for i in range(self.remaining_moves):
            heart_x = 20 + i * (self.heart_image.get_width() + 5)  # Adjust the spacing between hearts
            heart_y = 140
            self.screen.blit(self.heart_image, (heart_x, heart_y))

        # Draw power meter
        pygame.draw.rect(self.screen, RED, (10, 500, 30, -self.power_meter))

        # Draw dart circle only if there are remaining moves
        if self.remaining_moves > 0:
            pygame.draw.circle(self.screen, BLACK, (self.dart_x, self.dart_y), 10)

        # Draw back button
        pygame.draw.rect(self.screen, YELLOW, self.back_button)
        back_text = self.font.render("Back", True, BLACK)
        self.screen.blit(back_text, (self.back_button.x + 10, self.back_button.y + 8))

        pygame.display.flip()

    def run(self):
        self.welcome_screen()  # Display welcome screen before starting the game
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        if self.reset_round_button.collidepoint(x, y) and self.new_round_button_enabled:
                            self.reset_round()
                        elif self.reset_game_button.collidepoint(x, y):
                            self.reset_game()
                        elif self.back_button.collidepoint(x, y):
                            self.welcome_screen()
                        else:
                            self.throwing_dart = True
                            self.power_meter = 0
                            self.accuracy = random.randint(5, 20)  # Adjust accuracy
                elif event.type == pygame.MOUSEMOTION:
                    if self.throwing_dart:
                        self.dart_x, self.dart_y = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.throwing_dart:
                        self.throwing_dart = False
                        self.throw_dart()

            if self.throwing_dart:
                self.power_meter += 1
                # Apply power and accuracy to the dart position
                self.dart_x += int(math.cos(math.radians(self.dart_angle)) * self.power_meter * 0.1)
                self.dart_y -= int(math.sin(math.radians(self.dart_angle)) * self.power_meter * 0.1)
                self.dart_angle += random.randint(-self.accuracy, self.accuracy)

            self.draw()
            clock.tick(45)

if __name__ == "__main__":
    game = DartGame()
    game.run()
