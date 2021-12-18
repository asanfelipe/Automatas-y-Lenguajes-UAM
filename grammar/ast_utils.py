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
        self.root = 1

        new_nodes = []
        for field, value in ast.iter_fields(node):
            if (not isinstance(value, list)) and (not isinstance(value, ast)):
                new_nodes.append(field, value)

        node = 's{}'.format(self.n_node)
        node += '[label="{}()"'.format(type(node).__name__)
        print(node)
        actual_node = self.n_node
        self.n_node += 1

        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, type(ast)):
                        self.last_parent = actual_node
                        self.last_field_name = field
                        self.visit(item)
            elif isinstance(value, ast):
                self.last_parent = actual_node
                self.last_field_name = field
                self.visit(value)
        self.root = 0
        if self.root == 0:
            print("}")

# usar un esquema similar al generic_visit de la clase padre para recorrer los hijos del nodo actual
# obtener los nodos hijos (nodos AST y listas de nodos AST) del nodo actual
# obtener los campos hijos (el resto) del nodo actual
# procesar todos los campos hijos obtenidos del nodo actual (imprimir sus valores)
# procesar todos los nodos hijos obtenidos del nodo actual (llamada a visit)

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
        body_bool = True
        orelse_bool = True
        body_elem = []
        orelse_elem = []

        if isinstance(node.test, ast.NameConstant):
            if node.test.value:
                orelse_bool = False
            else:
                body_bool = False

        if body_bool == True:
            for elem in node.body:
                child = self.visit(elem)
                if isinstance(child, ast.AST):
                    body_elem.append(child) #Append añade a la lista un elemento en formato lista
                else:
                    body_elem.extend(child) #Extend añade a la lista los elementos sin formato lista
            if not orelse_bool:
                return body_elem

        if orelse_bool == True:
            for elem in node.orelse:
                child = self.visit(elem)
                if isinstance(child, ast.AST):
                    orelse_elem.append(child)
                else:
                    orelse_elem.extend(child)
            if not body_bool:
                return orelse_elem

        node.body = body_elem
        node.orelse = orelse_elem
        return node
    
