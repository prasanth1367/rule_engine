import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from engine.ast_builder import create_rule, combine_rules, Node
from db.models import store_rule, retrieve_rule, get_all_rules, delete_rule
from engine.evaluator import evaluate  # Ensure this matches the function name in evaluator.py

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/routes', methods=['GET'])
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        output.append(f"{rule.method} {rule.rule}")
    return jsonify(output)

# Endpoint to create and store a rule
@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    try:
        rule_string = request.json['rule']
        rule_name = request.json.get('rule_name', 'default_rule_name')
        print(f"Creating rule: {rule_name} with string: {rule_string}")  # Debug output
        rule_ast = create_rule(rule_string)
        store_rule(rule_name, rule_string, rule_ast)
        return jsonify({'message': 'Rule created successfully', 'rule_name': rule_name}), 201
    except Exception as e:
        print(f"Error in creating rule: {e}")  # Debug output
        return jsonify({'error': str(e)}), 400

# Endpoint to combine multiple rules into a single AST and store it
@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    try:
        rules = request.json.get('rules', [])
        if not isinstance(rules, list) or not all(isinstance(rule, str) for rule in rules):
            return jsonify({'error': 'Invalid input format. Expected a list of rule strings.'}), 400

        combined_ast = combine_rules(rules)
        combined_rule_name = request.json.get('combined_rule_name', 'default_combined_rule')
        
        store_rule(combined_rule_name, ' AND '.join(rules), combined_ast)
        
        return jsonify({
            'combined_ast': combined_ast.to_dict(),
            'message': f'Combined rule stored as {combined_rule_name}'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    data = request.json
    rule_id = data.get('rule_id')
    input_data = data.get('data')

    # Ensure rule_id is treated as a string
    if isinstance(rule_id, int):
        rule_id = str(rule_id)

    # Validate input data
    if not rule_id or not input_data:
        return jsonify({'error': 'Rule ID and input data are required'}), 400

    # Check if the expected keys exist in input_data
    required_keys = ['age', 'income', 'department']
    missing_keys = [key for key in required_keys if key not in input_data]
    if missing_keys:
        return jsonify({'error': f'Missing keys in input data: {", ".join(missing_keys)}'}), 400

    # Fetch the rule AST from the database
    print(f"Retrieving rule '{rule_id}' from the database")
    rule_ast = retrieve_rule(rule_id)
    
    # Ensure rule_ast is a Node instance, if not, convert it
    if isinstance(rule_ast, str):  # If it’s a string, you may need to parse it
        rule_ast = Node.from_dict(json.loads(rule_ast))  # Assuming the string is in JSON format

    if rule_ast is None or not isinstance(rule_ast, Node):
        return jsonify({'error': 'Rule not found or invalid AST'}), 404

    try:
        print(f"Evaluating rule '{rule_id}' with data: {input_data}")
        # Evaluate the rule with the provided data
        result = evaluate(rule_ast, input_data)
        return jsonify({'result': result}), 200
    except ValueError as e:
        return jsonify({'error': f'Value error: {str(e)}'}), 400
    except TypeError as e:
        return jsonify({'error': f'Type error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred during evaluation: {str(e)}'}), 400


# Endpoint to get a list of all rule names
@app.route('/get_all_rules', methods=['GET'])
def get_all_rules_api():
    try:
        rules = get_all_rules()  # Get all rule names
        return jsonify({'rules': rules}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint to delete a rule by name
@app.route('/delete_rule', methods=['DELETE'])
def delete_rule_api():
    try:
        rule_name = request.json['rule_name']  # Get rule name to delete
        delete_rule(rule_name)  # Delete the rule from the database
        return jsonify({'message': f'Rule {rule_name} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/modify_rule', methods=['PUT'])
def modify_rule_api():
    try:
        rule_name = request.json['rule_name']
        new_rule_string = request.json['new_rule']  # Expecting the modified rule string
        
        print(f"Modifying rule: {rule_name} to new rule: {new_rule_string}")  # Debug output

        # Validate new rule
        if not is_valid_rule(new_rule_string):
            return jsonify({'error': 'Invalid rule syntax'}), 400

        # Attempt to create AST from the new rule
        try:
            new_rule_ast = create_rule(new_rule_string)  # Create AST from the new rule
        except SyntaxError as se:
            return jsonify({'error': f'Syntax error in rule: {str(se)}'}), 400
        
        store_rule(rule_name, new_rule_string, new_rule_ast)  # Update the rule in the database
        
        return jsonify({'message': 'Rule modified successfully', 'rule_name': rule_name}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Function to validate rule syntax
def is_valid_rule(rule_string):
    valid_operators = ['>', '<', '>=', '<=', '==', '!=']
    return any(op in rule_string for op in valid_operators)

# Print all registered routes for debugging
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    app.run(debug=True)
