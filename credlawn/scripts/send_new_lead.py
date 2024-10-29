import frappe
import requests

@frappe.whitelist()
def send_lead():
    # Fetch records where lead_assigned is No
    records = frappe.get_all('Blasting', filters={'lead_assigned': 'No'}, fields=['name', 'customer_name', 'mobile_no', 'link', 'whatsapp_account', 'agent_number'])
    
    for record in records:
        customer_name = record.customer_name
        mobile_no = record.mobile_no
        link = record.link
        whatsapp_account = record.whatsapp_account
        agent_number = record.agent_number  # Fetch agent_number

        # Fetch the corresponding Credlawn Whatsapp record
        credlawn_record = frappe.get_doc('Credlawn Whatsapp', whatsapp_account)
        phone_no_id = credlawn_record.phone_no_id
        access_token = credlawn_record.get_password("access_token")  # Correctly use get_password to retrieve the token
        template_name = credlawn_record.template_name  # Fetch template_name

        # Prepare your message data
        data = {
            "messaging_product": "whatsapp",
            "to": agent_number,  # Use agent_number as the recipient
            "type": "template",
            "template": {
                "name": template_name,  # Use dynamic template_name
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
                            }
                        ]
                    }
                ]
            }
        }

        # Send the request using dynamic phone_no_id and access_token
        response = requests.post(
            f'https://graph.facebook.com/v20.0/{phone_no_id}/messages',  # Use dynamic phone_no_id
            headers={
                'Authorization': f'Bearer {access_token}',  # Use dynamic access_token
                'Content-Type': 'application/json'
            },
            json=data
        )

        # Check response status
        if response.status_code == 200:
            # Update lead_assigned to Yes
            frappe.db.set_value('Blasting', record.name, 'lead_assigned', 'Yes')
