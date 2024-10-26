import re

def evaluate(ast, data):
    if ast.node_type == 'operator':
        left_result = evaluate(ast.left, data)
        right_result = evaluate(ast.right, data)
        
        print(f"Evaluating: {ast.value} -> left: {left_result}, right: {right_result}")  # Debug output
        
        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result

    elif ast.node_type == 'operand':
        try:
            # Adjusted regex to capture composite conditions
            match = re.match(r"(\w+)\s*(>=|<=|==|!=|>|<)\s*([\w'\" ]+)", ast.value)
            if not match:
                raise ValueError(f"Invalid operand format: {ast.value}")

            left, op, right = match.groups()
            left_value = data.get(left)

            if left_value is None:
                raise ValueError(f"{left} is missing from the input data")

            # Convert left_value to int if it's numeric
            if isinstance(left_value, str) and left_value.isdigit():
                left_value = int(left_value)

            # Handle right value (considering it might be quoted)
            if right.isdigit():
                right_value = int(right)
            else:
                right_value = right.strip("'\"")

            # Perform comparison based on the operator
            result = {
                '>': left_value > right_value,
                '<': left_value < right_value,
                '==': left_value == right_value,
                '!=': left_value != right_value,
                '>=': left_value >= right_value,
                '<=': left_value <= right_value
            }[op]

            print(f"Evaluating {left} {op} {right} -> {result}")  # Debug output
            return result

        except Exception as e:
            raise ValueError(f"Evaluation error: {str(e)}")

    return False  # Fallback for unsupported types
