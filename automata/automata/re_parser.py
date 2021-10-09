"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton, State, Transition
from automata.re_parser_interfaces import AbstractREParser


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:

        listaEstados = [State('inicial', False), State('final', True)]
        return FiniteAutomaton(listaEstados[0], listaEstados, [], [])

    def _create_automaton_lambda(
        self,
    ) -> FiniteAutomaton:
        listaEstados = [State('inicial', False), State('final', True)]
        transicion = Transition(listaEstados[0], None, listaEstados[1])
        return FiniteAutomaton(listaEstados[0], listaEstados, [], transicion)

    def _create_automaton_symbol(
        self,
        symbol: str,
    ) -> FiniteAutomaton:
        raise NotImplementedError("This method must be implemented.")

    def _create_automaton_star(
        self,
        automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:
        raise NotImplementedError("This method must be implemented.")

    def _create_automaton_union(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        raise NotImplementedError("This method must be implemented.")

    def _create_automaton_concat(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        raise NotImplementedError("This method must be implemented.")
