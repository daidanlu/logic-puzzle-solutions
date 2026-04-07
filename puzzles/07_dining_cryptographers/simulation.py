"""
Dining Cryptographers Problem Simulation.
Validates XOR-based broadcast correctness and perfect secrecy.
"""
import random

def run_protocol(payer: str):
    # 1. Payment states
    P_A = 1 if payer == 'A' else 0
    P_B = 1 if payer == 'B' else 0
    P_C = 1 if payer == 'C' else 0

    # 2. Shared secret coins
    c_AB = random.choice([0, 1])
    c_BC = random.choice([0, 1])
    c_CA = random.choice([0, 1])

    # 3. Local XOR broadcasts
    M_A = c_AB ^ c_CA ^ P_A
    M_B = c_BC ^ c_AB ^ P_B
    M_C = c_CA ^ c_BC ^ P_C

    # 4. Global XOR sum
    S = M_A ^ M_B ^ M_C
    
    return M_A, M_B, M_C, S

def verify_perfect_secrecy(trials=100000):
    """Monte Carlo simulation from Observer C's perspective."""
    dist_A = {(0,0): 0, (0,1): 0, (1,0): 0, (1,1): 0}
    dist_B = {(0,0): 0, (0,1): 0, (1,0): 0, (1,1): 0}

    for _ in range(trials):
        # Case 1: A pays
        M_A, M_B, _, _ = run_protocol('A')
        dist_A[(M_A, M_B)] += 1
        
        # Case 2: B pays
        M_A, M_B, _, _ = run_protocol('B')
        dist_B[(M_A, M_B)] += 1

    print("[Observer C's Intercepted Distribution (M_A, M_B)]")
    print(f"{'State':<10} | {'If A Paid':<12} | {'If B Paid':<12}")
    print("-" * 40)
    for state in dist_A:
        prob_A = dist_A[state] / trials
        prob_B = dist_B[state] / trials
        print(f"{str(state):<10} | {prob_A:.4f}       | {prob_B:.4f}")

if __name__ == "__main__":
    # 1. Correctness: S=0 if NSA, S=1 if internal
    print("=== Correctness Verification ===")
    for payer in ['NSA', 'A', 'B', 'C']:
        _, _, _, S = run_protocol(payer)
        print(f"Payer: {payer:<3} -> Global XOR Sum (S): {S}")

    # 2. Anonymity: Distributions must be identical
    print("\n=== Perfect Secrecy Verification (100k trials) ===")
    verify_perfect_secrecy()