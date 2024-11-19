import frappe
from frappe.model.document import Document

def update_adobe_database_records():
    adobe_records = frappe.get_all('Adobe', fields=['name', 'reference_no', 'customer_name', 'creation_date', 'customer_type', 
                                                    'sm_code', 'product_code', 'promo_code', 'lc1_code', 'company_name', 
                                                    'dropoff_reason', 'idcom_status', 'vkyc_status', 'ipa_status', 
                                                    'current_status', 'city', 'state', 'pin_code', 'surrogate_eligibility', 
                                                    'decline_code', 'final_decision', 'etb_nb_succ_flag', 'curable_flag', 
                                                    'decline_description', 'channel', 'kyc_type', 'vkyc_expire_date', 
                                                    'vkyc_link', 'dap_final_flag', 'lc2_code', 'lg_code', 'restart_flag', 
                                                    'qde_status', 'company_code', 'dsa_code', 'inprocess_classification', 
                                                    'classification', 'decline_type', 'bkyc_status', 'bkyc_status_reason', 
                                                    'login_month', 'decision_month', 'duplicate_finder', 'file_type', 
                                                    'adobe_decision_date', 'final_decision_date', 'decision_date'])

    for adobe in adobe_records:
        reference_no = adobe['reference_no']

        try:
            existing_record = frappe.db.get_value('Adobe Database', {'reference_no': reference_no}, ['name', 'decision_date'])

            update_data = {}
            change_log = []

            decision_date = adobe.get('decision_date')
            final_decision_date = adobe.get('final_decision_date')

            change_log.append('<ul style="list-style-type: none; padding: 0; margin: 0;">')

            for field in ['promo_code', 'decline_description', 'decline_code', 'bkyc_status', 'product_code', 
                          'bkyc_status_reason', 'vkyc_link', 'vkyc_expire_date', 'vkyc_status', 'kyc_type', 
                          'dap_final_flag', 'qde_status', 'dropoff_reason', 'current_status', 'customer_name', 
                          'creation_date', 'customer_type', 'sm_code', 'lc1_code', 'company_name', 'idcom_status', 
                          'ipa_status', 'city', 'state', 'pin_code', 'surrogate_eligibility', 'final_decision', 
                          'etb_nb_succ_flag', 'curable_flag', 'channel', 'lc2_code', 'lg_code', 'restart_flag', 
                          'company_code', 'dsa_code', 'inprocess_classification', 'classification', 'decline_type', 
                          'login_month', 'decision_month', 'duplicate_finder', 'file_type', 'adobe_decision_date', 
                          'final_decision_date']:
                value = adobe.get(field)
                if value:
                    if existing_record:
                        old_value = frappe.db.get_value('Adobe Database', existing_record, field)
                        if old_value != value:
                            field_name = field.replace('_', ' ').title()
                            change_log.append(f'<li style="margin: 5px 0;"><b>{field_name}:</b> <span style="color:green; padding-left: 10px;">{old_value}</span> <span style="color:red;">--> {value}</span></li>')
                            update_data[field] = value
                    else:
                        field_name = field.replace('_', ' ').title()
                        change_log.append(f'<li style="margin: 5px 0;"><b>{field_name}:</b> {value}</li>')
                        update_data[field] = value

            change_log.append('</ul>')

            if final_decision_date:
                formatted_date = final_decision_date.strftime('%d-%m-%Y')
                change_log.append('<br><b>Decision Date:</b> <span style="color:blue;">' + formatted_date + '</span>')

            if existing_record:
                if change_log:
                    frappe.db.set_value('Adobe Database', existing_record, 'change_log', "".join(change_log))
                    frappe.db.set_value('Adobe Database', existing_record, update_data)

            else:
                # Only add to change_log for new records if there's initial data to log
                if change_log:
                    new_data = {"reference_no": adobe.get('reference_no')}
                    new_data.update(update_data)

                    doc = frappe.get_doc({
                        "doctype": "Adobe Database",
                        **new_data
                    })

                    doc.insert()

        except Exception as e:
            frappe.log_error(message=str(e), title=f"Error syncing record {reference_no}")
            continue
