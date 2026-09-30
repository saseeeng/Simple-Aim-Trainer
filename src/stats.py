import json
import os


class Stats:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all statistics."""

        self.hits = 0
        self.misses = 0
        self.reaction_times = []
        self.score = 0

    def register_hit(self, reaction_time):
        """Register a successful target hit."""

        self.hits += 1

        self.reaction_times.append(reaction_time)

        # Score is based on reaction time.
        if reaction_time <= 0.2:
            points = 100
        elif reaction_time <= 0.4:
            points = 80
        elif reaction_time <= 0.6:
            points = 60
        elif reaction_time <= 1.0:
            points = 40
        else:
            points = 20

        self.score += points

    def register_miss(self):
        """Register a missed shot."""

        self.misses += 1

        # Small penalty for missing.
        self.score = max(0, self.score - 5)

    def get_total_shots(self):
        """Return total number of clicks."""

        return self.hits + self.misses

    def get_accuracy(self):
        """Return accuracy as a percentage."""

        total = self.get_total_shots()

        if total == 0:
            return 0

        return (self.hits / total) * 100

    def get_average_reaction_time(self):
        """Return average reaction time in seconds."""

        if not self.reaction_times:
            return 0

        return sum(self.reaction_times) / len(self.reaction_times)

    def get_targets_per_second(self, game_time):
        """Return hits per second."""

        if game_time <= 0:
            return 0

        return self.hits / game_time

    def save_score(self, difficulty, game_time):
        """Save the current result to data/scores.json."""

        data_directory = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data"
        )

        os.makedirs(data_directory, exist_ok=True)

        file_path = os.path.join(
            data_directory,
            "scores.json"
        )

        # Load existing scores
        scores = []

        if os.path.exists(file_path):

            try:
                with open(file_path, "r") as file:
                    scores = json.load(file)

            except (json.JSONDecodeError, OSError):
                scores = []

        # Create new result
        result = {
            "score": self.score,
            "hits": self.hits,
            "misses": self.misses,
            "accuracy": round(self.get_accuracy(), 2),
            "average_reaction_ms": round(
                self.get_average_reaction_time() * 1000,
                2
            ),
            "difficulty": difficulty,
            "game_time": game_time
        }

        scores.append(result)

        # Sort by score
        scores.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        # Keep only top 10
        scores = scores[:10]

        with open(file_path, "w") as file:
            json.dump(
                scores,
                file,
                indent=4
            )

    @staticmethod
    def load_scores():
        """Load saved scores."""

        data_directory = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data"
        )

        file_path = os.path.join(
            data_directory,
            "scores.json"
        )

        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, "r") as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            return []