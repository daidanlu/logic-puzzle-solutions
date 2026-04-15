"""
Dining Philosophers Problem Simulator
Validates Symmetric Deadlock vs Dijkstra's Resource Hierarchy
"""

import threading
import time
import sys

sys.stdout.reconfigure(encoding="utf-8")


class Fork:
    def __init__(self, index):
        self.index = index
        self.lock = threading.Lock()

    def __repr__(self):
        return f"F{self.index}"


class Philosopher(threading.Thread):
    def __init__(self, index, left_fork, right_fork, strategy):
        super().__init__()
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.strategy = strategy
        self.name = f"P{self.index}"

    def run(self):
        print(f"[{self.name}] Thinking...")
        time.sleep(0.1)

        # Strategy Allocation
        if self.strategy == "symmetric":
            first_fork = self.left_fork
            second_fork = self.right_fork

        elif self.strategy == "dijkstra":
            if self.left_fork.index < self.right_fork.index:
                first_fork = self.left_fork
                second_fork = self.right_fork
            else:
                # P4 must acquire F0 (right) first, then F4 (left).
                first_fork = self.right_fork
                second_fork = self.left_fork

        print(
            f"[{self.name}] Hungry, attempting to acquire the first fork {first_fork}..."
        )
        first_fork.lock.acquire()
        print(f"[{self.name}] Successfully acquired the first fork {first_fork}.")

        time.sleep(0.5)

        print(f"[{self.name}] Attempting to acquire the second fork {second_fork}...")
        second_fork.lock.acquire()
        print(
            f"[{self.name}] Successfully acquired the second fork {second_fork}! Eating..."
        )

        time.sleep(0.5)

        # Release resources
        second_fork.lock.release()
        first_fork.lock.release()
        print(
            f"[{self.name}] Finished eating, released {first_fork} and {second_fork}."
        )


def run_simulation(strategy):
    print("\n" + "=" * 70)
    print(
        f"=== Starting Dining Philosophers Simulation | Strategy: {strategy.upper()} ==="
    )
    print("=" * 70)

    # Initialize 5 single-instance forks (Resource Set F)
    forks = [Fork(i) for i in range(5)]

    # Initialize 5 philosopher threads (Process Set P)
    philosophers = []
    for i in range(5):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % 5]  # Cyclic adjacency topological constraint
        p = Philosopher(i, left_fork, right_fork, strategy)
        philosophers.append(p)

    # Start all philosophers concurrently
    for p in philosophers:
        p.daemon = True
        p.start()

    # Wait for all threads to finish
    # If deadlock occurs, the main thread will permanently block at join()
    for p in philosophers:
        p.join(timeout=3)
        if p.is_alive():
            print("\nTERMINAL VERDICT: System frozen!")
            print(
                "FATAL DEADLOCK occurred! A directed cycle has formed in the Resource Allocation Graph!"
            )
            return

    print(
        "\nSIMULATION COMPLETE: No philosophers starved. System successfully cleared all states!"
    )


if __name__ == "__main__":
    run_simulation("symmetric")
    time.sleep(2)
    run_simulation("dijkstra")
