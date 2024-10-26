import frappe
import requests

@frappe.whitelist()
def send_lead():
    # Fetch records where lead_assigned is No
    records = frappe.get_all('Blasting', filters={'lead_assigned': 'No'}, fields=['name', 'customer_name', 'mobile_no', 'link'])
    
    for record in records:
        customer_name = record.customer_name
        mobile_no = record.mobile_no
        link = record.link

        # Prepare your message data
        data = {
            "messaging_product": "whatsapp",
            "to": "919685399388",
            "type": "template",
            "template": {
                "name": "new_lead",
                "language": {
                    "code": "en"
                },
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "text",
                                "text": customer_name
                            }
                        ]
                    },
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": customer_name
                            },
                            {
                                "type": "text",
                                "text": mobile_no
                            },
                            {
                                "type": "text",
                                "text": f"https://cipl.me/{link}"
                            }
                        ]
                    }
                ]
            }
        }

        # Send the request
        response = requests.post(
            'https://graph.facebook.com/v20.0/455614377625850/messages',
            headers={
                'Authorization': 'Bearer EAAO0SXjh39MBO8AORVhdilmZA6lZBDrwNZAUQwaf3GdaSeV58awZATPuDTU0QNoTR2BXr5OM8ZCjE1hmdSM4F4tuVkvQwqyc10zN6ZCGvKuVZBqEfYZBxqZCvtCCn0rTXrurRxI4s2KcZAOAcPFTZAeZBIeTG1Cx91PV81WwV9hpcWNNaDfPyDfsgPfcRbfN7zMYazNQQwZDZD',
                'Content-Type': 'application/json'
            },
            json=data
        )

        # Check response status
        if response.status_code == 200:
            # Update lead_assigned to Yes
            frappe.db.set_value('Blasting', record.name, 'lead_assigned', 'Yes')
        else:
            frappe.log_error(f"Failed to send message: {response.status_code} - {response.text}", "WhatsApp Message Error")
    
    # Optionally, you can log a success message or return something
