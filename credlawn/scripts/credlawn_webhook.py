import frappe
from frappe.utils import now_datetime
import json

@frappe.whitelist(allow_guest=True)
def handle_webhook():
    
    data = frappe.local.form_dict 



    if isinstance(data, str):
        data = json.loads(data) 

    if "cmd" in data:
        del data["cmd"]
        
    headers = dict(frappe.local.request.headers)

    webhook_response = frappe.new_doc('Webhook Response')
    webhook_response.sender_headers = json.dumps(headers)
    webhook_response.response_data = json.dumps(data)  
    webhook_response.status_code = 200  
    webhook_response.timestamp = now_datetime() 
    webhook_response.insert(ignore_permissions=True)  

    return {
        "status": "success",
        "message": "Webhook data received Successfully."
    }
