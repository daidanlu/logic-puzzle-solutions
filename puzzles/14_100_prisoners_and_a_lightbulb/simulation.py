import random

class Node:
    def __init__(self, node_id, is_counter):
        self.node_id = node_id
        self.is_counter = is_counter
        
        if self.is_counter:
            # The counter maintains a local integer accumulator initialized to 1.
            self.count = 1
            self.has_transmitted = None 
        else:
            # Each follower maintains a local Boolean variable initialized to False.
            self.has_transmitted = False
            self.count = None

def run_simulation():
    print("=== 100 Prisoners & 1-bit Shared Memory Simulation ===\n")
    
    # The prisoners elect one special node called the counter or master.
    # The remaining 99 nodes are called followers or slaves.
    nodes = [Node(i, is_counter=(i == 0)) for i in range(100)]
    
    # There is a single state register in the interrogation room, represented by a light bulb.
    # The initial state is OFF.
    light_bulb = False 
    days = 0
    
    # actual_visited tracks true visits for an omniscient safety check.
    actual_visited = set()

    while True:
        days += 1
        
        # The scheduler selects one of the 100 nodes uniformly and independently at random.
        chosen = random.choice(nodes)
        actual_visited.add(chosen.node_id)

        if chosen.is_counter:
            # --- Counter FSM ---
            # If the light is ON.
            if light_bulb is True:
                # The counter turns the light OFF and increments its count.
                light_bulb = False
                chosen.count += 1
                
                # If the count reaches 100, trigger the halting assertion.
                if chosen.count == 100:
                    print(f"[{days} Days] Counter reached 100. Executing Halt_And_Assert()!")
                    # Verify that all 100 nodes have indeed visited the room.
                    assert len(actual_visited) == 100, "FATAL ERROR: Safety invariant broken!"
                    print("Assertion SUCCESS: All 100 nodes have been scheduled at least once.")
                    break
            # If the light is OFF, the counter does nothing and leaves the state unchanged.
        
        else:
            # --- Follower FSM ---
            # If the light is OFF and the follower has not yet transmitted.
            if light_bulb is False and chosen.has_transmitted is False:
                # The follower turns the light ON.
                light_bulb = True
                # The follower's local state is permanently updated.
                chosen.has_transmitted = True
            # Otherwise, the follower does nothing and leaves the state unchanged.

if __name__ == "__main__":
    run_simulation()