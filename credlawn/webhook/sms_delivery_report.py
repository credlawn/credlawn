import frappe
from frappe.utils import now_datetime
import json

@frappe.whitelist(allow_guest=True)
def get_sms_delivery_report():
    
    data = frappe.local.form_dict 



    if isinstance(data, str):
        data = json.loads(data) 

    if "cmd" in data:
        del data["cmd"]
        
    headers = dict(frappe.local.request.headers)

    frappe.enqueue(method=process_sms_delivery, queue="default", timeout=300, is_async=True, headers=headers, data=data)


    return {
        "status": "success",
        "message": "Data Received."
    }

def process_sms_delivery(headers, data):

    sms_delivery = frappe.new_doc('SMS Delivery')
    sms_delivery.sender_headers = json.dumps(headers)
    sms_delivery.response_data = json.dumps(data)  
    sms_delivery.status_code = 200   
    sms_delivery.insert(ignore_permissions=True)

    frappe.db.commit()  


