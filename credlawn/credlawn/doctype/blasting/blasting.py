from frappe import _
from frappe.model.document import Document

class Blasting(Document):
    def validate(self):
        if self.login_status in ["Denied", "Duplicate", "Approved", "Rejected"]:
            self.lead_status = "Closed"
        elif self.login_status in ["IP Approved", "CNR", "Follow up", "SVKYC", "Cure Pending"]:
            self.lead_status = "Team"
        elif self.login_status in ["VKYC", "BKYC", "Risk", "Cure Done"]:
            self.lead_status = "Bank"
        
        # New validation for app_status
        if self.login_status in ["VKYC", "SVKYC", "BKYC", "Risk", "Cure Done", "Approved"]:
            self.app_status = "Complete"
