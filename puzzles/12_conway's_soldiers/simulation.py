import math
import random


class ConwayPhysicsEngine:
    def __init__(self):
        self.phi = (math.sqrt(5) - 1) / 2
        self.board = set()

    def get_distance(self, x: int, y: int) -> int:
        return abs(x) + abs(5 - y)

    def calculate_total_energy(self) -> float:
        total_v = 0.0
        for x, y in self.board:
            total_v += self.phi ** self.get_distance(x, y)
        return total_v

    def add_soldier(self, x: int, y: int):
        if y > 0:
            raise ValueError("Deployment must be in the southern hemisphere (y <= 0).")
        self.board.add((x, y))

    def apply_jump(self, start: tuple, over: tuple, land: tuple):
        if start in self.board and over in self.board and land not in self.board:
            energy_before = self.calculate_total_energy()

            self.board.remove(start)
            self.board.remove(over)
            self.board.add(land)

            energy_after = self.calculate_total_energy()
            delta = energy_after - energy_before

            print(f"Jump: {start} over {over} -> {land}")
            print(
                f"Energy: {energy_before:.6f} -> {energy_after:.6f} (Delta: {delta:.6f})"
            )

            assert delta <= 1e-9, "Physics broken: Energy increased!"
            return True
        return False

    def get_all_valid_jumps(self):
        """Scan the current board and return all valid jump moves."""
        jumps = []
        directions = [
            ((0, 1), (0, 2)),  # up
            ((0, -1), (0, -2)),  # down
            ((1, 0), (2, 0)),  # right
            ((-1, 0), (-2, 0)),  # left
        ]
        for x, y in self.board:
            for (dx1, dy1), (dx2, dy2) in directions:
                over = (x + dx1, y + dy1)
                land = (x + dx2, y + dy2)
                if over in self.board and land not in self.board:
                    jumps.append(((x, y), over, land))
        return jumps


if __name__ == "__main__":
    engine = ConwayPhysicsEngine()

    print("=== Phase 1: Heavy Deployment ===")
    # We're dropping a massive 41 x 21 solid square array directly into the Southern Hemisphere. x-range: -10 to 10; y-range: 0 to -40
    for x in range(-10, 11):
        for y in range(0, -41, -1):
            engine.add_soldier(x, y)

    initial_energy = engine.calculate_total_energy()
    print(f"Deployed {len(engine.board)} soldiers.")
    print(f"Initial Total Energy V: {initial_energy:.8f}")
    print("-" * 40)

    print("\n=== Phase 2: Random Walk Simulation ===")
    # test 10 steps
    for step in range(1, 11):
        valid_jumps = engine.get_all_valid_jumps()
        if not valid_jumps:
            print("Deadlock! No more valid jumps.")
            break

        # Randomly select a valid action to execute.
        chosen_jump = random.choice(valid_jumps)
        print(f"[Step {step}]")
        engine.apply_jump(*chosen_jump)
        print("-" * 40)
