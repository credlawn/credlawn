import frappe
from frappe.model.document import Document
import re

class CasePunching(Document):
    def validate(self):
        reference_pattern = r"^24[A-Z]\d{2}[A-Z]\d{8}[A-Z0-9]{2}$"
        mobile_pattern = r"^\d{10}$"
        
        if self.reference_no:
            if not re.match(reference_pattern, self.reference_no):
                frappe.throw("Invalid Reference No. Please try Again")
        else:
            frappe.throw("Reference is Missing. Please enter Reference No.")
        
        if self.mobile_no:
            if not re.match(mobile_pattern, self.mobile_no):
                frappe.throw("Mobile Number must be 10 digits.")
        else:
            frappe.throw("Mobile Number is Missing. Please enter Mobile No.")

    def after_insert(self):

        if self.reference_no:
            self.reference_no = self.reference_no.upper().strip()

        if self.customer_name:
            self.customer_name = self.customer_name.title().strip()
