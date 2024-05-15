import tkinter as tk
from tkinter import messagebox, simpledialog
from MyClasses import Calculation
import numpy as np

class FormApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Analytic Hierarchy Process')
        self.geometry('600x400')
        self.n = simpledialog.askinteger("Input", "Enter the number of criteria (3-8):", minvalue=3, maxvalue=8)

        self.entries = []
        for i in range(self.n**2):
            entry = tk.Entry(self, width=10)
            entry.grid(row=i // self.n, column=i % self.n)
            self.entries.append(entry)

        calculate_btn = tk.Button(self, text="Hesapla", command=self.calculate)
        calculate_btn.grid(row=self.n + 1, column=0, columnspan=self.n)

    def calculate(self):
        try:
            values = [float(entry.get()) for entry in self.entries]
            criteria_matrix = np.array(values).reshape((self.n, self.n))
            average_criteria = Calculation.calc_average(criteria_matrix, self.n)

            CR = Calculation.consistency_vector(criteria_matrix, average_criteria)
            message = f"Consistency Ratio: {CR:.4f}\n"
            if CR < 0.10:
                message += "The matrix is consistent."
            else:
                message += "The matrix is not consistent, please revise it."
            messagebox.showinfo("Results", message)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = FormApp()
    app.mainloop()
