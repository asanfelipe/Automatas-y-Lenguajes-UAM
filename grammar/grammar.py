from __future__ import annotations

from collections import deque
from typing import AbstractSet, Collection, MutableSet, Optional
from typing import Union, List

class RepeatedCellError(Exception):
    """Exception for repeated cells in LL(1) tables."""

class SyntaxError(Exception):
    """Exception for parsing errors."""

class Production:
    """
    Class representing a production rule.
    Args:
        left: Left side of the production rule. It must be a character
            corresponding with a non terminal symbol.
        right: Right side of the production rule. It must be a string
            that will result from expanding ``left``.
    """

    def __init__(self, left: str, right: str) -> None:
        self.left = left
        self.right = right

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.left == other.left
            and self.right == other.right
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.left!r} -> {self.right!r})"
        )

    def __hash__(self) -> int:
        return hash((self.left, self.right))

class Grammar:
    """
    Class that represent a grammar.

    Args:
        terminals: Terminal symbols of the grammar.
        non_terminals: Non terminal symbols of the grammar.
        productions: Production rules of the grammar.
        axiom: Axiom of the grammar.

    """

    def __init__(
        self,
        terminals: AbstractSet[str],
        non_terminals: AbstractSet[str],
        productions: Collection[Production],
        axiom: str,
    ) -> None:
        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        if axiom not in non_terminals:
            raise ValueError(
                "Axiom must be included in the set of non terminals.",
            )

        for p in productions:
            if p.left not in non_terminals:
                raise ValueError(
                    f"{p}: "
                    f"Left symbol {p.left} is not included in the set "
                    f"of non terminals.",
                )
            if p.right is not None:
                for s in p.right:
                    if (
                        s not in non_terminals
                        and s not in terminals
                    ):
                        raise ValueError(
                            f"{p}: "
                            f"Invalid symbol {s}.",
                        )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.axiom = axiom

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"axiom={self.axiom!r}, "
            f"productions={self.productions!r})"
        )


    def compute_first(self, sentence: str) -> AbstractSet[str]:
        """
        Method to compute the first set of a string.

        Args:
            str: string whose first set is to be computed.

        Returns:
            First set of str.
        """

        conjunto = set()
        return self.compute_first_set(sentence, conjunto)

    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        """
        Method to compute the follow set of a non-terminal symbol.

        Args:
            symbol: non-terminal whose follow set is to be computed.

        Returns:
            Follow set of symbol.
        """

        conjunto = set()
        return self.compute_follow_set(symbol, conjunto)

    def compute_first_set(self, sentence: str, visited: AbstractSet[str]) -> AbstractSet[str]:

        conjunto_primeros = set() #inicializamos un set vacio

        if (sentence == "") or (sentence is None): #si la sentencia esta vacia devolvemos vacio
            conjunto_primeros.add("")
            return conjunto_primeros
        for symbol in sentence: #para cada simbolo de la sentencia
            if symbol in self.terminals: #si el simbolo esta en los terminales
                conjunto_primeros.add(symbol) #se añade y devuelve
                return conjunto_primeros
            else:
                if symbol in self.non_terminals: #si el simbolo esta en los no terminales
                    for production in self.productions: #para cada produccion de todas
                        if (production.left == symbol) and (production not in visited): #si la produccion de la izquierda es la misma que el simbolo
                            visited.add(production) #se añade al set de visitados
                            conjunto_primeros.update(self.compute_first_set(production.right, visited)) #se actualiza el set first
                    if "" not in conjunto_primeros: #si lambda no está en el conjunto se devuelve
                        return conjunto_primeros
                    else:
                        conjunto_primeros.remove("") #si lambda está en first, lo elimina
                else:
                    raise ValueError("Symbol not expected")

        conjunto_primeros.add("") #añade lambda al set
        return conjunto_primeros

    def compute_follow_set(self, symbol: str, visited: AbstractSet[str]) -> AbstractSet[str]:
        conjunto_siguientes = set()

        for production in self.productions:
            right = production.right
            while symbol in right:
                index = right.index(symbol)
                right = right[index+1:] #iguala la derecha a partir del indice+1
                conjunto_siguientes.update(self.compute_first(right))
            if "" in conjunto_siguientes:
                conjunto_siguientes.remove("")
                if production.left not in visited:
                    visited.add(production.left)
                    conjunto_siguientes.update(self.compute_follow_set(production.left, visited))
                    
        if symbol not in self.non_terminals:
            raise ValueError("Not valid Symbol")
        if symbol == self.axiom:
            conjunto_siguientes.add('$')

        return conjunto_siguientes
	

    def get_ll1_table(self) -> Optional[LL1Table]:
        """
        Method to compute the LL(1) table.

        Returns:
            LL(1) table for the grammar, or None if the grammar is not LL(1).
        """
        cells = []
        for production in self.productions:
            first = self.compute_first(production.right)
            for element in first:
                if element in self.terminals:
                    cells.append(TableCell(production.left, element, production.right))
                elif element == "":
                    follows = self.compute_follow(production.left)
                    if "$" in follows:
                        cells.append(TableCell(production.left, "$", production.right))
                    for follow in follows:
                        if follow in self.terminals:
                            cells.append(TableCell(production.left, follow, production.right))

        return LL1Table(self.non_terminals, self.terminals.union("$"), cells)


    def is_ll1(self) -> bool:
        return self.get_ll1_table() is not None

class TableCell:
    """
    Cell of a LL1 table.
    Args:
        non_terminal: Non terminal symbol.
        terminal: Terminal symbol.
        right: Right part of the production rule.
    """

    def __init__(self, non_terminal: str, terminal: str, right: str) -> None:
        self.non_terminal = non_terminal
        self.terminal = terminal
        self.right = right

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.non_terminal == other.non_terminal
            and self.terminal == other.terminal
            and self.right == other.right
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.non_terminal!r}, {self.terminal!r}, "
            f"{self.right!r})"
        )

    def __hash__(self) -> int:
        return hash((self.non_terminal, self.terminal))

class LL1Table:
    """
    LL1 table.
    Args:
        non_terminals: Set of non terminal symbols.
        terminals: Set of terminal symbols.
        cells: Cells of the table.
    """

    def __init__(
        self,
        non_terminals: AbstractSet[str],
        terminals: AbstractSet[str],
        cells: Collection[TableCell],
    ) -> None:

        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        for c in cells:
            if c.non_terminal not in non_terminals:
                raise ValueError(
                    f"{c}: "
                    f"{c.non_terminal} is not included in the set "
                    f"of non terminals.",
                )
            if c.terminal not in terminals:
                raise ValueError(
                    f"{c}: "
                    f"{c.terminal} is not included in the set "
                    f"of terminals.",
                )
            for s in c.right:
                if (
                    s not in non_terminals
                    and s not in terminals
                ):
                    raise ValueError(
                        f"{c}: "
                        f"Invalid symbol {s}.",
                    )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.cells = {(c.non_terminal, c.terminal): c.right for c in cells}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"cells={self.cells!r})"
        )

    def add_cell(self, cell: TableCell) -> None:
        """
        Adds a cell to an LL(1) table.
        Args:
            cell: table cell to be added.
        Raises:
            RepeatedCellError: if trying to add a cell already filled.
        """
        if (cell.non_terminal, cell.terminal) in self.cells:
            raise RepeatedCellError(
                f"Repeated cell ({cell.non_terminal}, {cell.terminal}).")
        else:
            self.cells[(cell.non_terminal, cell.terminal)] = cell.right

    def analyze(self, input_string: str, start: str) -> ParseTree:
        """
        Method to analyze a string using the LL(1) table.
        Args:
            input_string: string to analyze.
            start: initial symbol.
        Returns:
            ParseTree object with either the parse tree (if the elective exercise is solved)
            or an empty tree (if the elective exercise is not considered).
        Raises:
            SyntaxError: if the input string is not syntactically correct.
        """
        stack = []
        stack.append("$")

        for element in start[::-1]:
            tree = ParseTree(element)
            stack.append((element, tree))
            if element == start[-1]:
                root = tree

        while len(stack) != 1:
            top_tuple = stack.pop()
            current_tree = top_tuple[1]
            top = top_tuple[0]

            if top in self.non_terminals and len(input_string):
                first_input = input_string[0]
                if (top, first_input) in self.cells.keys():
                    new_top = self.cells[(top, first_input)]
                    if new_top or new_top == '':
                        children = []
                        if new_top == "":
                            child = ParseTree("λ")
                            children.append(child)
                        for element in new_top[::-1]:
                            child = ParseTree(element)
                            children.append(child)
                            stack.append((element, child))
                        current_tree.add_children(children[::-1])
                    else:
                        raise SyntaxError("String is not syntactically correct.") 
                else:
                    raise SyntaxError("String is not syntactically correct.") 

            elif top in self.terminals:
                if len(input_string) != 0:
                    if top == input_string[0]:
                        if input_string != "$":
                            input_string = input_string[1:]
                    else:
                        raise SyntaxError("String is not syntactically correct.") 
                else:
                    raise SyntaxError("String is not syntactically correct.") 
            else:
                raise SyntaxError("String is not syntactically correct.") 

        if(len(input_string) != 1):
            raise SyntaxError("String is not syntactically correct.") 

        return root

class ParseTree():
    """
    Parse Tree.
    Args:
        root: root node of the tree.
        children: list of children, which are also ParseTree objects.
    """
    def __init__(self, root: str, children: Collection['ParseTree'] = []) -> None:
        self.root = root
        self.children = children

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.root!r}: {self.children})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.root == other.root
            and len(self.children) == len(other.children)
            and all([x.__eq__(y) for x, y in zip(self.children, other.children)])
        )

    def add_children(self, children: Collection['ParseTree']) -> None:
        self.children = children