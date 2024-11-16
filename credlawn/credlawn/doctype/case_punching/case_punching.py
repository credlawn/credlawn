import frappe
from frappe.model.document import Document
import re
from frappe.utils import nowdate

class CasePunching(Document):
    def validate(self):

        reference_pattern = r"^24[a-zA-Z]\d{2}[a-zA-Z]\d{8}[a-zA-Z0-9]{2}$"
        mobile_pattern = r"^\d{10}$"
        

        if not self.reference_no:
            frappe.throw("Reference No. is missing. Please enter a Reference No.")
        elif not re.match(reference_pattern, self.reference_no):
            frappe.throw("Invalid Reference No. Please try again.")
        

        if not self.mobile_no:
            frappe.throw("Mobile Number is missing. Please enter a Mobile No.")
        elif not re.match(mobile_pattern, self.mobile_no):
            frappe.throw("Mobile Number must be 10 digits.")
        

        if self.reference_no:

            self.reference_no = str(self.reference_no).upper().strip()

            self.name = self.reference_no 


        if self.customer_name:
            self.customer_name = self.customer_name.title().strip()

    def after_insert(self):
        self.update_employee_name()

    def on_update(self):
        self.update_employee_name()
        self.reload()

    def update_employee_name(self):
        employee = frappe.get_doc("Employee", self.employee)
        if employee:
            frappe.db.set_value("Case Punching", self.name, "employee_name", employee.employee_name)

        if not self.punching_date:
            frappe.db.set_value("Case Punching", self.name, "punching_date", nowdate())
