import frappe
from frappe.model.document import Document
import json

class WebhookResponse(Document):
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
