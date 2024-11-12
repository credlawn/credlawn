import frappe
import time
import requests

@frappe.whitelist()
def send_lead(blasting_name):
    # Adding a small delay (100ms)
    time.sleep(0.1)  # 100ms delay

    # Fetch the updated Blasting document
    blasting_doc = frappe.get_doc('Blasting', blasting_name)
    
    # Now send the WhatsApp message
    send_whatsapp_message(blasting_doc)

def send_whatsapp_message(blasting_doc):
    # Get the relevant fields from the Blasting document
    customer_name = blasting_doc.customer_name
    mobile_no = blasting_doc.mobile_no
    link = "https://cipl.me/" + blasting_doc.link
    whatsapp_account = blasting_doc.whatsapp_account
    agent_number = blasting_doc.agent_number

    # Fetch the corresponding Credlawn Whatsapp record
    credlawn_record = frappe.get_doc('Credlawn Whatsapp', whatsapp_account)
    phone_no_id = credlawn_record.phone_no_id
    access_token = credlawn_record.get_password("access_token")
    template_name = credlawn_record.template_name

    # Prepare the message data
    data = {
        "messaging_product": "whatsapp",
        "to": agent_number,  # Recipient (agent number)
        "type": "template",
        "template": {
            "name": template_name,
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
                            "text": link
                        }
                    ]
                }
            ]
        }
    }

    # Send the WhatsApp message using the appropriate API
    response = requests.post(
        f'https://graph.facebook.com/v20.0/{phone_no_id}/messages',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json=data
    )

    # Check if the message was sent successfully
    if response.status_code == 200:
        # If successful, update the Blasting document to indicate the lead has been assigned
        frappe.db.set_value('Blasting', blasting_doc.name, 'lead_assigned', 'Yes')
