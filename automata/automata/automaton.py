"""Automaton implementation."""
from typing import Collection

from interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)



class State(AbstractState):
    """State of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class Transition(AbstractTransition[State]):
    """Transition of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class FiniteAutomaton(
    AbstractFiniteAutomaton[State, Transition],
):
    """Automaton."""

    def __init__(
        self,
        *,
        initial_state: State,
        states: Collection[State],
        symbols: Collection[str],
        transitions: Collection[Transition],
    ) -> None:
        super().__init__(
            initial_state=initial_state,
            states=states,
            symbols=symbols,
            transitions=transitions,
        )

        # Add here additional initialization code.
        # Do not change the constructor interface.
                        
                        
    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":        

        from automaton_evaluator import FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(self)        
        f_initial_state_set = evaluator.current_states   
        f_symbols = self.symbols
        f_symbols.remove(None)
   
        f_states = []
        f_initial_state = State(str(f_initial_state_set))
        f_states.append(f_initial_state)
        f_transitions = []        
        
        for symbol in self.symbols:
            evaluator.process_symbol(symbol)
            result = evaluator.current_states
            evaluator.current_states = f_initial_state_set
            final_state = State(str(result))
            f_states.append(final_state)
            f_transitions.append(Transition(f_initial_state, symbol, final_state))
           


    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
