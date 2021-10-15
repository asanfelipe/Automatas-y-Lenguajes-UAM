"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton, State, Transition
from automata.re_parser_interfaces import AbstractREParser
from typing import Collection


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:

        q0 = State(str(super.state_counter), False)

        super.state_counter += 1
        qf = State(str(super.state_counter), True)

        listaEstados = [q0, qf]
        return FiniteAutomaton(q0, listaEstados, [], [])

    def _create_automaton_lambda(
        self,
    ) -> FiniteAutomaton:

        q0 = State(str(super.state_counter), False)

        super.state_counter += 1
        qf = State(str(super.state_counter), True)

        listaEstados = [q0, qf]
        transiciones = Collection[Transition(q0, None, qf)]
        return FiniteAutomaton(q0, listaEstados, [], transiciones)

    def _create_automaton_symbol(
        self,
        symbol: str,
    ) -> FiniteAutomaton:

        q0 = State(str(super.state_counter), False)

        super.state_counter += 1
        qf = State(str(super.state_counter), True)

        listaEstados = [q0, qf]
        transiciones = Collection[Transition(q0, symbol, qf)]
        sym = Collection[symbol]
        return FiniteAutomaton(q0, listaEstados, sym, transiciones)

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
