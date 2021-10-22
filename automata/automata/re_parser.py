"""Conversion from regex to automata."""
from automaton import FiniteAutomaton, State, Transition
from re_parser_interfaces import AbstractREParser
from automata.utils import write_dot
#from typing import Collection #Esto no hace falta
import sys
sys.path.append("D:/UNIVERSIDAD/1er cuatri/AUTLEN/PRACTICAS/P1/autlen21-22/automata/automata")



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

        #automaton = automaton.copy()
        q0 = State(name=str(self.state_counter), is_final=False)
        self.state_counter += 1
        
        qf = State(name=str(self.state_counter), is_final=True)
        self.state_counter += 1

        for s in automaton.states:
            if s.is_final:
                t_final=Transition(s, None, automaton.initial_state)

        t1 = Transition(q0, None, automaton.initial_state)
        t2 = Transition(q0, None, qf)
        
        for s in automaton.states:
            if s.is_final:
                t3=Transition(s, None, qf)
                s.is_final = False

        transiciones = list(automaton.transitions)
        transiciones.append(t_final)
        transiciones.append(t1)
        transiciones.append(t2)
        transiciones.append(t3)

        listaEstados = list(automaton.states)
        listaEstados.append(q0)
        listaEstados.append(qf)

        return FiniteAutomaton(initial_state=q0, states=listaEstados, symbols=automaton.symbols, transitions=transiciones)

    def _create_automaton_union(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        
        q0 = State(name=str(self.state_counter), is_final=False)
        self.state_counter += 1
        
        qf = State(name=str(self.state_counter), is_final=True)
        self.state_counter += 1

        listaEstados = list(automaton1.states) + list(automaton2.states)
        listaEstados.append(q0)
        listaEstados.append(qf)

        sym = set(automaton2.symbols) | set(automaton1.symbols)

        for s in automaton1.states:
            if s.is_final:
                t_final1=Transition(s, None, qf)
                s.is_final = False

        for s in automaton2.states:
            if s.is_final:
                t_final2=Transition(s, None, qf)
                s.is_final = False

        transiciones = list(automaton1.transitions) + list(automaton2.transitions)
        transiciones.append(Transition(q0, None, automaton1.initial_state)) 
        transiciones.append(Transition(q0, None, automaton2.initial_state))
        transiciones.append(t_final1)
        transiciones.append(t_final2)

        return FiniteAutomaton(initial_state=q0, states=listaEstados, symbols=sym, transitions=transiciones)

    def _create_automaton_concat(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        
        listaEstados = list(automaton1.states) + list(automaton2.states)
        sym = set(automaton1.symbols) | set(automaton2.symbols)

        for s in automaton1.states:
            if s.is_final:
                t_final=Transition(s, None, automaton2.initial_state)
                s.is_final = False

        transiciones = list(automaton1.transitions) + list(automaton2.transitions)
        transiciones.append(t_final)

        return FiniteAutomaton(initial_state=automaton1.initial_state, states=listaEstados, symbols=sym, transitions=transiciones)

#Añadido por nosotros para poder ver que los autómatas están bien creados
#Se puede ver el autómata dibujado en la página "dreampuf.github.io/GraphvizOnline/"
if __name__ == "__main__":
    e = REParser()
    #Autómata vacío
    empty_ = e._create_automaton_empty()
    print("AUTOMATA VACIO:")
    print(write_dot(empty_))
    print("#########################\n")
    #Autómata lambda
    lambda_ = e._create_automaton_lambda()
    print("AUTOMATA LAMBDA:")
    print(write_dot(lambda_))
    print("#########################\n")
    #Autómata símbolo
    symbol_ = e._create_automaton_symbol("a")
    print("AUTOMATA SIMBOLO:")
    print(write_dot(symbol_))
    print("#########################\n")
    #Autómata estrella
    star_ = e._create_automaton_star(symbol_)
    print("AUTOMATA ESTRELLA:")
    print(write_dot(star_))
    print("#########################\n")
    #Autómata unión
    symbol2_ = e._create_automaton_symbol("b")
    symbol1_ = e._create_automaton_symbol("a")
    union_ = e._create_automaton_union(symbol1_, symbol2_)
    print("AUTOMATA UNION:")
    print(write_dot(union_))
    print("#########################\n")
    #Autómata concatenado
    symbol2_ = e._create_automaton_symbol("b")
    symbol1_ = e._create_automaton_symbol("a")
    concat_ = e._create_automaton_concat(symbol1_, symbol2_)
    print("AUTOMATA CONCATENADO:")
    print(write_dot(concat_))
    print("#########################\n")