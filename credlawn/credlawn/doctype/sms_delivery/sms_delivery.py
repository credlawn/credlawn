import frappe
from frappe.model.document import Document
import json

class SMSDelivery(Document):
    def after_insert(self):
        if self.sender_headers:
            try:
                headers = json.loads(self.sender_headers)
                webhook_type = headers.get('Webhook-Type')
                if webhook_type:
                    self.webhook_type = webhook_type
                    self.save(ignore_permissions=True)
            except json.JSONDecodeError:
                pass
            except Exception:
                pass

        if self.response_data:
            try:
                response_data_str = self.response_data.strip()

                response_data = json.loads(response_data_str)

                data_str = response_data.get('data')
                if data_str:
                    try:
                        data = json.loads(data_str)
                    except json.JSONDecodeError:
                        return

                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                for report in item.get("report", []):
                                    if isinstance(report, dict):
                                        request_id = item.get("requestId")
                                        mobile_no = report.get("number")
                                        amount = report.get("amount")
                                        timestamp = report.get("date")
                                        delivery_status = report.get("desc")
                                        failed_reason = report.get("failedReason")

                                        self.request_id = request_id
                                        self.mobile_no = mobile_no
                                        self.amount = amount
                                        self.timestamp = timestamp
                                        self.delivery_status = delivery_status
                                        self.failed_reason = failed_reason

                        self.save(ignore_permissions=True)

            except json.JSONDecodeError:
                return
            except Exception as e:
                frappe.log_error(frappe.get_traceback(), f"Error in SMSDelivery after_insert: {str(e)}")


        self.update_sms_status_to_campaign()

    def update_sms_status_to_campaign(self):

        if not self.mobile_no or not self.delivery_status:
            return


        campaign_data = frappe.get_all('Campaigndata', filters={'mobile_no': self.mobile_no, 'campaign_type': "SMS"}, fields=['name'])

        if campaign_data:

            for record in campaign_data:
                campaign_doc = frappe.get_doc('Campaigndata', record['name'])
                campaign_doc.message_status = self.delivery_status
                campaign_doc.save(ignore_permissions=True)
                frappe.db.commit() 
