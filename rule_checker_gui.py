import tkinter as tk
from tkinter import messagebox
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

class RuleEngineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rule Engine GUI")

        # Create a main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        # Create Rule
        self.create_rule_frame = tk.Frame(self.main_frame)
        self.create_rule_frame.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.create_rule_frame, text="Create Rule Name").pack()
        self.rule_name_entry = tk.Entry(self.create_rule_frame, width=50)
        self.rule_name_entry.pack()
        tk.Label(self.create_rule_frame, text=" Create Rule (e.g., ((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing'))").pack()
        self.rule_string_entry = tk.Entry(self.create_rule_frame, width=50)
        self.rule_string_entry.pack()
        self.create_rule_button = tk.Button(self.create_rule_frame, text="Create Rule", command=self.create_rule)
        self.create_rule_button.pack()

        # Combine Rules
        self.combine_rule_frame = tk.Frame(self.main_frame)
        self.combine_rule_frame.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.combine_rule_frame, text="Combine Rules (comma-separated IDs)").pack()
        self.rule_ids_entry = tk.Entry(self.combine_rule_frame, width=50)
        self.rule_ids_entry.pack()
        tk.Label(self.combine_rule_frame, text="Combined Rule Name").pack()
        self.combined_rule_name_entry = tk.Entry(self.combine_rule_frame, width=50)
        self.combined_rule_name_entry.pack()
        self.combine_rule_button = tk.Button(self.combine_rule_frame, text="Combine Rules", command=self.combine_rules)
        self.combine_rule_button.pack()

        # Evaluate Rule
        self.evaluate_rule_frame = tk.Frame(self.main_frame)
        self.evaluate_rule_frame.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.evaluate_rule_frame, text="Select Rule ID to Evaluate").pack()
        self.rule_id_entry = tk.Entry(self.evaluate_rule_frame, width=50)
        self.rule_id_entry.pack()
        tk.Label(self.evaluate_rule_frame, text="Data (JSON)").pack()
        self.data_entry = tk.Entry(self.evaluate_rule_frame, width=50)
        self.data_entry.pack()
        self.evaluate_rule_button = tk.Button(self.evaluate_rule_frame, text="Evaluate Rule", command=self.evaluate_rule)
        self.evaluate_rule_button.pack()

        # Modify Rule
        self.modify_rule_frame = tk.Frame(self.main_frame)
        self.modify_rule_frame.grid(row=3, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.modify_rule_frame, text="Modify Rule ID").pack()
        self.modify_rule_id_entry = tk.Entry(self.modify_rule_frame, width=50)
        self.modify_rule_id_entry.pack()
        tk.Label(self.modify_rule_frame, text="New Rule String").pack()
        self.new_rule_string_entry = tk.Entry(self.modify_rule_frame, width=50)
        self.new_rule_string_entry.pack()
        self.modify_rule_button = tk.Button(self.modify_rule_frame, text="Modify Rule", command=self.modify_rule)
        self.modify_rule_button.pack()

        # Delete Rule
        self.delete_rule_frame = tk.Frame(self.main_frame)
        self.delete_rule_frame.grid(row=4, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.delete_rule_frame, text="Delete Rule (Rule Name)").pack()
        self.delete_rule_name_entry = tk.Entry(self.delete_rule_frame, width=50)
        self.delete_rule_name_entry.pack()
        self.delete_rule_button = tk.Button(self.delete_rule_frame, text="Delete Rule", command=self.delete_rule)
        self.delete_rule_button.pack()

        # Get All Rules
        self.get_all_rules_button = tk.Button(self.main_frame, text="Get All Rules", command=self.get_all_rules)
        self.get_all_rules_button.grid(row=5, column=0, padx=10, pady=5, sticky='w')

        # Output
        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky='nsew')
        self.output_text = tk.Text(self.output_frame, height=20, width=60)
        self.output_text.pack()

        # Configure grid to allow resizing
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def create_rule(self):
        rule_string = self.rule_string_entry.get()
        rule_name = self.rule_name_entry.get()
        try:
            response = requests.post(f"{BASE_URL}/create_rule", json={
                "rule": rule_string,
                "rule_name": rule_name
            })
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Create Rule Response: {response.json()}\n")
            # Optionally clear inputs
            self.rule_name_entry.delete(0, tk.END)
            self.rule_string_entry.delete(0, tk.END)
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def combine_rules(self):
        rule_ids = self.rule_ids_entry.get().split(',')
        rule_ids = [id.strip() for id in rule_ids]
        combined_rule_name = self.combined_rule_name_entry.get()
        if not combined_rule_name:
            self.output_text.insert(tk.END, "Error: Combined rule name is required.\n")
            return
        try:
            response = requests.post(f"{BASE_URL}/combine_rules", json={
                "rules": rule_ids,
                "combined_rule_name": combined_rule_name
            })
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Combine Rules Response: {response.json()}\n")
            # Optionally clear inputs
            self.rule_ids_entry.delete(0, tk.END)
            self.combined_rule_name_entry.delete(0, tk.END)
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def evaluate_rule(self):
        rule_name = self.rule_name_entry.get()  # Use the correct entry for rule ID
        data_json = self.data_entry.get()   # Get JSON data from data entry

        try:
            # Parse the JSON data
            data = json.loads(data_json)  # This may raise JSONDecodeError

            # Ensure the necessary keys exist
            if 'age' not in data or 'income' not in data:
                self.output_text.insert(tk.END, "Error: Missing 'age' or 'income' in data.\n")
                return
        
            # Convert rule_id to integer and validate
            rule_name = int(rule_name)

            # Send the rule_id and data to the evaluation endpoint
            response = requests.post(f"{BASE_URL}/evaluate_rule", json={
                "rule_name": rule_name,
                "data": data
            })
    
            response.raise_for_status()  # Raise an error for bad responses
            self.output_text.insert(tk.END, f"Evaluate Rule Response: {response.json()}\n")

        except ValueError as e:
            self.output_text.insert(tk.END, f"Invalid input: {e}\n")
        except json.JSONDecodeError:
            self.output_text.insert(tk.END, "Invalid JSON format. Please check your input.\n")
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def modify_rule(self):
        rule_name = self.modify_rule_id_entry.get()
        new_rule_string = self.new_rule_string_entry.get()
        try:
            response = requests.put(f"{BASE_URL}/modify_rule", json={"rule_name": rule_name, "new_rule": new_rule_string})
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Modify Rule Response: {response.json()}\n")
            # Optionally clear inputs
            self.modify_rule_id_entry.delete(0, tk.END)
            self.new_rule_string_entry.delete(0, tk.END)
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def delete_rule(self):
        rule_name = self.delete_rule_name_entry.get()
        try:
            response = requests.delete(f"{BASE_URL}/delete_rule", json={"rule_name": rule_name})
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Delete Rule Response: {response.json()}\n")
            # Optionally clear input
            self.delete_rule_name_entry.delete(0, tk.END)
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def get_all_rules(self):
        try:
            response = requests.get(f"{BASE_URL}/get_all_rules")
            response.raise_for_status()
            rules = response.json().get("rules", [])
            rules_text = "\n".join(rules) if rules else "No rules found."
            self.output_text.insert(tk.END, f"Get All Rules Response:\n{rules_text}\n")
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = RuleEngineApp(root)
    root.mainloop()
