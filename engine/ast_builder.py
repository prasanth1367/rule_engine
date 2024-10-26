import ast

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        return {
            'node_type': self.node_type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            node_type=data['node_type'],
            value=data.get('value'),  # Use .get to avoid KeyError
            left=cls.from_dict(data['left']),
            right=cls.from_dict(data['right'])
        )


def create_rule(rule_string):
    print(f"Creating rule from string: {rule_string}")  # Debug output
    # Use `eval` to parse and create the rule expression
    tree = ast.parse(rule_string, mode='eval')
    ast_representation = _tree_to_ast(tree.body)
    print(f"AST Representation: {ast_representation.to_dict()}")  # Print as dict for better readability
    return ast_representation


def _get_operator_string(op):
    # Mapping AST comparison operators to string representations
    if isinstance(op, ast.Gt):
        return ">"
    elif isinstance(op, ast.Lt):
        return "<"
    elif isinstance(op, ast.Eq):
        return "=="
    elif isinstance(op, ast.GtE):
        return ">="
    elif isinstance(op, ast.LtE):
        return "<="
    elif isinstance(op, ast.NotEq):
        return "!="
    return None

def _tree_to_ast(node):
    if isinstance(node, ast.BoolOp):
        op = 'AND' if isinstance(node.op, ast.And) else 'OR'
        # Handle multiple values for BoolOps (AND/OR)
        left = _tree_to_ast(node.values[0])
        right = _tree_to_ast(node.values[1])
        return Node(node_type='operator', left=left, right=right, value=op)
    
    elif isinstance(node, ast.Compare):
        left = _tree_to_ast(node.left)
        comparator = node.comparators[0]
        op = _get_operator_string(node.ops[0])

        if isinstance(comparator, ast.Constant):
            comparator_value = comparator.value
        else:
            raise ValueError("Unsupported comparator type")

        return Node(node_type='operand', value=f'{left.value} {op} {comparator_value}')

    elif isinstance(node, ast.Constant):
        return Node(node_type='operand', value=node.value)

    elif isinstance(node, ast.Name):
        return Node(node_type='operand', value=node.id)

    return None  # Handle unsupported node types

def combine_rules(rules):
    nodes = [create_rule(rule) for rule in rules]
    # Implementing a simple combination logic
    if len(nodes) == 0:
        return None
    
    # Create a combined 'AND' node
    combined_node = Node(node_type='operator', value='AND', left=nodes[0])
    
    current_node = combined_node
    for node in nodes[1:]:
        # Combine the current node with the next node
        current_node.right = node
        current_node = node  # Move to the next node
    
    return combined_node
