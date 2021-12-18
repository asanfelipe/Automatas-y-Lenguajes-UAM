import unittest
from typing import AbstractSet

from grammar import Grammar
from utils import GrammarFormat

class TestFirst(unittest.TestCase):
    def _check_first(
        self,
        grammar: Grammar,
        input_string: str,
        first_set: AbstractSet[str],
    ) -> None:
        with self.subTest(
            string=f"First({input_string}), expected {first_set}",
        ):
            computed_first = grammar.compute_first(input_string)
            self.assertEqual(computed_first, first_set)

    def test_case1(self) -> None:
        """Test Case 1."""
        grammar_str = """
        E -> TX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "E", {'(', 'i'})
        self._check_first(grammar, "T", {'(', 'i'})
        self._check_first(grammar, "X", {'', '+'})
        self._check_first(grammar, "Y", {'', '*'})
        self._check_first(grammar, "", {''})
        self._check_first(grammar, "Y+i", {'+', '*'})
        self._check_first(grammar, "YX", {'+', '*', ''})
        self._check_first(grammar, "YXT", {'+', '*', 'i', '('})

    def test_case2(self) -> None:
        """Test case 2."""
        grammar_str = """
        E -> TY
        T -> EXY
        X -> *
        E -> i
        E ->
        Y -> (E)
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "E", {"i", "*"})
        self._check_first(grammar, "T", {"i", "*"})
        self._check_first(grammar, "X", {"*"})
        self._check_first(grammar, "Y", {"("})

    def test_case3(self) -> None:
        """Test case 3."""
        grammar_str = """
        E-> TY
        T-> EXY
        T -> 
        X -> *
        E -> i
        E ->
        Y -> (E)
        Y ->
        """
        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "E", {"i", "(", "*", ""})
        self._check_first(grammar, "T", {"i", "(", "*"})
        self._check_first(grammar, "X", {"*"})
        self._check_first(grammar, "Y", {"(", ""})    

    
if __name__ == '__main__':
    unittest.main()
