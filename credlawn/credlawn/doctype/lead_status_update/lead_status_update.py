import frappe
from frappe.model.document import Document
import re

class LeadStatusUpdate(Document):
    def validate(self):

        if self.reference_no:
            reference_pattern = r"^24[a-zA-Z]\d{2}[a-zA-Z]\d{8}[a-zA-Z0-9]{2}$"
            if not re.match(reference_pattern, self.reference_no):
                frappe.throw("Invalid Reference No. Please try again.")
            self.reference_no = str(self.reference_no).upper().strip()


        if not self.source and not self.mobile_no:
            frappe.throw("Please enter 'Source' or 'Mobile No'")
        

        if self.source:
            self.source = str(self.source).strip() 

            self.source = self.source.lower() 
            if not re.match(r'^[a-z]{5}$', self.source):  
                frappe.throw("Please enter correct Source Code.")


        if self.mobile_no:
            self.mobile_no = str(self.mobile_no).strip()
            if not re.match(r'^\d{10}$', self.mobile_no):
                frappe.throw("Mobile No is not Correct.")

    def after_insert(self):
        self.update_agent_number()

    def on_update(self):
        self.update_agent_number()
        self.reload()

    def update_agent_number(self):
        if self.source:
            blasting = frappe.get_all('Blasting', filters={'name': self.source}, fields=['agent_number'])
            if blasting:
                agent_number = blasting[0].get('agent_number')
                if agent_number:
                    frappe.db.set_value('Lead Status Update', self.name, 'agent_number', agent_number)
                    frappe.db.commit()

        elif self.mobile_no:
            blasting = frappe.get_all('Blasting', filters={'mobile_no': self.mobile_no}, fields=['agent_number'])
            if blasting:
                agent_number = blasting[0].get('agent_number')
                if agent_number:
                    frappe.db.set_value('Lead Status Update', self.name, 'agent_number', agent_number)
                    frappe.db.commit()
