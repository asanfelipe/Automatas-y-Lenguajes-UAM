import ast
import numbers

class ASTMagicNumberDetector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.magic_numbers=0

    def _check_magic_number(self, number:complex) -> None:
        if isinstance(number, numbers.Number):
            if number != 0 | number != 1 | number != 1j:
                self.magic_numbers = self.magic_numbers + 1

    def visit_Num(self, node:ast.Num) -> None:
        self._check_magic_number(node.n)

    def visit_Constant(self, node: ast.Constant) -> None:
        self._check_magic_number(node.value)