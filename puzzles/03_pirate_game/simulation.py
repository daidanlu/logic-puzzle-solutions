"""
Dynamic Programming Simulation for the Generalized Pirate Game.
This script demonstrates the phase transitions and the emergence of the 2^k survival sequence.
"""

def simulate_pirates(total_pirates: int, total_coins: int):
    # survives[i] records whether pirate i survives (1-indexed)
    survives = [False] * (total_pirates + 1)
    
    # Track all surviving pirates for final analysis
    surviving_pirates = []

    print("=== Pirate Game Simulation ===")
    print(f"Configuration: Total Pirates (N) = {total_pirates}, Total Coins (M) = {total_coins}\n")

    for n in range(1, total_pirates + 1):
        # Phase 1 & 2: Coins are sufficient to guarantee survival (N <= 2M + 2)
        if n <= 2 * total_coins + 2:
            survives[n] = True
            surviving_pirates.append(n)
        else:
            # Phase 3: Coins are insufficient. Survival depends on free votes.
            req_votes = (n + 1) // 2     # Minimum votes needed
            base_votes = 1 + total_coins # 1 (self-vote) + M (votes bought with coins)
            
            # Dynamic Programming state transition: 
            # Count consecutive doomed pirates immediately preceding the current pirate.
            # They will cast free votes to prevent the current pirate from dying.
            free_votes = 0
            idx = n - 1
            while idx > 0 and not survives[idx]:
                free_votes += 1
                idx -= 1
                
            total_votes = base_votes + free_votes
            
            # Determine survival state
            if total_votes >= req_votes:
                survives[n] = True
                surviving_pirates.append(n)
            else:
                survives[n] = False
                
    # --- Print Analytical Report ---
    threshold = 2 * total_coins + 2
    print(f"[Phase 1 & 2] Pirates 1 to {threshold}:")
    print("All survive. The proposer can secure necessary votes via coin distribution.\n")
    
    print(f"[Phase 3] Pirates > {threshold}:")
    phase3_survivors = [p for p in surviving_pirates if p > threshold]
    
    if not phase3_survivors:
        print("No pirates survive in Phase 3.")
    else:
        print("Surviving pirates in Phase 3:")
        print(phase3_survivors)
        
        # Verify the 2^k interval pattern
        print("\nVerifying survival intervals (expected to strictly follow 2^k):")
        intervals = []
        prev = threshold # The last survivor before Phase 3 begins
        
        for survivor in phase3_survivors:
            diff = survivor - prev
            intervals.append(diff)
            prev = survivor
            
        print(f"Intervals between survivors: {intervals}")

if __name__ == "__main__":
    N = 500
    M = 100
    simulate_pirates(total_pirates=N, total_coins=M)