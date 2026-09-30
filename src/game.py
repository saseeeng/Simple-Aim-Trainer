import time
import pygame

from target import Target
from stats import Stats
import target


class Game:
    WIDTH = 1000
    HEIGHT = 700

    GAME_TIME = 30

    TARGET_COUNT = 5
    TARGET_LIFETIME = 4.0

    BACKGROUND_COLOR = (25, 25, 25)
    UI_COLOR = (45, 45, 45)
    WHITE = (245, 245, 245)
    GRAY = (170, 170, 170)
    GREEN = (70, 200, 120)
    RED = (220, 70, 70)
    YELLOW = (240, 200, 70)

    def __init__(self, difficulty="Normal"):

        self.difficulty = difficulty

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )

        pygame.display.set_caption(
            "Python Aim Trainer"
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 26)
        self.large_font = pygame.font.Font(None, 64)
        self.title_font = pygame.font.Font(None, 80)

        self.stats = Stats()

        self.targets = [
            self.create_target()
            for _ in range(self.TARGET_COUNT)
        ]

        self.running = True
        self.game_finished = False

        self.start_time = None
        self.last_target_time = None

    def get_target_radius(self):
        """Return target size based on difficulty."""

        sizes = {
            "Easy": 40,
            "Normal": 30,
            "Hard": 20
        }

        return sizes.get(
            self.difficulty,
            30
        )
    
    def create_target(self):
        return Target(
            self.WIDTH,
            self.HEIGHT,
            self.get_target_radius(),
            self.TARGET_LIFETIME
        )
    
    def start(self):
        """Start a new game."""

        self.stats.reset()

        self.targets = [
            self.create_target()
            for _ in range(self.TARGET_COUNT)
        ]
        self.start_time = time.time()
        self.last_target_time = self.start_time

        self.game_finished = False

    def get_remaining_time(self):
        """Return remaining game time."""

        if self.start_time is None:
            return self.GAME_TIME

        elapsed = time.time() - self.start_time

        return max(
            0,
            self.GAME_TIME - elapsed
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for index, target in enumerate(self.targets):
                if target.is_clicked(mouse_x, mouse_y):
                    reaction_time = time.time() - self.last_target_time
                    self.stats.register_hit(reaction_time)
                    self.targets[index] = self.create_target()
                    self.last_target_time = time.time()
                    break
            else:
                self.stats.register_miss()

    def update(self):
        """Update the game state."""

        if self.game_finished:
            return
        
        self.targets = [
            target for target in self.targets
            if not target.is_expired()
        ]
        while len(self.targets) < self.TARGET_COUNT:
            self.targets.append(self.create_target())

        remaining_time = self.get_remaining_time()

        if remaining_time <= 0:

            self.game_finished = True

            self.stats.save_score(
                self.difficulty,
                self.GAME_TIME
            )

    def draw_header(self):
        """Draw the top information bar."""

        pygame.draw.rect(
            self.screen,
            self.UI_COLOR,
            (0, 0, self.WIDTH, 70)
        )

        remaining_time = self.get_remaining_time()

        # Time
        time_text = self.font.render(
            f"Time: {remaining_time:.1f}",
            True,
            self.WHITE
        )

        self.screen.blit(
            time_text,
            (20, 20)
        )

        # Hits
        hits_text = self.font.render(
            f"Hits: {self.stats.hits}",
            True,
            self.GREEN
        )

        self.screen.blit(
            hits_text,
            (190, 20)
        )

        # Misses
        misses_text = self.font.render(
            f"Misses: {self.stats.misses}",
            True,
            self.RED
        )

        self.screen.blit(
            misses_text,
            (310, 20)
        )

        # Accuracy
        accuracy_text = self.font.render(
            f"Accuracy: {self.stats.get_accuracy():.1f}%",
            True,
            self.WHITE
        )

        self.screen.blit(
            accuracy_text,
            (450, 20)
        )

        # Score
        score_text = self.font.render(
            f"Score: {self.stats.score}",
            True,
            self.YELLOW
        )

        self.screen.blit(
            score_text,
            (700, 20)
        )

        # Difficulty
        difficulty_text = self.small_font.render(
            self.difficulty,
            True,
            self.GRAY
        )

        self.screen.blit(
            difficulty_text,
            (880, 25)
        )

    def draw(self):
        """Draw the game."""

        self.screen.fill(
            self.BACKGROUND_COLOR
        )

        self.draw_header()

        if not self.game_finished:
            for target in self.targets:
                target.draw(self.screen)

    def draw_game_over(self):
        """Draw the final statistics screen."""

        self.screen.fill(
            self.BACKGROUND_COLOR
        )

        title = self.title_font.render(
            "GAME OVER",
            True,
            self.WHITE
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(self.WIDTH // 2, 150)
            )
        )

        stats = [
            f"Score: {self.stats.score}",
            f"Hits: {self.stats.hits}",
            f"Misses: {self.stats.misses}",
            f"Accuracy: {self.stats.get_accuracy():.1f}%",
            (
                "Average Reaction: "
                f"{self.stats.get_average_reaction_time() * 1000:.0f} ms"
            )
        ]

        y = 260

        for text in stats:

            rendered = self.font.render(
                text,
                True,
                self.WHITE
            )

            self.screen.blit(
                rendered,
                rendered.get_rect(
                    center=(self.WIDTH // 2, y)
                )
            )

            y += 50

        instruction = self.small_font.render(
            "Press R to play again or ESC to return to menu",
            True,
            self.GRAY
        )

        self.screen.blit(
            instruction,
            instruction.get_rect(
                center=(self.WIDTH // 2, 570)
            )
        )

    def run(self):
        """Run the game loop."""

        self.start()

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        return "menu"

                    if (
                        event.key == pygame.K_r
                        and self.game_finished
                    ):
                        self.start()

                if not self.game_finished:

                    self.handle_event(event)

            self.update()

            if self.game_finished:

                self.draw_game_over()

            else:

                self.draw()

            pygame.display.flip()

            self.clock.tick(144)

        return "quit"
    