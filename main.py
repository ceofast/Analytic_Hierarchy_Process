import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from MyClasses import Calculation
from tkinter import messagebox, simpledialog, ttk

class FormApp(tk.Tk):
    def __init__(self):
        """
        Initialize the main application window and its components.
        """
        super().__init__()
        self.title('Analytic Hierarchy Process')
        self.geometry('800x600')

        # Dropdown for selecting the weighting method
        self.method_label = tk.Label(self, text="Select Weighting Method:")
        self.method_label.grid(row=0, column=0, padx=10, pady=5)

        self.method_var = tk.StringVar(value="AHP")
        self.method_dropdown = ttk.Combobox(self, textvariable=self.method_var)
        self.method_dropdown['values'] = ("AHP", "Logarithmic Regression")
        self.method_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Number of criteria input
        self.n = simpledialog.askinteger("Input", "Enter the number of criteria (3-8):", minvalue=3, maxvalue=8)

        # Dynamic entry fields for criteria matrix
        self.entries = []
        for i in range(self.n ** 2):
            entry = tk.Entry(self, width=10)
            entry.grid(row=(i // self.n) + 1, column=i % self.n, padx=5, pady=5)
            self.entries.append(entry)

        # Calculate button
        calculate_btn = tk.Button(self, text="Calculate", command=self.calculate)
        calculate_btn.grid(row=self.n + 2, column=0, columnspan=self.n, pady=20)

        # Plot buttons
        bar_chart_btn = tk.Button(self, text="Show Bar Chart", command=self.show_bar_chart)
        bar_chart_btn.grid(row=self.n + 3, column=0, pady=10)

        pie_chart_btn = tk.Button(self, text="Show Pie Chart", command=self.show_pie_chart)
        pie_chart_btn.grid(row=self.n + 3, column=1, pady=10)

        # Scenario buttons
        save_scenario_btn = tk.Button(self, text="Save Scenario", command=self.save_scenario)
        save_scenario_btn.grid(row=self.n + 3, column=2, pady=10)

        load_scenario_btn = tk.Button(self, text="Load Scenario", command=self.load_scenario)
        load_scenario_btn.grid(row=self.n + 3, column=3, pady=10)

        compare_scenarios_btn = tk.Button(self, text="Compare Scenarios", command=self.compare_scenarios)
        compare_scenarios_btn.grid(row=self.n + 3, column=4, pady=10)

        # Result label
        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=self.n + 4, column=0, columnspan=self.n, pady=10)

        self.criteria_matrix = None
        self.average_criteria = None
        self.scenarios = {}

    def calculate(self):
        """
        Gather input from the entries, process the AHP calculations, and display the results.
        Handles errors by showing appropriate messages.
        """
        try:
            values = [float(entry.get()) for entry in self.entries]
            self.criteria_matrix = np.array(values).reshape((self.n, self.n))
            method = self.method_var.get()

            if method == "AHP":
                self.average_criteria = Calculation.calc_average(self.criteria_matrix, self.n)
            elif method == "Logarithmic Regression":
                self.average_criteria = Calculation.logarithmic_regression(self.criteria_matrix, self.n)

            CR = Calculation.consistency_vector(self.criteria_matrix, self.average_criteria)
            message = f"Consistency Ratio: {CR:.4f}\n"
            if CR < 0.10:
                message += "The matrix is consistent."
            else:
                message += "The matrix is not consistent, please revise it."
            self.result_label.config(text=message)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_bar_chart(self):
        """
        Display a bar chart of the priority vector.
        """
        if self.average_criteria is not None:
            plt.figure()
            plt.bar(range(self.n), self.average_criteria, tick_label=[f'Criterion {i+1}' for i in range(self.n)])
            plt.xlabel('Criteria')
            plt.ylabel('Weight')
            plt.title('Priority Vector')
            plt.show()
        else:
            messagebox.showwarning("Warning", "Please calculate the priorities first.")

    def show_pie_chart(self):
        """
                Display a pie chart of the priority vector.
        """
        if self.average_criteria is not None:
            plt.figure()
            plt.pie(self.average_criteria, labels=[f"Criterion {i+1}" for i in range(self.n)], autopct='%1.1f%%')
            plt.title('Priority Distribution')
            plt.show()
        else:
            messagebox.showwarning("Warning", "Please calculate the priorities first.")

    def save_scenario(self):
        """
        Save the current scenario with a unique name provided by the user.
        """
        if self.criteria_matrix is not None and self.average_criteria is not None:
            scenario_name = simpledialog.askstring("Input", "Enter a name for the scenario: ")
            if scenario_name:
                self.screnarios[scenario_name] = {
                    'criteria_matrix': self.criteria_matrix,
                    'average_criteria': self.average_criteria
                }
                messagebox.showinfo("Success", f"Scenario '{scenario_name}' saved succesfully.")
        else:
            messagebox.showwarning("Warning", "Please calculate the priorities first.")


    def load_scenario(self):
        """
        Load a saved scenario by selecting from the list of saved scenarios.
        """
        if self.scenarios:
            scenario_name = simpledialog.askstring("Input", "Enter the name of the scenario to load:")
            if scenario_name in self.scenarios:
                scenario = self.scenarios[scenario_name]
                self.criteria_matrix = scenario['criteria_matrix']
                self.average_criteria = scenario['average_criteria']
                messagebox.showinfo("Success", f"Scenario '{scenario_name}' loaded successfully.")
                # Update the entry fields with the loaded scenario
                for i in range(self.n ** 2):
                    self.entries[i].delete(0, tk.END)
                    self.entries[i].insert(0, str(self.criteria_matrix.flatten()[i]))
            else:
                messagebox.showerror("Error", f"Scenario '{scenario_name}' not found.")
        else:
            messagebox.showwarning("Warning", "No scenarios saved yet.")

    def compare_scenarios(self):
        """
        Compare multiple scenarios and display the results.
        """
        if len(self.scenarios) > 1:
            scenario_names = list(self.scenarios.keys())
            comparison_data = {name: self.scenarios[name]['average_criteria'] for name in scenario_names}

            plt.figure()
            for name, data in comparison_data.items():
                plt.plot(range(self.n), data, marker='o', label=name)

            plt.xlabel('Criteria')
            plt.ylabel('Weight')
            plt.title('Scenario Comparison')
            plt.legend()
            plt.show()
        else:
            messagebox.showwarning("Warning", "Please save at least two scenarios to compare.")

if __name__ == "__main__":
    app = FormApp()
    app.mainloop()
