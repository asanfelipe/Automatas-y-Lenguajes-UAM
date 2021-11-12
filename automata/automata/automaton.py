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
        
    """
    Nuestra idea para hacer to_deterministic:
    1. Creamos una nueva funcion llamada accesibleStates, a la que llamamos con un estado inicial y unos simbolos.
        Esta funcion nos devolvera una lista de estados accesibles a los que se puede acceder desde el estado con los simbolos
        que hemos pasado a la funcion.
    2. En to_deterministic, para cada estado que hemos recogido en la lista de estados accesibles que nos ha sido devuelta por 
        accesibleStates, lo recorremos para ver a que estados nuevos nos podemos mover con el primer simbolo (usando accesibleStates)
        y esos estados o estado lo almacenamos en una variable con set, para que si hay estados repetidos, no se repitan.
    3. Para almacenar los resultados utilizaremos un diccionario, ejemplo:
        Diccionario = {'a': {set de states: set de states} , 'b':{set de states: set de states} , ...}
	    Diccionario['a'][{0,1,2,5,f}] = {3}
    4. Comprobamos si el resultado del paso 2 es distinto de vacío y si se encuentra en Diccionario['a'].keys(). Si no es asi
        lo añadimos.
    5. Hacemos lo mismo que en el paso 2 pero con otro símbolo y cuando terminemos hacemos lo mismo que en el paso 4.
        En resumen, hacemos un bucle for para cada símbolo.
    6. Después y si todo se ha realizado correctamente, deberíamos tener todos los datos necesarios almacenados en el diccionario
        para poder crear el automata determinista.
    """      

    def accesibleStates(
            self,
            start_state: State,
            symbol,
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
        
        import automaton_evaluator 

        set_estados = {}
        diccionario = {}

        for s in self.symbols:
            set_estados = accesibleStates(self.initial_state, s)
            if set_estados != None & set_estados not in diccionario[s].keys():
                diccionario[s] = set_estados

        # lista_transiciones = []

        # for t in self.transitions:
        #     if t.symbol == None:
        #         if t.final_state.is_final:
        #             q0 = State(name=str(t.initial_state.name + t.final_state.name), is_final=True)
        #             ##############################Este algoritmo repite estados##################################
        #             lista_estados.append(q0)
        #         else:
        #             q0 = State(name=str(t.initial_state.name + t.final_state.name), is_final=False)
        #             ##############################Este algoritmo repite estados##################################
        #             lista_estados.append(q0)
        #         for aux1 in self.transitions:
        #             if aux1.final_state == t.initial_state:
        #                 lista_transiciones.append(Transition(aux1.final_state, aux1.symbol, q0))
        #         for aux2 in self.transitions:
        #             if aux2.initial_state == t.final_state:
        #                 lista_transiciones.append(Transition(q0, aux2.symbol, aux2.initial_state))



    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
