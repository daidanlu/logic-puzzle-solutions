import logging
from typing import Set, List, Dict

# Configure standard logging for production-grade output
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class RussianCardsProtocol:

    def __init__(self) -> None:
        # Physical constraints and distribution
        self.card_universe: Set[int] = set(range(7))
        self.alice_hand: Set[int] = {0, 1, 2}
        self.bob_hand: Set[int] = {3, 4, 6}
        self.eve_hand: Set[int] = {5}

        # Fano plane block design ensuring exactly 1-element intersections between any two blocks
        self.broadcast_sets: List[Set[int]] = [
            {0, 1, 2},  # h0: The true hand
            {0, 3, 4},  # h1: Obfuscation vector
            {0, 5, 6},  # h2: Obfuscation vector
            {1, 3, 5},  # h3: Obfuscation vector
            {1, 4, 6},  # h4: Obfuscation vector
            {2, 3, 6},  # h5: Obfuscation vector
            {2, 4, 5},  # h6: Obfuscation vector
        ]

    def execute_protocol(self) -> None:
        """Executes the broadcast and subsequent deductive phases for all agents."""
        logger.info("=== Russian Cards Protocol Execution ===")
        logger.info(f"Transmitter (Alice) Hand : {self.alice_hand}")
        logger.info(f"Receiver (Bob) Hand      : {self.bob_hand}")
        logger.info(f"Eavesdropper (Eve) Hand  : {self.eve_hand}\n")

        logger.info(
            "Alice broadcasts the Fano plane candidate sets over the public channel:"
        )
        for i, candidate in enumerate(self.broadcast_sets):
            logger.info(f"  h{i} = {candidate}")

        self._bob_deduction_phase()
        self._eve_deduction_phase()

    def _bob_deduction_phase(self) -> None:
        """Models the deterministic decryption by the intended receiver."""
        logger.info("\n--- Receiver (Bob) Deduction Phase ---")

        # Asymmetric filtration: Bob excludes any set intersecting with his own cards
        valid_candidates: List[Set[int]] = [
            candidate
            for candidate in self.broadcast_sets
            if not candidate.intersection(self.bob_hand)
        ]

        logger.info(
            f"Bob filters candidates using his private key (hand: {self.bob_hand})."
        )
        logger.info(f"Remaining candidates for Bob: {valid_candidates}")

        # Hard assertions to prove theoretical convergence
        assert (
            len(valid_candidates) == 1
        ), "Integrity Failure: Bob's state space did not collapse to a singular solution."
        assert (
            valid_candidates[0] == self.alice_hand
        ), "Integrity Failure: Bob derived the incorrect hand."
        logger.info(
            "STATUS: SUCCESS. Bob deterministically isolated Alice's exact hand."
        )

    def _eve_deduction_phase(self) -> None:
        """Models the partial deduction and epistemic obfuscation for the eavesdropper."""
        logger.info("\n--- Eavesdropper (Eve) Deduction Phase ---")

        valid_candidates: List[Set[int]] = [
            candidate
            for candidate in self.broadcast_sets
            if not candidate.intersection(self.eve_hand)
        ]

        logger.info(
            f"Eve filters candidates using her compromised key (hand: {self.eve_hand})."
        )
        logger.info(f"Remaining candidates for Eve: {valid_candidates}")

        assert (
            len(valid_candidates) == 4
        ), "Security Failure: Eve's state space collapsed beyond the theoretical threshold."

        self._analyze_epistemic_blind_spot(valid_candidates)

    def _analyze_epistemic_blind_spot(self, eve_candidates: List[Set[int]]) -> None:
        """Statistically validates the zero-knowledge leakage constraint."""
        logger.info("\n--- Epistemic Blind Spot Analysis ---")

        unknown_cards: Set[int] = self.card_universe - self.eve_hand
        frequency_map: Dict[int, int] = {card: 0 for card in unknown_cards}

        for candidate in eve_candidates:
            for card in candidate:
                frequency_map[card] += 1

        candidate_count = len(eve_candidates)
        for card, count in frequency_map.items():
            probability = (count / candidate_count) * 100
            logger.info(
                f"Card {card} appearance frequency: {count}/{candidate_count} ({probability:.1f}% probability)"
            )

            # Mathematical proof of unconditional security:
            # Every unknown card must appear exactly twice across the 4 remaining candidate sets.
            assert (
                count == 2
            ), f"Security Failure: Information leakage detected on card {card}."

        logger.info("STATUS: SUCCESS. Eve remains in perfect epistemic superposition.")


if __name__ == "__main__":
    protocol = RussianCardsProtocol()
    protocol.execute_protocol()
