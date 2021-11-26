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


class ASTDotVisitor(ast.NodeVisitor):

    def __init__(self) -> None:
        self.level = 0
        self.n_node = 0
        self.last_parent: Optional[int] = None
        self.last_field_name = ""
    
    def generic_visit(self, node: ast.AST) -> None:
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        print(field)
                        print(item)
                        item.padre = node ########no estoy segura de esto#######
                        self.visit(item)
            elif isinstance(value, AST):
                print(field)
                print(value)
                value.padre = node ########no estoy segura de esto#######
                self.visit(value)

# usar un esquema similar al generic_visit de la clase padre para recorrer los hijos del nodo actual
# obtener los nodos hijos (nodos AST y listas de nodos AST) del nodo actual
# obtener los campos hijos (el resto) del nodo actual
# procesar todos los campos hijos obtenidos del nodo actual (imprimir sus valores)
# procesar todos los nodos hijos obtenidos del nodo actual (llamada a visit)