"""Conversion from regex to automata."""
from automaton import FiniteAutomaton, State, Transition
from re_parser_interfaces import AbstractREParser
#from typing import Collection #Esto no hace falta


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:

        #Creamos un estado q0 con el nombre (que es un contador) y diciendole que no es un estado final.
        #Necesitamos añadir la asignación (name=, is_final=) ya que los argumentos que recibe
        #FiniteAutomaton son keyword-only
        q0 = State(name=str(self.state_counter), is_final=False)
        #Incrementamos el valor del contador.
        self.state_counter += 1
        
        #Hacemos lo mismo con qf
        qf = State(name=str(self.state_counter), is_final=True)
        self.state_counter += 1
        
        #Almacenamos en una lista los estados creados anteriormente.
        listaEstados = [q0, qf]

        #Como los argumentos que recibe FiniteAutomaton son keyword-only, añadimos lo comentado anteriormente
        #de initial_state=, states=, ..., etc
        return FiniteAutomaton(initial_state=q0, states=listaEstados, symbols=[], transitions=[])

    def _create_automaton_lambda(
        self,
    ) -> FiniteAutomaton:

        q0 = State(name=str(self.state_counter), is_final=False)
        self.state_counter += 1
        
        qf = State(name=str(self.state_counter), is_final=True)
        self.state_counter += 1
        
        listaEstados = [q0, qf]
        transiciones = [Transition(q0, None, qf)]
        
        return FiniteAutomaton(initial_state=q0, states=listaEstados, symbols=[], transitions=transiciones)

    def _create_automaton_symbol(
        self,
        symbol: str,
    ) -> FiniteAutomaton:

        q0 = State(name=str(self.state_counter), is_final=False)
        self.state_counter += 1
        
        qf = State(name=str(self.state_counter), is_final=True)
        self.state_counter += 1

        listaEstados = [q0, qf]
        transiciones = [Transition(q0, symbol, qf)]
        sym = [symbol]
        
        return FiniteAutomaton(initial_state=q0, states=listaEstados, symbols=sym, transitions=transiciones)

    def _create_automaton_star(
        self,
        automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:

        #En todos los automatas restantes hay que averiguar cómo se especifican un símbolo o un estado concreto
        transiciones = [automaton.transitions, Transition(automaton.states, automaton.symbols, automaton.states)]

        return FiniteAutomaton(initial_state=automaton.initial_state, states=automaton.states, symbols=automaton.symbols, transitions=transiciones)

    def _create_automaton_union(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        
        q0 = State(name=str(self.state_counter), is_final=False)
        self.state_counter += 1
        
        qf = State(name=str(self.state_counter), is_final=True)
        self.state_counter += 1

        listaEstados = [q0, automaton1.states, automaton2.states, qf]
        sym = [automaton2.symbols, automaton1.symbols]

        for s in automaton1.states:
            if s.is_final:
                t_final1=Transition(s, sym, qf)

        for s in automaton2.states:
            if s.is_final:
                t_final2=Transition(s, sym, qf)

        transiciones = [automaton1.transitions, automaton2.transitions, Transition(q0, sym, automaton1.initial_state), 
            Transition(q0, sym, automaton2.initial_state), t_final1, t_final2]


        return FiniteAutomaton(initial_state=q0, states=listaEstados, symbols=sym, transitions=transiciones)

    def _create_automaton_concat(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        
        listaEstados = [automaton1.states, automaton2.states]
        sym = [automaton1.symbols, automaton2.symbols]

        for s in automaton1.states:
            if s.is_final:
                t_final=Transition(s, sym, automaton2.initial_state)

        transiciones = [automaton1.transitions, automaton2.transitions, t_final]

        return FiniteAutomaton(initial_state=automaton1.initial_state, states=listaEstados, symbols=sym, transitions=transiciones)
