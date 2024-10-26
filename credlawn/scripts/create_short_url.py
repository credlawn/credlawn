from __future__ import unicode_literals
import frappe
import requests
import json

@frappe.whitelist()
def run_post_request():
    frappe.enqueue(run_post_request_background)

def run_post_request_background():
    # Fetch records from Login Link where url_status is Pending
    pending_links = frappe.get_all('Login Link', filters={'url_status': 'Test'}, fields=['name', 'bank_link', 'lc2_code', 'metatitle'])
    
    for link in pending_links:
        url = 'https://cipl.me/api/url/add'
        headers = {
            'Authorization': 'Bearer bTQRwBUpxAGYzvyf',
            'Content-Type': 'application/json'
        }
        data = {
            "url": link.bank_link,
            "status": "private",
            "custom": link.lc2_code,
            "expiry": "",  # Expiry date
            "type": "direct",  # Type
            "metatitle": link.metatitle,
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            frappe.log("Success: " + response.text)
            # Update the url_status to Approved
            frappe.db.set_value('Login Link', link.name, 'url_status', 'Approved')
        else:
            frappe.log("Error: " + response.text)

