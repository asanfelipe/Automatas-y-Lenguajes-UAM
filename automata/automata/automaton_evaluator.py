"""Evaluation of automata."""
from typing import Set

from automaton import FiniteAutomaton, State
from interfaces import AbstractFiniteAutomatonEvaluator


class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    #Función que recibe un símbolo y procesa si se avanza en los estados con él o no.
    def process_symbol(self, symbol: str) -> None:
        #Si el símbolo (letra, número...) no se encuentra en los símbolos del autómata
        if symbol not in self.automaton.symbols:
            #generamos un error que indique que el símbolo no se encuentra en el alfabeto.
            raise ValueError(
                "Symbol not included in alphabet"
            )
        #Creamos una nueva variable llamada states que se encuentra vacía al principio.
        states = set()
        #Para cada transición de las transiciones del autómata
        for transition in self.automaton.transitions:
            #si el estado inicial de la transición se encuentra en los estados actuales y el simbolo de la transición es el mismo que symbol
            if transition.initial_state in self.current_states and transition.symbol == symbol:
                #añade a la variable states el estado final al que se llega mediante esa transición.
                states.add(transition.final_state)
        #Llamamos a la función _complete_lambdas pasandole por referencia el conjunto de estados que hemos creado anteriormente.
        self._complete_lambdas(states)
        #Añadimos a los estados actuales todos los estados que hemos recogido en la variable states.
        self.current_states = states
       

    #Función que recibe un conjunto de estados y los completa con lambdas.
    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        #Almacenamos en la variable initial_len la longitud de los estados que tenemos que completar con lambdas.
        initial_len = len(set_to_complete)
        #Para cada transición del conjunto de transiciones del autómata
        for transition in self.automaton.transitions:
            #si el estado inicial de la transición se encuentra en el conjunto de estados a completar
            if transition.initial_state in set_to_complete:
                #y el simbolo de la transición es una lambda
                if transition.symbol is None:
                    #añadimos el estado final al conjunto de estados a completar.
                    set_to_complete.add(transition.final_state)
        #Si la longitud inicial es distinta de la longitud del conjunto de estados
        if (initial_len != len(set_to_complete)):
            #volvemos a llamar a la funcion _complete_lambdas con el conjunto de estados.
            self._complete_lambdas(set_to_complete)


    #Función que devuelve un valor booleano si hay algun estado final.
    def is_accepting(self) -> bool:
        #Para cada estado de los estados actuales
        for state in self.current_states:
            #si el estado es un estado final devolvemos True
            if state.is_final:
                return True
        #Si no hay ningun estado que se encuentre en los actuales, devolvemos False
        return False
