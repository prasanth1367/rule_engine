import psycopg2
import json
import logging
from engine.ast_builder import Node

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        return psycopg2.connect(
            dbname="rule_engine_db",
            user="postgres",
            password="prasanth",
            host='localhost',
            port='5432'
        )
    except psycopg2.DatabaseError as e:
        logger.error(f"Database connection error: {e}")
        return None

def store_rule(rule_name: str, rule_string: str, rule_ast: Node) -> bool:
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    '''
                    INSERT INTO rules (rule_name, rule_string, ast)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (rule_name) DO UPDATE
                    SET rule_string = EXCLUDED.rule_string, ast = EXCLUDED.ast
                    ''',
                    (rule_name, rule_string, json.dumps(rule_ast.to_dict()))  # Store AST as JSON
                )
        logger.info(f"Rule '{rule_name}' stored/updated successfully.")
        return True
    except psycopg2.Error as e:
        logger.error(f"Error storing rule: {e}")
        return False
    finally:
        conn.close()

def retrieve_rule(rule_name: str) -> Node:
    logger.info(f"Retrieving rule with name: {rule_name}")
    conn = get_db_connection()
    if conn is None:
        logger.error("Database connection failed.")
        return None
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT ast FROM rules WHERE rule_name = %s", (rule_name,))
                result = cur.fetchone()
                logger.info(f"Query result: {result}")
                if result is None:
                    logger.warning(f"Rule '{rule_name}' not found in the database.")
                    return None

                ast_dict = result[0]
                logger.info(f"Retrieved rule AST: {ast_dict}")
                return Node.from_dict(ast_dict)
    except psycopg2.Error as e:
        logger.error(f"Error retrieving rule: {e}")
        return None
    finally:
        conn.close()

def get_all_rules() -> list:
    conn = get_db_connection()
    if conn is None:
        return []
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT rule_name FROM rules")
                return [row[0] for row in cur.fetchall()]
    except psycopg2.Error as e:
        logger.error(f"Error fetching all rules: {e}")
        return []
    finally:
        conn.close()

def delete_rule(rule_name: str) -> bool:
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM rules WHERE rule_name = %s", (rule_name,))
        logger.info(f"Rule '{rule_name}' deleted successfully.")
        return True
    except psycopg2.Error as e:
        logger.error(f"Error deleting rule: {e}")
        return False
    finally:
        conn.close()

def evaluate_rule(rule_name: str, input_data: dict) -> bool:
    ast = retrieve_rule(rule_name)
    if ast is None:
        logger.warning(f"Rule '{rule_name}' not found.")
        return None

    try:
        logger.info(f"Evaluating AST for rule '{rule_name}' with input data: {input_data}")
        result = ast.evaluate(input_data)  # Ensure that Node has an evaluate method
        return result
    except Exception as e:
        logger.error(f"Error evaluating rule '{rule_name}': {e}")
        return None
