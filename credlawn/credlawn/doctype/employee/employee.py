import frappe
from frappe.model.document import Document
from datetime import datetime

class Employee(Document):
    def after_insert(self):
        self.calculate_age()

    def on_update(self):
        self.calculate_age()
        self.refresh()

    def calculate_age(self):
        if self.date_of_birth:
            dob = datetime.strptime(self.date_of_birth, "%Y-%m-%d")
            today = datetime.today()

            age_years = today.year - dob.year
            age_months = today.month - dob.month

            if age_months < 0 or (age_months == 0 and today.day < dob.day):
                age_years -= 1
                age_months += 12

            self.age = f"{age_years} Years {age_months} Months"
            frappe.db.set_value('Employee', self.name, 'age', self.age)

            frappe.db.commit()
            frappe.msgprint("Employee Saved Successfully.")

    def refresh(self):
        self.reload()
