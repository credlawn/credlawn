import requests
import frappe
import time

def get_access_token():
    access_token_record = frappe.get_doc('Access Tokens', 'msg91')
    access_token = access_token_record.get_password("access_token")
    return access_token if access_token else None


def create_recipient_data(record, campaign_doc):
    recipient_data = {
        "mobiles": record.mobile_no
    }
    # Dynamically add the variable name-value pairs
    for var_name, var_value in [
        (record.var_1_name, record.var_1_value),
        (record.var_2_name, record.var_2_value),
        (record.var_3_name, record.var_3_value),
        (record.var_4_name, record.var_4_value),
    ]:
        if var_name and var_value:
            recipient_data[var_name] = var_value
    return recipient_data

# Main function to send SMS
@frappe.whitelist()
def send_sms(campaign_name):
    # Fetch the Campaigndata records based on campaign_name (parent)
    camp_data_records = frappe.get_all('Campaigndata', filters={'parent': campaign_name}, fields=[
        'name', 'template_id', 'mobile_no', 'var_1_name', 'var_1_value', 'var_2_name', 'var_2_value',
        'var_3_name', 'var_3_value', 'var_4_name', 'var_4_value', 'campaign_date'
    ])

    if not camp_data_records:
        return "failure"

    campaign_doc = frappe.get_doc('Campaign', campaign_name)

    # Fetch the access token
    access_token = get_access_token()
    if not access_token:
        return "failure"

    url = "https://control.msg91.com/api/v5/flow"
    headers = {
        'accept': 'application/json',
        'authkey': access_token,
        'content-type': 'application/json'
    }

    batch_size = 60
    recipient_batch = []
    for i, record_data in enumerate(camp_data_records):
        try:
            # Fetch the full document for the current Campaigndata record using its 'name'
            record = frappe.get_doc('Campaigndata', record_data.name)

            if not record:
                continue  

            recipient_data = create_recipient_data(record, campaign_doc)

            recipient_batch.append(recipient_data)

            if len(recipient_batch) == batch_size or i == len(camp_data_records) - 1:
                data = {
                    "template_id": record_data.template_id,
                    "short_url": "0",  # Static value
                    "realTimeResponse": "1",  # Static value
                    "recipients": recipient_batch
                }

                response = requests.post(url, headers=headers, json=data)

                recipient_batch = []

                if len(recipient_batch) == 0: 
                    time.sleep(1)  

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Error while sending SMS")

    return "success"
