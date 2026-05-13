from typing import Dict, List, Tuple


# Encoding:
# +1 means the coin is placed on the left pan.
# -1 means the coin is placed on the right pan.
#  0 means the coin is not used in that weighing.
#
# Rows are weighings.
# Columns are coins 1 to 12.
WEIGHING_MATRIX: List[List[int]] = [
    [-1, -1, -1, +1, +1, +1, -1, +1,  0,  0,  0,  0],
    [-1, -1,  0,  0,  0, -1, +1, -1, +1, +1, +1,  0],
    [ 0, +1, -1,  0, -1, +1,  0, -1, +1,  0, -1, +1],
]


Vector = Tuple[int, int, int]
Diagnosis = Tuple[int, str]


def get_coin_vectors(matrix: List[List[int]]) -> Dict[int, Vector]:
    """
    Return the ternary column vector for each coin.

    The vector for coin i describes the result pattern that would occur
    if coin i were counterfeit and heavy.
    """
    vectors = {}

    for coin_index in range(12):
        column = tuple(matrix[row][coin_index] for row in range(3))
        vectors[coin_index + 1] = column

    return vectors


def negate(vector: Vector) -> Vector:
    return tuple(-x for x in vector)


def check_balanced_weighings(matrix: List[List[int]]) -> None:
    """
    Each weighing must place the same number of coins on the left and right pans.
    """
    for row_index, row in enumerate(matrix, start=1):
        left_count = row.count(+1)
        right_count = row.count(-1)

        assert left_count == right_count, (
            f"Weighing {row_index} is invalid: "
            f"{left_count} coins on the left, {right_count} on the right."
        )


def build_decoder(coin_vectors: Dict[int, Vector]) -> Dict[Vector, Diagnosis]:
    """
    Build the decoding table.

    If the result equals v_i, coin i is heavy.
    If the result equals -v_i, coin i is light.
    """
    decoder: Dict[Vector, Diagnosis] = {}

    for coin, vector in coin_vectors.items():
        heavy_result = vector
        light_result = negate(vector)

        assert heavy_result != (0, 0, 0), f"Coin {coin} has zero vector."

        assert heavy_result not in decoder, (
            f"Ambiguous heavy vector for coin {coin}: {heavy_result}"
        )
        decoder[heavy_result] = (coin, "heavy")

        assert light_result not in decoder, (
            f"Ambiguous light vector for coin {coin}: {light_result}"
        )
        decoder[light_result] = (coin, "light")

    return decoder


def simulate_weighing_result(
    coin_vectors: Dict[int, Vector],
    counterfeit_coin: int,
    kind: str,
) -> Vector:
    """
    Simulate the three weighing outcomes.

    If the counterfeit coin is heavy, the outcome is its column vector.
    If the counterfeit coin is light, the outcome is the negative of its column vector.
    """
    vector = coin_vectors[counterfeit_coin]

    if kind == "heavy":
        return vector

    if kind == "light":
        return negate(vector)

    raise ValueError("kind must be either 'heavy' or 'light'.")


def verify_all_cases() -> None:
    check_balanced_weighings(WEIGHING_MATRIX)

    coin_vectors = get_coin_vectors(WEIGHING_MATRIX)
    decoder = build_decoder(coin_vectors)

    total_cases = 0

    for coin in range(1, 13):
        for kind in ["heavy", "light"]:
            result = simulate_weighing_result(coin_vectors, coin, kind)
            decoded_coin, decoded_kind = decoder[result]

            assert decoded_coin == coin and decoded_kind == kind, (
                f"Failed case: coin {coin} is {kind}. "
                f"Observed result {result}, decoded as coin {decoded_coin} {decoded_kind}."
            )

            total_cases += 1

    print(f"All {total_cases} cases verified successfully.")
    print("The three-weighing strategy uniquely identifies the counterfeit coin.")
    print("The strategy also determines whether the counterfeit coin is heavy or light.")


if __name__ == "__main__":
    verify_all_cases()