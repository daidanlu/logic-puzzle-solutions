"""
Simulation for Fitch Cheney's Five-Card Trick.

The program implements the deterministic protocol described in the proof:

1. Alice receives 5 cards.
2. By the pigeonhole principle, at least two cards have the same suit.
3. Alice chooses a same-suit pair whose clockwise rank distance is in {1,...,6}.
   The first card of the display is the anchor; the paired card is hidden.
4. The remaining three displayed cards encode the offset 1..6 by their permutation.
5. Bob decodes the hidden card from the anchor and the permutation.

The script also verifies the protocol over all C(52, 5) possible hands.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import comb
from typing import Dict, Iterable, List, Sequence, Tuple

# Rank values are interpreted modulo 13.
# A = 1, ..., Q = 12, K = 13.
RANKS: Tuple[str, ...] = (
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
)
RANK_VALUE: Dict[str, int] = {rank: i + 1 for i, rank in enumerate(RANKS)}
VALUE_RANK: Dict[int, str] = {i + 1: rank for i, rank in enumerate(RANKS)}

# This order is used only to define a public total order on cards.
# It makes Diamonds < Clubs < Hearts < Spades, equivalently
# Spades > Hearts > Clubs > Diamonds.
SUITS: Tuple[str, ...] = ("D", "C", "H", "S")
SUIT_NAME: Dict[str, str] = {
    "S": "Spades",
    "H": "Hearts",
    "C": "Clubs",
    "D": "Diamonds",
}
SUIT_ORDER: Dict[str, int] = {suit: i for i, suit in enumerate(SUITS)}


@dataclass(frozen=True, order=False)
class Card:
    rank: str
    suit: str

    @property
    def value(self) -> int:
        return RANK_VALUE[self.rank]

    def sort_key(self) -> Tuple[int, int]:
        """Public total order used by Alice and Bob for permutation encoding."""
        return (self.value, SUIT_ORDER[self.suit])

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def long_name(self) -> str:
        return f"{SUIT_NAME[self.suit]} {self.rank}"


# Permutation dictionary for the three remaining cards.
# If the sorted cards are S < M < L, then these six arrangements encode offsets 1..6.
ENCODE_PATTERN: Dict[int, Tuple[int, int, int]] = {
    1: (0, 1, 2),  # S, M, L
    2: (0, 2, 1),  # S, L, M
    3: (1, 0, 2),  # M, S, L
    4: (1, 2, 0),  # M, L, S
    5: (2, 0, 1),  # L, S, M
    6: (2, 1, 0),  # L, M, S
}

DECODE_PATTERN: Dict[Tuple[int, int, int], int] = {
    pattern: offset for offset, pattern in ENCODE_PATTERN.items()
}


def build_deck() -> List[Card]:
    """Return a standard 52-card deck."""
    return [Card(rank, suit) for suit in SUITS for rank in RANKS]


def clockwise_distance(start: Card, end: Card) -> int:
    """
    Return the clockwise distance from start to end on the rank cycle modulo 13.

    The cards must have the same suit and distinct ranks.
    The result is in {1, ..., 12}.
    """
    if start.suit != end.suit:
        raise ValueError("Clockwise distance is only defined for same-suit cards.")
    distance = (end.value - start.value) % 13
    if distance == 0:
        raise ValueError("Cards of the same suit cannot have the same rank in a deck.")
    return distance


def choose_anchor_and_hidden(hand: Sequence[Card]) -> Tuple[Card, Card]:
    """
    Deterministically choose an anchor card and a hidden card.

    For every same-suit pair, exactly one of the two directions has distance <= 6.
    We collect all valid ordered choices (anchor, hidden), then choose the one with
    the lexicographically smallest public sorting key. This extra tie-breaking rule
    is not needed for Bob's decoding, but it makes Alice's algorithm deterministic.
    """
    candidates: List[Tuple[Tuple[Tuple[int, int], Tuple[int, int]], Card, Card]] = []

    for a, b in combinations(hand, 2):
        if a.suit != b.suit:
            continue

        dist_ab = clockwise_distance(a, b)
        if 1 <= dist_ab <= 6:
            candidates.append(((a.sort_key(), b.sort_key()), a, b))
        else:
            candidates.append(((b.sort_key(), a.sort_key()), b, a))

    if not candidates:
        raise ValueError(
            "No same-suit pair found. This should be impossible for 5 cards and 4 suits."
        )

    _, anchor, hidden = min(candidates, key=lambda item: item[0])
    return anchor, hidden


def encode_three_cards(remaining: Sequence[Card], offset: int) -> List[Card]:
    """
    Encode offset 1..6 using a permutation of the three remaining cards.
    """
    if len(remaining) != 3:
        raise ValueError("Exactly three remaining cards are required.")
    if offset not in ENCODE_PATTERN:
        raise ValueError("Offset must be in {1, 2, 3, 4, 5, 6}.")

    ordered = sorted(remaining, key=lambda card: card.sort_key())
    pattern = ENCODE_PATTERN[offset]
    return [ordered[i] for i in pattern]


def decode_three_cards(cards: Sequence[Card]) -> int:
    """
    Decode the offset 1..6 from the order of the last three displayed cards.
    """
    if len(cards) != 3:
        raise ValueError("Exactly three cards are required for decoding.")

    ordered = sorted(cards, key=lambda card: card.sort_key())
    index_of_card = {card: i for i, card in enumerate(ordered)}
    pattern = tuple(index_of_card[card] for card in cards)

    if pattern not in DECODE_PATTERN:
        raise ValueError("Invalid permutation pattern.")
    return DECODE_PATTERN[pattern]


def alice_encode(hand: Sequence[Card]) -> Tuple[List[Card], Card]:
    """
    Alice receives five cards and returns:
    - the four displayed cards in order,
    - the hidden card.

    The first displayed card is the anchor.
    The last three displayed cards encode the offset from anchor to hidden.
    """
    if len(hand) != 5:
        raise ValueError("Alice must receive exactly five cards.")
    if len(set(hand)) != 5:
        raise ValueError("The five cards must be distinct.")

    anchor, hidden = choose_anchor_and_hidden(hand)
    offset = clockwise_distance(anchor, hidden)

    if not (1 <= offset <= 6):
        raise AssertionError("The chosen offset must be in {1, ..., 6}.")

    remaining = [card for card in hand if card not in (anchor, hidden)]
    encoded_tail = encode_three_cards(remaining, offset)
    displayed = [anchor] + encoded_tail

    return displayed, hidden


def bob_decode(displayed: Sequence[Card]) -> Card:
    """
    Bob receives the four displayed cards and reconstructs the hidden card.
    """
    if len(displayed) != 4:
        raise ValueError("Bob must see exactly four cards.")
    if len(set(displayed)) != 4:
        raise ValueError("The displayed cards must be distinct.")

    anchor = displayed[0]
    tail = displayed[1:]
    offset = decode_three_cards(tail)

    hidden_value = ((anchor.value - 1 + offset) % 13) + 1
    hidden_rank = VALUE_RANK[hidden_value]

    return Card(hidden_rank, anchor.suit)


def verify_hand(hand: Sequence[Card]) -> bool:
    """Return True iff Bob correctly decodes Alice's hidden card."""
    displayed, hidden = alice_encode(hand)
    decoded = bob_decode(displayed)
    return decoded == hidden


def verify_all_hands() -> None:
    """
    Exhaustively verify the protocol over all C(52, 5) possible five-card hands.
    """
    deck = build_deck()
    total = comb(len(deck), 5)
    checked = 0

    for hand in combinations(deck, 5):
        checked += 1
        displayed, hidden = alice_encode(hand)
        decoded = bob_decode(displayed)

        if decoded != hidden:
            raise AssertionError(
                "Protocol failed.\n"
                f"Hand:      {format_cards(hand)}\n"
                f"Displayed: {format_cards(displayed)}\n"
                f"Hidden:    {hidden}\n"
                f"Decoded:   {decoded}"
            )

    print(f"Exhaustive verification passed: {checked:,} / {total:,} hands.")


def format_cards(cards: Iterable[Card]) -> str:
    return " ".join(str(card) for card in cards)


def demo() -> None:
    """
    Demonstrate the example from the proof:

    Spades 4, Spades 9, Hearts J, Clubs 2, Diamonds 7.
    Alice should be able to hide Spades 9 and display:
    Spades 4, Hearts J, Clubs 2, Diamonds 7.
    """
    hand = [
        Card("4", "S"),
        Card("9", "S"),
        Card("J", "H"),
        Card("2", "C"),
        Card("7", "D"),
    ]

    displayed, hidden = alice_encode(hand)
    decoded = bob_decode(displayed)
    offset = decode_three_cards(displayed[1:])

    print("=" * 72)
    print("Demo: Fitch Cheney's Five-Card Trick")
    print("=" * 72)
    print(f"Original hand:      {format_cards(hand)}")
    print(f"Displayed by Alice: {format_cards(displayed)}")
    print(f"Hidden by Alice:    {hidden}")
    print()
    print(f"Anchor card:        {displayed[0]}")
    print(f"Encoded offset:     +{offset}")
    print(f"Decoded by Bob:     {decoded}")
    print(f"Correct:            {decoded == hidden}")
    print("=" * 72)


def sample_random_tests(num_tests: int = 10_000, seed: int = 0) -> None:
    import random

    rng = random.Random(seed)
    deck = build_deck()

    for _ in range(num_tests):
        hand = rng.sample(deck, 5)
        if not verify_hand(hand):
            raise AssertionError(f"Random test failed on hand: {format_cards(hand)}")

    print(f"Random verification passed: {num_tests:,} sampled hands.")


if __name__ == "__main__":
    demo()
    sample_random_tests()
    verify_all_hands()
