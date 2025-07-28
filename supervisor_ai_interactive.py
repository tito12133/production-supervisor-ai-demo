import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import textwrap

class ProductionSupervisorAIInteractive:
    def __init__(self, root):
        self.root = root
        self.root.title("Production Supervisor AI – Interactive Demo")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        self.team = ["Operator A", "Operator B", "Inspector C", "Assembler D"]
        self.tasks_completed = []
        self.safety_logs = []
        self.scenarios = self._load_scenarios()

        self._setup_styles()
        self._build_ui()
        self._log("Welcome to Production Supervisor AI Interactive Demo\n")

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 11), padding=8)
        style.configure('TLabel', font=('Segoe UI', 11))
        style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'))
        style.configure('TFrame', padding=10)
        style.configure('Log.TLabel', font=('Consolas', 10))

    def _build_ui(self):
        # Header label
        header = ttk.Label(self.root, text="Production Supervisor AI – Interactive Demo", style='Header.TLabel')
        header.pack(pady=10)

        # Frame for task input and assignment
        task_frame = ttk.LabelFrame(self.root, text="Assign Custom Task to Operator")
        task_frame.pack(fill='x', padx=15, pady=5)

        ttk.Label(task_frame, text="Select Operator:").grid(row=0, column=0, sticky='w', padx=5, pady=6)
        self.operator_var = tk.StringVar(value=self.team[0])
        operator_menu = ttk.Combobox(task_frame, textvariable=self.operator_var, values=self.team, state="readonly", width=18)
        operator_menu.grid(row=0, column=1, sticky='w', padx=5, pady=6)

        ttk.Label(task_frame, text="Enter Task Description:").grid(row=1, column=0, sticky='nw', padx=5, pady=6)
        self.task_text = tk.Text(task_frame, height=3, width=60, wrap='word')
        self.task_text.grid(row=1, column=1, sticky='w', padx=5, pady=6)

        assign_btn = ttk.Button(task_frame, text="Assign Task", command=self.assign_custom_task)
        assign_btn.grid(row=2, column=1, sticky='e', padx=5, pady=6)

        # Frame for controls
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill='x', padx=15, pady=5)

        ttk.Button(control_frame, text="Review Random Scenario", command=self.review_scenario).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Give Safety Briefing", command=self.safety_briefing).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Evaluate AI Output", command=self.evaluate_ai_output).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Show Completed Tasks", command=self.show_tasks).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Clear Log", command=self.clear_log).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Exit", command=self.root.quit).pack(side='right', padx=5)

        # Scrollable log area
        self.log_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Consolas", 11))
        self.log_area.pack(expand=True, fill='both', padx=15, pady=10)
        self.log_area.configure(state='disabled')

    def _log(self, text):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, text + "\n\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')

    def _load_scenarios(self):
        return [
            {
                "title": "Operator Misses Quality Check",
                "details": "An operator failed to log a quality inspection during a 12-hour shift.",
                "expected_actions": [
                    "Investigate root cause of missed QC",
                    "Reinforce importance of Quality Control with operator",
                    "Update operator training record",
                    "Log corrective action in system"
                ]
            },
            {
                "title": "Machine Downtime",
                "details": "Fabrication machine offline for 45 minutes, delaying 50 parts.",
                "expected_actions": [
                    "Notify maintenance team immediately",
                    "Reassign idle operators to other tasks",
                    "Update production schedule to accommodate delay",
                    "Log downtime reason for future analysis"
                ]
            },
            {
                "title": "Safety Near-Miss",
                "details": "An assembler bypassed a guard on a press, nearly causing injury.",
                "expected_actions": [
                    "Immediately stop work in affected area",
                    "File a safety incident report",
                    "Retrain employee on safety protocols",
                    "Reinforce lockout-tagout procedures"
                ]
            }
        ]

    def assign_custom_task(self):
        operator = self.operator_var.get()
        task = self.task_text.get("1.0", tk.END).strip()
        if not task:
            messagebox.showwarning("Input Required", "Please enter a task description before assigning.")
            return
        assignment = f"Task Assigned: {operator} — {task}"
        self.tasks_completed.append((operator, task))
        self._log(assignment)
        self.task_text.delete("1.0", tk.END)

    def review_scenario(self):
        scenario = random.choice(self.scenarios)
        self._log(f"--- Scenario: {scenario['title']} ---")
        self._log(textwrap.fill(scenario['details'], width=80))
        response = self._prompt_text("Scenario Response", "Describe your corrective actions:")
        if response is not None:
            self._log(f"Your response: {response}")
        self._log("Recommended Best Practice Actions:")
        for step in scenario['expected_actions']:
            self._log(f" - {step}")

    def safety_briefing(self):
        tips = [
            "Always enforce PPE (gloves, goggles, ear protection).",
            "Ensure machine guards are never bypassed.",
            "Document all incidents, including near-misses.",
            "Rotate staff regularly to avoid fatigue on long shifts."
        ]
        tip = random.choice(tips)
        self.safety_logs.append(tip)
        self._log(f"Safety Briefing Tip: {tip}")

    def evaluate_ai_output(self):
        sample_output = "Operator A: Assemble 100 units in 2 hours without QC verification."
        self._log("AI-Generated Workflow Sample:")
        self._log(f"  {sample_output}")
        decision = self._prompt_text("AI Output Evaluation", "Is this acceptable? Why or why not?")
        if decision is not None:
            self._log(f"Your evaluation: {decision}")
        guidance = (
            "Supervisor Guidance:\n"
            "This is NOT acceptable — QC verification cannot be skipped. "
            "Feedback must highlight regulatory and safety requirements."
        )
        self._log(guidance)

    def show_tasks(self):
        if not self.tasks_completed:
            self._log("No tasks have been assigned/completed yet.")
            return
        self._log("Completed Tasks:")
        for op, task in self.tasks_completed:
            self._log(f" - {op}: {task}")

    def clear_log(self):
        self.log_area.configure(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.configure(state='disabled')
        self._log("Log cleared.")

    def _prompt_text(self, title, prompt):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("600x200")
        dialog.grab_set()
        dialog.resizable(False, False)

        ttk.Label(dialog, text=prompt, font=("Segoe UI", 11)).pack(pady=8, padx=10, anchor='w')

        text_box = tk.Text(dialog, height=6, width=70, wrap='word')
        text_box.pack(padx=10)

        response_var = {'value': None}

        def submit():
            response = text_box.get("1.0", tk.END).strip()
            if not response:
                messagebox.showwarning("Input Required", "Please enter a response before submitting.")
                return
            response_var['value'] = response
            dialog.destroy()

        submit_btn = ttk.Button(dialog, text="Submit", command=submit)
        submit_btn.pack(pady=10)

        dialog.wait_window()
        return response_var['value']

def main():
    root = tk.Tk()
    app = ProductionSupervisorAIInteractive(root)
    root.mainloop()

if __name__ == "__main__":
    main()
