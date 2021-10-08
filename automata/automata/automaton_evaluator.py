"""Evaluation of automata."""
from typing import Set

from automata.automaton import FiniteAutomaton, State
from automata.interfaces import AbstractFiniteAutomatonEvaluator


class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    def process_symbol(self, symbol: str) -> None:
        if symbol not in self.automaton.symbols:
            raise ValueError(
                f"Symbol not included in the alphabet"
            )
        
        states = set()

        for t in self.automaton.transitions:
            if t.initial_state in self.current_states:
                states.add(t.final_state)

        self._complete_lambdas(states)

        self.current_states = states
       

    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        for t in self.automaton.transitions:
            if t.initial_state in set_to_complete:
                if t.symbol is None:
                    set_to_complete.add(t.final_state)


    def is_accepting(self) -> bool:
        for state in self.current_states:
            if state.is_final:
                return True
        return False
