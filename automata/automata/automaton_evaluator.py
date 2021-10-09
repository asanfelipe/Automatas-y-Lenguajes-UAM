"""Evaluation of automata."""
from typing import Set

from automata.automaton import FiniteAutomaton, State
from automata.interfaces import AbstractFiniteAutomatonEvaluator


class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    #Función que recibe un símbolo y procesa 
    #si se avanza en los estados con él o no.
    def process_symbol(self, symbol: str) -> None:
        if symbol not in self.automaton.symbols:                #Si el símbolo (letra, número...) no se encuentra en los símbolos del autómata
            raise ValueError(                                   #generamos un error que indique que el símbolo no se encuentra en el alfabeto.
                f"Symbol not included in the alphabet"
            )
        
        states = set()                                          #Creamos una nueva variable llamada states que se encuentra vacía al principio.

        for transition in self.automaton.transitions:           #Para cada transicion de las transiciones del autómata
            if transition.initial_state in self.current_states: #si el estado inicial de la transición se encuentra en los estados actuales
                states.add(transition.final_state)              #añade a la variable states el estado final al que se llega mediante esa transición.

        self._complete_lambdas(states)                          #Llamamos a la función _complete_lambdas pasandole por referencia el conjunto de estados
                                                                #que hemos creado anteriormente.
        self.current_states = states                            #Añadimos a los estados actuales todos los estados que hemos recogido en la variable states.
       

    #Función que recibe un conjunto de estados
    #y los completa con lambdas.
    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        for transition in self.automaton.transitions:
            if transition.initial_state in set_to_complete:
                if transition.symbol is None:
                    set_to_complete.add(transition.final_state)


    #Función que devuelve un valor booleano si
    #hay algun estado final.
    def is_accepting(self) -> bool:
        for state in self.current_states:                       #Para cada estado de los estados actuales
            if state.is_final:                                  #si el estado es un estado final
                return True                                     #devolvemos True
        return False                                            #Si no hay ningun estado que se encuentre en los actuales, devolvemos False
