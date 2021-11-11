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
        

    def accesibleStates(
            self,
            start_state: State,
            symbols: Collection[str],
            ) -> Collection[State]:
        accesible_states = {}
        new_states = {}
        for t in self.transitions:
            if t.symbol in symbols and start_state==t.initial_state:
                new_states.add(t.final_state)
        accesible_states.add(new_states)
        while(new_states):
            previous_new_states = new_states
            new_states = {}                                  
            for t in self.transitions:
                    if t.symbol in symbols and t.initial_state in previous_new_states:
                        new_states.add(t.final_state)
            new_states = new_states - accesible_states
            accesible_states.add(new_states)
            
                
        return accesible_states
                

    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":
        
        lista_estados = []
        lista_transiciones = []

        for t in self.transitions:
            if t.symbol == None:
                if t.final_state.is_final:
                    q0 = State(name=t.initial_state.name + t.final_state.name), is_final=True)
                    ##############################Este algoritmo repite estados##################################
                    lista_estados.append(q0)
                elif:
                    q0 = State(name=t.initial_state.name + t.final_state.name), is_final=False)
                    ##############################Este algoritmo repite estados##################################
                    lista_estados.append(q0)
                for aux1 in self.transitions:
                    if aux1.final_state == t.initial_state:
                        lista_transiciones.append(Transition(aux1.final_state, aux1.symbol, q0))
                for aux2 in self.transitions:
                    if aux2.initial_state == t.final_state:
                        lista_transiciones.append(Transition(q0, aux2.symbol, aux2.initial_state))

                

        
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
