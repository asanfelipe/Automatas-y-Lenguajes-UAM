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
        f_symbols = self.symbols
        #Como el automata determinista no tiene lambdas, borramos ese símbolo
        f_symbols.remove(None)
   
        #Inicializamos una lista de estados que tendrá el automata determinista vacia
        f_states = []
        #Almacenamos en f_initial_state el primer elemento (un estado) del conjunto f_initial_state_set
        f_initial_state = State(str(f_initial_state_set))
        #Añadimos a los estados que tendrá el automata determinista el estado anterior
        f_states.append(f_initial_state)
        #Inicializamos una lista de transiciones que tendrá el automata determinista vacía
        f_transitions = []        
        
        while... #ESTO NO ESTA HECHO
                #AQUI HABRIA QUE VER ALGUNA MANERA DE QUE SE SIGA HACIENDO EL BUCLE FOR MIENTRAS NOS VAYAN SALIENDO ESTADOS NUEVOS
                #QUE NO TENEMOS EN LA LISTA DE ESTADOS DEL AUTOMATA DETERMINISTA (Y COMPROBAR QUE NO ESTÉ REPETIDO)
                
            #Para cada simbolo en los simbolos del automata
            for symbol in self.symbols:
                #Llamamos a process_symbol con dicho simbolo
                evaluator.process_symbol(symbol)
                #Almacenamos los estados a los que se llega con ese simbolo en una variable llamada result
                result = evaluator.current_states
                #Ahora tomamos como estados actuales los estados que se encontraban en la variable f_initial_state_set 
                evaluator.current_states = f_initial_state_set
                #Asignamos el estado "result" en la variable final_state
                final_state = State(str(result))
                #Añadimos a la lista de estados del automata determinista final_state
                f_states.append(final_state)
                #Añadimos la transición a la lista de transiciones con los datos recogidos
                f_transitions.append(Transition(f_initial_state, symbol, final_state))
           
        #ESTO NO ESTA HECHO
        #AL FINAL, SE DEBERIA RETORNAR EL FINITEAUTOMATON DANDOLE LOS VALORES QUE HEMOS RECOGIDO ANTERIORMENTE

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
