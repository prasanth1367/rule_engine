**Rule Engine Application**

**Objective**

The Rule Engine Application is designed to evaluate and process data based on user-defined rules, providing automated insights and responses. It supports integrating rule checking with custom logic, database operations, and a graphical user interface (GUI) for rule management.

**Project Structure**
bash
Copy code
rule_engine/
├── app.py                     # Main application script to run the rule engine
├── db/                        # Directory for database-related operations or files
├── engine/                    # Contains core logic for the rule evaluation
├── response.json              # Sample JSON response used for processing
├── rule_checker_gui.py        # GUI for managing and checking rules
├── venv/                      # Virtual environment for dependencies
└── __pycache__/               # Compiled Python files

**Tech Stack**
1. Programming Language: Python
2. Database: PostgreSQL


**Prerequisites**
1. Python 3.8+
2. Git
3. Visual Studio Code (VS Code)
Virtual Environment (recommended)

**Create and activate a virtual environment**

command:  python -m venv venv

**Activate the environment:**

1. On Windows: venv\Scripts\activate
2. On macOS/Linux: source venv/bin/activate

**Install Dependencies**

command: pip install -r requirements.txt

**Set Up Database**

This project uses PostgreSQL. Set up a PostgreSQL database with connection details configured in the main script or environment variables.

1. install the database
2. after installing create a database

**After creating the database create table in the psql**

command:

CREATE TABLE rules (
    id SERIAL PRIMARY KEY,         -- Auto-incrementing ID for each rule
    rule_name VARCHAR(255) UNIQUE, -- Unique name for the rule
    rule_string TEXT NOT NULL,     -- The actual rule string provided by the user
    rule_ast JSONB                 -- JSONB column to store the rule's AST
);

**For checking the table in databse**
1. open the psql command prompt
2. command: SELECT * FROM rules;

**Configuration**
1. Database Settings: Modify the configurations in the db/ directory as needed.
2. Rule Definitions: Update rule logic in the engine/ directory according to the application requirements.

**Running the Application**

Start the Main Application:

command: python app.py

**Launch the Rule Checker GUI:**

command: python rule_checker_gui.py


**Data for testing**
   1. create_rule: rule name: 1  rule string: "((age > 30 AND department = 'Sales') OR (salary > 50000))"
   2. evalute_ rule: rule name: 1  json data: {"age": 15,"department": "Sales","salary": 60000}
   3. combine_rule:   comma seperated-names and give required new rule name
   4. modify_rule: rule name: 1    new rule string: "((age >+ 40 AND department = 'HR') OR (salary > 50000))"
   5. delete_rule: rule name
   6. get_all_rules

**Key Features**

1. Automated Rule Evaluation: Processes incoming data based on predefined rules.
2. Rule Management GUI: User-friendly interface for managing and testing rules.
3. Integration with Databases: Supports database operations for storing and retrieving data.
4. JSON Response Handling: Processes JSON responses for rule evaluation.
