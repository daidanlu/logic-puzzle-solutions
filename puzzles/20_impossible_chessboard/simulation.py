import random

BOARD_SIZE = 64


def checksum(board):
    """
    Compute XOR checksum of all positions whose coins are heads.

    board[i] = 1 means heads
    board[i] = 0 means tails
    """
    result = 0
    for i, coin in enumerate(board):
        if coin == 1:
            result ^= i
    return result


def flip_coin(board, position):
    """
    Return a new board after flipping exactly one coin.
    """
    new_board = board.copy()
    new_board[position] ^= 1
    return new_board


def alice_choose_flip(board, key_position):
    """
    Alice computes the current checksum P_current
    and chooses F = P_current XOR K.
    """
    current = checksum(board)
    return current ^ key_position


def bob_decode(board):
    """
    Bob computes the checksum of the final board
    and outputs it as the key position.
    """
    return checksum(board)


def simulate_once(verbose=True):
    """
    Run one random example of the protocol.
    """
    board = [random.randint(0, 1) for _ in range(BOARD_SIZE)]
    key_position = random.randint(0, BOARD_SIZE - 1)

    current_checksum = checksum(board)
    flip_position = alice_choose_flip(board, key_position)
    final_board = flip_coin(board, flip_position)
    bob_answer = bob_decode(final_board)

    if verbose:
        print("Initial checksum:", current_checksum)
        print("Key position:    ", key_position)
        print("Alice flips:     ", flip_position)
        print("Final checksum:  ", checksum(final_board))
        print("Bob answers:     ", bob_answer)

    assert bob_answer == key_position
    return True


def test_flip_identity(trials=1000):
    """
    Verify the key observation:

    flipping position F changes the checksum from P to P XOR F.
    """
    for _ in range(trials):
        board = [random.randint(0, 1) for _ in range(BOARD_SIZE)]
        current = checksum(board)

        for flip_position in range(BOARD_SIZE):
            final_board = flip_coin(board, flip_position)
            new_checksum = checksum(final_board)

            assert new_checksum == (current ^ flip_position)

    print(f"Flip identity passed for {trials} random boards.")


def test_protocol(trials=1000):
    """
    For many random boards, test all possible key positions.
    """
    for _ in range(trials):
        board = [random.randint(0, 1) for _ in range(BOARD_SIZE)]

        for key_position in range(BOARD_SIZE):
            flip_position = alice_choose_flip(board, key_position)
            final_board = flip_coin(board, flip_position)
            bob_answer = bob_decode(final_board)

            assert bob_answer == key_position

    print(f"Protocol passed for {trials} random boards and all 64 key positions.")


def test_edge_case():
    """
    Test the edge case where P_current == K.

    Then Alice flips position 0.
    Since 0 XOR does not change the checksum, Bob still gets K.
    """
    board = [random.randint(0, 1) for _ in range(BOARD_SIZE)]
    key_position = checksum(board)

    flip_position = alice_choose_flip(board, key_position)
    final_board = flip_coin(board, flip_position)
    bob_answer = bob_decode(final_board)

    print("Edge case:")
    print("Current checksum:", key_position)
    print("Alice flips:     ", flip_position)
    print("Bob answers:     ", bob_answer)

    assert flip_position == 0
    assert bob_answer == key_position

    print("Edge case passed.")


if __name__ == "__main__":
    random.seed(0)

    print("One example:")
    simulate_once(verbose=True)

    print()
    test_flip_identity()

    print()
    test_edge_case()

    print()
    test_protocol()
