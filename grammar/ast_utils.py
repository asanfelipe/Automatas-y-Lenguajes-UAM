import ast
import numbers
import types
import inspect
from typing import Optional, Union, List

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


class ASTDotVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.root = 0
        self.n_node = 0
        self.last_parent: Optional[int] = None
        self.last_field_name = ""

    def generic_visit(self, node: ast.AST) -> None:
        if self.root == 0:
            print("digraph {")

        node_string = f's{self.n_node} [label = "{type(node).__name__}('
        node_arguments = ""
        current_node = self.n_node
        if self.last_parent is not None:
            print(f's{self.last_parent} -> s{self.n_node} [label = "{self.last_field_name}"]')

        self.n_node += 1
        self.root += 1
        for field, value in ast.iter_fields(node):
            self.last_field_name = str(field)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.last_parent = current_node
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.last_parent = current_node
                self.visit(value)
            else:
                node_arguments += f'{field}={value!r}, '


        self.root -= 1
        if node_arguments != "":
            node_arguments = node_arguments[:-2]

        print(node_string + node_arguments + ')"]')

        if self.root == 0:
            print("}")

class ASTReplaceNum(ast.NodeTransformer):
    def __init__(self, number: complex) -> None:
        self.number = number

    def visit_Num(self, node: ast.Num):
        return ast.Num(self.number)

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, numbers.Number):
            return ast.Constant(self.number)
        return node
    
def transform_code(f, transformer):
    f_ast = ast.parse(inspect.getsource(f))
    new_tree = ast.fix_missing_locations(transformer.visit(f_ast))
    old_code = f.__code__
    code = compile(new_tree, old_code.co_filename, 'exec')
    new_f = types.FunctionType(code.co_consts[0], f.__globals__)
    return new_f
    
class ASTRemoveConstantIf(ast.NodeTransformer):
    def visit_If(self, node: ast.If) -> Union[ast.AST, List[ast.stmt]]:
        self.generic_visit(node)

        if isinstance(node.test, ast.Constant) or isinstance(node.test, ast.NameConstant):
            if node.test.value:
                return node.body
            else:
                if not node.test.value:
                    node.body = node.orelse
                    return node.orelse
        return node
    
