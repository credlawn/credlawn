import frappe
from frappe.model.document import Document

class Database(Document):
    def before_insert(self):
        if self.customer_name: self.customer_name = self.customer_name.title().strip()
        if self.email: self.email = self.email.lower().strip()
        if self.city: self.city = self.city.title().strip()
        if self.company_name: self.company_name = self.company_name.title().strip()
        if self.mobile_no:
            self.mobile_no = ''.join(filter(str.isdigit, self.mobile_no))
            if len(self.mobile_no) != 10:
                frappe.throw("Mobile number must be 10 digits.")
