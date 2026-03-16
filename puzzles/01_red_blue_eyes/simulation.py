"""
Multi-Agent Simulation for the Blue-Eyed Islanders Puzzle.
"""

class Person:
    def __init__(self, pid: int, is_blue: bool, total_blue_in_island: int):
        self.pid = pid
        self.is_blue = is_blue
        
        # What this person sees: B-1 if they are blue, B if they are brown
        self.observed_blue = total_blue_in_island - 1 if is_blue else total_blue_in_island
        
        # Epistemic state: The total number of blue eyes could only be what they see, or what they see + 1
        self.possible_totals = {self.observed_blue, self.observed_blue + 1}
        
        # Common knowledge introduced by the foreigner: Total blue eyes >= 1
        if 0 in self.possible_totals:
            self.possible_totals.remove(0)
            
        self.has_left = False

    def deduce_and_leave(self) -> bool:
        """Deduce if they are blue-eyed based on their current epistemic state."""
        if self.has_left:
            return False
            
        # If the hypothesis space collapses to exactly one possibility, and it's greater than the observed blue eyes, they must be blue.
        if len(self.possible_totals) == 1:
            inferred_total = list(self.possible_totals)[0]
            if inferred_total > self.observed_blue:
                self.has_left = True
                return True
        return False

    def update_knowledge(self, current_day: int):
        """Update epistemic state based on the timeout event (no one die today)."""
        # If current_day passes and no one has died, the true total must be > current_day.
        if not self.has_left and current_day in self.possible_totals:
            self.possible_totals.remove(current_day)


class Island:
    def __init__(self, total_population: int, blue_count: int):
        self.day = 1
        # Initialize the population
        self.people = [
            Person(pid=i, is_blue=(i < blue_count), total_blue_in_island=blue_count)
            for i in range(total_population)
        ]
            
    def simulate(self):
        print("=== Simulation Started ===")
        print("Foreigner's Announcement: At least one person has blue eyes.\n")
        
        while True:
            # 1. Noon: Everyone tries to deduce their color and decide whether to leave
            left_today = []
            for person in self.people:
                if person.deduce_and_leave():
                    left_today.append(person)
            
            # 2. Check the outcome of the day
            if left_today:
                print(f"Day {self.day} Noon: {len(left_today)} blue-eyed islanders figured it out and committed suicide.")
                break # Puzzle resolved
            else:
                print(f"Day {self.day} Noon: No one leaves. Everyone continues to wait.")
                
            # 3. Evening: Everyone updates their internal knowledge based on today's outcome
            for person in self.people:
                person.update_knowledge(self.day)
                
            self.day += 1


if __name__ == "__main__":
    # Test parameters: 1000 people in total, 100 of them have blue eyes.
    N = 1000 
    K = 100 
    
    print(f"Setup: Total population = {N}, Blue eyes = {K}")
    print("Condition: Islanders can see others but don't know the exact total count.\n")
    
    island = Island(total_population=N, blue_count=K)
    island.simulate()