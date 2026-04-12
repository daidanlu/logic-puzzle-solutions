"""
General Byzantine Generals Problem Simulator - OM(m) Recursive Algorithm
Validates that N >= 3m + 1 nodes can reach consensus with m traitors.
Simulates N=7, m=2 using the recursive OM(2) algorithm.
"""
from collections import Counter
import random

def deterministic_majority(votes):
    """
    Returns the absolute majority of votes. Ties default to 'Retreat'.
    """
    if not votes:
        return 'Retreat'
    counts = Counter(votes)
    most_common = counts.most_common()
    
    # Check for absolute majority
    if len(most_common) == 1 or most_common[0][1] > most_common[1][1]:
        return most_common[0][0]
    return 'Retreat'

def OM_algorithm(m, commander_id, commander_value, lieutenants, traitors, depth=0):
    """
    The recursive OM(m) algorithm by Leslie Lamport.
    Returns a dictionary of {lieutenant_id: decided_value}.
    """
    indent = "  " * depth
    decisions = {}

    # Base Case: OM(0)
    # The commander sends its value, and lieutenants just use it.
    if m == 0:
        for L in lieutenants:
            if commander_id in traitors:
                # Traitor sends random/conflicting noise in the final step
                val = random.choice(['Attack', 'Retreat'])
            else:
                val = commander_value
            decisions[L] = val
        return decisions

    # Recursive Case: OM(m) where m > 0
    # Step 1: Commander sends v to all lieutenants
    received_from_commander = {}
    for L in lieutenants:
        if commander_id in traitors:
            # Traitor commander sends conflicting orders to split the network
            received_from_commander[L] = random.choice(['Attack', 'Retreat'])
        else:
            received_from_commander[L] = commander_value

    # Step 2: Each lieutenant acts as a commander in OM(m-1)
    # received_vectors[L_receiver][L_sender] = value
    received_vectors = {L: {} for L in lieutenants}
    
    for L_sender in lieutenants:
        other_lieutenants = [x for x in lieutenants if x != L_sender]
        
        # Recursive call: L_sender initiates OM(m-1) to other lieutenants
        # If L_sender is a traitor, it will automatically act maliciously in the recursive call
        om_results = OM_algorithm(
            m - 1, 
            commander_id=L_sender, 
            commander_value=received_from_commander[L_sender], 
            lieutenants=other_lieutenants, 
            traitors=traitors,
            depth=depth + 1
        )
        
        # Record the results returned from the OM(m-1) sub-universe
        for L_receiver, val in om_results.items():
            received_vectors[L_receiver][L_sender] = val

    # Step 3: Majority Vote
    for L in lieutenants:
        # Information set = [value from Commander] + [values from other Lieutenants]
        votes = [received_from_commander[L]] + list(received_vectors[L].values())
        decision = deterministic_majority(votes)
        decisions[L] = decision

    return decisions

def run_simulation(N, m, traitors, commander_id, commander_value):
    print("\n" + "="*70)
    print(f"Executing OM({m}) Algorithm for N={N}, m={m}")
    print(f"Commander: {commander_id} | Traitors: {traitors}")
    print("="*70)
    
    # Initialize lieutenants
    lieutenants = [f"L{i}" for i in range(1, N) if f"L{i}" != commander_id]
    
    # Run OM(m)
    print(f"-> Initiating recursive message storm (OM({m}) -> OM({m-1}) -> ... -> OM(0))...")
    final_decisions = OM_algorithm(m, commander_id, commander_value, lieutenants, traitors)
    
    print("\n[Final Local Decisions]")
    loyal_decisions = []
    for L, decision in final_decisions.items():
        role = "Traitor" if L in traitors else "Loyal  "
        print(f"   - {role} {L} decided to: {decision}")
        if L not in traitors:
            loyal_decisions.append(decision)
            
    # Verify Interactive Consistency (IC1)
    print("\n=> Conclusion:")
    if len(set(loyal_decisions)) == 1:
        print(f"   [SUCCESS] All loyal lieutenants reached consensus: '{loyal_decisions[0]}'")
        print("             Interactive Consistency is completely satisfied!")
    else:
        print("   [FAILURE] System fractured! Loyal nodes made conflicting decisions.")

if __name__ == "__main__":
    # N=7, m=2 requires OM(2). (1 Commander, 6 Lieutenants)
    
    # Scenario 1: Commander is Loyal, two Lieutenants are Traitors
    run_simulation(
        N=7, m=2, 
        traitors=['L3', 'L6'], 
        commander_id='Commander', 
        commander_value='Attack'
    )
    
    # Scenario 2: Commander is a Traitor, one Lieutenant is a Traitor
    # Even with the Commander actively injecting chaos, the network should reach consensus
    run_simulation(
        N=7, m=2, 
        traitors=['Commander', 'L4'], 
        commander_id='Commander', 
        commander_value='Attack' # This value is ignored because Commander is a traitor
    )