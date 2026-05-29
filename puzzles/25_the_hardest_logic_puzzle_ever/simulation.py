from itertools import permutations
from typing import Callable, Dict, Iterable, List, Optional, Tuple

GodName = str
Role = str
Word = str
Arrangement = Dict[GodName, Role]
LanguageMap = Dict[Word, bool]
Proposition = Callable[[Arrangement], bool]

GODS: Tuple[GodName, GodName, GodName] = ("A", "B", "C")
ROLES: Tuple[Role, Role, Role] = ("True", "False", "Random")
WORDS: Tuple[Word, Word] = ("Ja", "Da")


class PuzzleSimulationError(RuntimeError):
    """Raised when the simulated strategy fails an internal consistency check."""


def word_for_truth_value(value: bool, language: LanguageMap) -> Word:
    """
    Return the word that expresses a yes/no truth value under a language mapping.

    In this program, True means a yes-answer and False means a no-answer.
    The mapping is intentionally configurable because the puzzle does not reveal
    whether `Ja` or `Da` means yes.
    """
    for word, means_yes in language.items():
        if means_yes == value:
            return word
    raise PuzzleSimulationError(
        "Invalid language map: no word matches the requested value."
    )


def direct_answer_non_random(
    role: Role, proposition_is_true: bool, language: LanguageMap
) -> Word:
    """
    Simulate how True or False would answer a direct yes-or-no question.

    True gives the correct yes/no answer. False gives the opposite answer.
    Random is deliberately excluded here because the key lemma only applies to
    non-random gods.
    """
    if role == "True":
        return word_for_truth_value(proposition_is_true, language)
    if role == "False":
        return word_for_truth_value(not proposition_is_true, language)
    raise PuzzleSimulationError("The non-random answer function was called on Random.")


def embedded_answer_non_random(
    role: Role, proposition_is_true: bool, language: LanguageMap
) -> Word:
    """
    Simulate the embedded question used in the proof:

        If I asked you whether proposition p is true, would you answer `Ja`?

    For True and False, this reproduces the lemma from the README: the answer is
    `Ja` exactly when p is true, regardless of whether `Ja` means yes or no.
    """
    hypothetical_direct_answer = direct_answer_non_random(
        role, proposition_is_true, language
    )
    meta_proposition_is_true = hypothetical_direct_answer == "Ja"
    return direct_answer_non_random(role, meta_proposition_is_true, language)


def ask_embedded_question(
    arrangement: Arrangement,
    god: GodName,
    proposition: Proposition,
    language: LanguageMap,
    random_forced_answer: Optional[Word] = None,
) -> Word:
    """
    Ask the embedded question to a specific god.

    If the addressed god is True or False, the response is computed exactly.
    If the addressed god is Random, this verifier treats Random's answer as an
    externally forced `Ja` or `Da`. This is enough for the strategy because the
    proof only needs to survive either possible first answer from Random.
    """
    role = arrangement[god]
    if role == "Random":
        if random_forced_answer not in WORDS:
            raise PuzzleSimulationError(
                "Random must be forced to answer either `Ja` or `Da`."
            )
        return random_forced_answer

    proposition_is_true = proposition(arrangement)
    return embedded_answer_non_random(role, proposition_is_true, language)


def run_three_question_strategy(
    arrangement: Arrangement,
    language: LanguageMap,
    random_first_answer: Word = "Ja",
    verbose: bool = False,
) -> Arrangement:
    """
    Execute the three-question strategy from the README.

    The returned dictionary is the strategy's inferred identity assignment. A correct
    implementation should return exactly the same mapping as the hidden arrangement.
    """
    trace: List[str] = []

    # Question 1: ask B whether A is Random, using the embedded-question form.
    # Selection rule from the proof:
    # - If B answers `Ja`, choose C.
    # - If B answers `Da`, choose A.
    q1_answer = ask_embedded_question(
        arrangement=arrangement,
        god="B",
        proposition=lambda state: state["A"] == "Random",
        language=language,
        random_forced_answer=random_first_answer,
    )
    x = "C" if q1_answer == "Ja" else "A"

    if arrangement[x] == "Random":
        raise PuzzleSimulationError("Question 1 failed to select a non-random god.")

    trace.append(
        f"Q1 to B: Is A Random under the embedded form? Answer = {q1_answer}; choose X = {x}."
    )

    # Question 2: ask X whether X is True, again using the embedded-question form.
    # Since X is guaranteed not to be Random, `Ja` identifies X as True and `Da`
    # identifies X as False.
    q2_answer = ask_embedded_question(
        arrangement=arrangement,
        god=x,
        proposition=lambda state, selected=x: state[selected] == "True",
        language=language,
    )
    x_role = "True" if q2_answer == "Ja" else "False"

    trace.append(
        f"Q2 to X={x}: Is X True under the embedded form? Answer = {q2_answer}; infer {x} = {x_role}."
    )

    # Question 3: choose one of the remaining two gods as Y and the other as Z.
    # Ask X whether Y is Random. Since X is non-random, the lemma applies again.
    remaining = [god for god in GODS if god != x]
    y, z = remaining[0], remaining[1]

    q3_answer = ask_embedded_question(
        arrangement=arrangement,
        god=x,
        proposition=lambda state, candidate=y: state[candidate] == "Random",
        language=language,
    )

    inferred: Arrangement = {}
    inferred[x] = x_role

    if q3_answer == "Ja":
        inferred[y] = "Random"
        inferred[z] = "False" if x_role == "True" else "True"
    else:
        inferred[z] = "Random"
        inferred[y] = "False" if x_role == "True" else "True"

    trace.append(
        f"Q3 to X={x}: Is Y={y} Random under the embedded form? "
        f"Answer = {q3_answer}; infer final mapping = {format_arrangement(inferred)}."
    )

    if verbose:
        print("Sample strategy trace")
        print("---------------------")
        print(f"Hidden arrangement: {format_arrangement(arrangement)}")
        print(f"Language mapping: {format_language(language)}")
        for line in trace:
            print(line)
        print()

    return inferred


def all_arrangements() -> Iterable[Arrangement]:
    """Generate all six possible assignments of True, False, and Random to A, B, and C."""
    for roles in permutations(ROLES):
        yield dict(zip(GODS, roles))


def all_language_maps() -> Iterable[LanguageMap]:
    """Generate both possible meanings of the words `Ja` and `Da`."""
    yield {"Ja": True, "Da": False}
    yield {"Ja": False, "Da": True}


def format_arrangement(arrangement: Arrangement) -> str:
    """Format an identity assignment in a compact, stable order."""
    return ", ".join(f"{god}={arrangement[god]}" for god in GODS)


def format_language(language: LanguageMap) -> str:
    """Format the unknown language mapping for readable output."""
    ja_meaning = "yes" if language["Ja"] else "no"
    da_meaning = "yes" if language["Da"] else "no"
    return f"Ja={ja_meaning}, Da={da_meaning}"


def verify_embedded_lemma() -> None:
    """
    Verify the key lemma computationally for True and False.

    This step documents that the code's embedded-question model matches the written
    proof before the full three-question strategy is tested.
    """
    for language in all_language_maps():
        for role in ("True", "False"):
            for proposition_is_true in (True, False):
                answer = embedded_answer_non_random(role, proposition_is_true, language)
                expected = "Ja" if proposition_is_true else "Da"
                if answer != expected:
                    raise PuzzleSimulationError(
                        "Embedded lemma verification failed for "
                        f"role={role}, proposition={proposition_is_true}, language={format_language(language)}."
                    )


def exhaustive_strategy_verification() -> int:
    """
    Exhaustively verify the three-question strategy.

    The test covers:
    - 6 possible placements of True, False, and Random among A, B, and C;
    - 2 possible meanings of `Ja` and `Da`;
    - both possible first answers from Random only in the cases where B is Random.

    The function returns the number of effective scenario checks completed.
    """
    cases_checked = 0

    for arrangement in all_arrangements():
        for language in all_language_maps():
            random_answer_options = WORDS if arrangement["B"] == "Random" else ("Ja",)

            for random_first_answer in random_answer_options:
                inferred = run_three_question_strategy(
                    arrangement=arrangement,
                    language=language,
                    random_first_answer=random_first_answer,
                    verbose=False,
                )
                cases_checked += 1

                if inferred != arrangement:
                    raise PuzzleSimulationError(
                        "Strategy verification failed.\n"
                        f"Hidden arrangement: {format_arrangement(arrangement)}\n"
                        f"Language mapping: {format_language(language)}\n"
                        f"Forced first Random answer: {random_first_answer}\n"
                        f"Inferred arrangement: {format_arrangement(inferred)}"
                    )

    return cases_checked


def main() -> None:
    """Run the proof-oriented simulation and print a concise verification report."""
    sample_arrangement: Arrangement = {"A": "False", "B": "Random", "C": "True"}
    sample_language: LanguageMap = {"Ja": False, "Da": True}

    run_three_question_strategy(
        arrangement=sample_arrangement,
        language=sample_language,
        random_first_answer="Ja",
        verbose=True,
    )

    verify_embedded_lemma()
    cases_checked = exhaustive_strategy_verification()

    print("Exhaustive verification")
    print("-----------------------")
    print(
        "Embedded lemma check: passed for True and False under both language mappings."
    )
    print(f"Three-question strategy check: passed for {cases_checked} total scenarios.")
    print(
        "Conclusion: the executable simulation matches the proof strategy in the README."
    )


if __name__ == "__main__":
    main()
