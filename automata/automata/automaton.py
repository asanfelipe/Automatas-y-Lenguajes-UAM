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
        
    # def copy(self) -> FiniteAutomaton:
    #     return FiniteAutomaton(self.initial_state, self.states.copy(), self.symbols, transitions)
        

    def to_deterministic(
        self,
    ) -> AbstractFiniteAutomaton:
        
        
        # Que queremos de devuelve el metodo:
            # Nada. Modificamos las propiedas internas del objeto (self)
            # FineteAutomaton. Creado a partir del self pero que sea determinista (sin modificar el self)
        raise NotImplementedError("This method must be implemented.")
        
# aut1 = FiniteAutomaton(....)
# Opcion 1: aut1.to_deterministic() -> a partir de ahora aurt1 es determinista
# Opcion 2: aut2 = aut1.to_deterministic() -> tengo 2 automatas uno determinista y otro no
    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
