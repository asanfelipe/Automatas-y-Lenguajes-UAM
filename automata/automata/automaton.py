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

        #Importamos FiniteAutomatonEvaluator ya que usaremos sus funciones
        from automaton_evaluator import FiniteAutomatonEvaluator
        #Nos creamos un objeto de la clase FiniteAutomatonEvaluator
        evaluator = FiniteAutomatonEvaluator(self)
        #f_initial_state_set es el conjunto de estados actuales iniciales del evaluador y que serán estados del automata determinista
        f_initial_state_set = evaluator.current_states
        #f_symbols son los simbolos finales que tendrá el automata determinista
        # quitamos el None por si es AFD-lambda
        f_symbols = tuple(set(self.symbols) - {None})
   
        #Inicializamos un set de estados que tendrá el automata determinista vacia
        f_states = dict()
        #Almacenamos en f_initial_state el primer elemento (un estado) del conjunto f_initial_state_set
        state_name = ""
        for elem in sorted(f_initial_state_set):
            state_name += elem.name
        if state_name == "":
            state_name = "empty"
        f_initial_state = State(state_name)
        for estados in f_initial_state_set:
            if estados.is_final == True:
                f_initial_state.is_final = True
        #Añadimos a los estados que tendrá el automata determinista el estado anterior
        f_states[state_name] = f_initial_state
 
        #Inicializamos una lista de transiciones que tendrá el automata determinista vacía
        f_transitions = set()      
        
        #Recorremos todos los estados que hemos ido almacenando en el nuevo autómata finito para comprobar todas
        #las transiciones posibles para cada simbolo en los simbolos del automata
        f_states_asSet = [f_initial_state_set]
        new_states = [f_initial_state_set]
        evaluated_states = []
        while (new_states):
            for state in new_states:
                for symbol in f_symbols:
                    #Llamamos a process_symbol con dicho simbolo
                    evaluator.current_states = state
                    evaluator.process_symbol(symbol)
                    #Almacenamos los estados a los que se llega con ese simbolo en una variable llamada result
                    result = evaluator.current_states
                    #Ahora tomamos como estados actuales los estados que se encontraban en la variable f_initial_state_set 
                    evaluator.current_states = state
                    # if (not result):
                    #     continue
                    if result not in f_states_asSet:
                        f_states_asSet.append(result)
                    #Asignamos el estado "result" en la variable final_state
                    state_name = ""
                    for elem in sorted(result):
                        state_name += elem.name
                    if state_name == "":
                        state_name = "empty"
                    
                    if state_name in f_states:

                        final_state = f_states[state_name]

                    else:

                        final_state = State(state_name)
                        for estados in result:
                            if estados.is_final == True:
                                final_state.is_final = True

                        f_states[state_name] = final_state
                    
                    #Añadimos a la lista de estados del automata determinista initial_state                          
                    state_name = ""
                    for elem in sorted(state):
                        state_name += elem.name
                    if state_name == "":
                        state_name = "empty"
                        
                    if state_name in f_states:

                        initial_state = f_states[state_name]

                    else:

                        initial_state = State(state_name)
                        for estados in state:
                            if estados.is_final == True:
                                initial_state.is_final = True

                        f_states[state_name] = initial_state

                    #Añadimos la transición a la lista de transiciones con los datos recogidos
                    transicion = Transition(initial_state, symbol, final_state)
                    f_transitions.add(transicion)
                    
            evaluated_states = evaluated_states + new_states
            new_states = [elem for elem in f_states_asSet if elem not in evaluated_states] 

        #Almacenamos en un set los datos del diccionario
        states_set = set()
        for s in f_states.values():
            states_set.add(s)

        #Retornamos el autómata finito con los sets de datos que hemos ido almacenando
        return FiniteAutomaton(initial_state=f_initial_state, states=states_set, symbols=f_symbols, transitions=f_transitions)

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
