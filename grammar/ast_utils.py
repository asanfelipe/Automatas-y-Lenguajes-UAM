import ast
import numbers
class ASTMagicNumberDetector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.magic_numbers=0
    def check_magic_number(self, number:complex) -> None:
        if isinstance(number, numbers.Number):
            self.magic_numbers = self.magic_numbers + 1
    #def visit_Num(self, node:ast.Num) -> None:
