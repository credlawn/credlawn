import frappe
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

    def after_insert(self):
        campaign_data = frappe.db.get_value("Campaigndata", self.name, ["campaign_type", "campaign_date", "customer_name", "mob_no", "data_source"], as_dict=True)

        if campaign_data:
            # Assign values from the Campaign Data to the Blasting document
            self.campaign_type = campaign_data.campaign_type
            self.campaign_date = campaign_data.campaign_date
            self.customer_name = campaign_data.customer_name
            self.mobile_no = campaign_data.mob_no
            self.data_source = campaign_data.data_source
            click_fields = ['click_1', 'click_2', 'click_3', 'click_4', 'click_5', 'click_6', 'click_7', 'click_8']
            for i, click_field in enumerate(click_fields):
                if not getattr(self, click_field):
                    setattr(self, click_field, self.cr_date)
                    break

            self.save(ignore_permissions=True)
            frappe.enqueue('credlawn.scripts.send_lead.send_lead', blasting_name=self.name)
        else:
            return
