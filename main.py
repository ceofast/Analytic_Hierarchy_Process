import numpy as np
import tkinter as tk
from tkinter import messagebox
from MyClasses import Calculation

class FormApp(tk.Tk):
    def __init__(self):
        """
        Initializes the main window of the application, setting up the UI components including entry fields and calculation button.
        """
        super().__init__()
        self.title('Analytic Hierarchy Process')
        self.geometry('600x400')

        # Create entry widgets dynamically and arrange them in a grid
        self.entries = [tk.Entry(self, width=10) for _ in range(52)]
        for idx, entry in enumerate(self.entries):
            row = idx // 10
            col = idx % 10
            entry.grid(row=row, column=col)

        # Calculation button initialization and placement
        calculate_btn = tk.Button(self, text="Calculate", command=self.calculate)
        calculate_btn.grid(row=6, column=0)

    def calculate(self):
        """
        Gathers user input from the entry fields, performs calculations to determine the AHP priorities and consistency index,
        and displays the results in a message box. Handles errors in user input with an error message.
        """
        try:
            # Extract and convert input values from entry fields
            values = [float(entry.get()) for entry in self.entries]
            c1 = np.array(values[0:9]).reshape((3, 3))
            c2 = np.array(values[9:18]).reshape((3, 3))
            c3 = np.array(values[18:27]).reshape((3, 3))
            c4 = np.array(values[27:36]).reshape((3, 3))
            all_criteria = np.array(values[36:52]).reshape((4, 4))

            # Calculate averages and consistency
            average1 = Calculation.calc_average(c1, 3)
            average2 = Calculation.calc_average(c2, 3)
            average3 = Calculation.calc_average(c3, 3)
            average4 = Calculation.calc_average(c4, 3)
            average_criteria = Calculation.calc_average(all_criteria, 4)

            mux_arr = Calculation.mux_array(average1, average2, average3, average4, average_criteria)
            m_inconsistency_index = Calculation.consistency_vector(all_criteria, average_criteria)

            # Display results
            messagebox.showinfo("Results", f"Consistency Index: {m_inconsistency_index}\nMux Values: {mux_arr}")

        except ValueError:
            # Handle invalid input
            messagebox.showerror("Error", "Please fill all fields with valid numbers")

if __name__ == "__main__":
    app = FormApp()
    app.mainloop()
