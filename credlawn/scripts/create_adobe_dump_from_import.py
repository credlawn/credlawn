import frappe
from datetime import datetime, timedelta

@frappe.whitelist()
def create_adobe_dump_records():
    approved_records = frappe.get_all(
        'Adobe Import',
        filters={
            'ipa_status': 'APPROVE',
            'file_type': 'New'
        },
        fields=['reference_no']
    )

    created_count = 0

    for record in approved_records:
        if created_count >= 50:
            break

        reference_no = record.reference_no
        adobe_dump_exists = frappe.db.exists('Adobe Dump', {'reference_no': reference_no})

        if not adobe_dump_exists:
            adobe_import_data = frappe.get_all(
                'Adobe Import',
                filters={'reference_no': reference_no},
                fields=[
                    'customer_name', 'creation_date', 'customer_type', 'reference_no', 'city', 'promo_code',
                    'lc1_code', 'lc2_code', 'decision_date', 'decline_description', 'decline_code', 
                    'bkyc_status', 'bkyc_status_reason', 'sm_code', 'company_name', 'product_code', 
                    'vkyc_link', 'vkyc_expiry_date', 'vkyc_status', 'kyc_type_adobe', 
                    'dap_final_flag', 'qde_status', 'dropoff_reason', 'current_status'  # Added current_status
                ]
            )

            for data in adobe_import_data:
                if created_count >= 50:
                    break

                # Convert vkyc_expiry_date from Excel format to datetime
                vkyc_expiry_date = None
                if data.vkyc_expiry_date:
                    try:
                        excel_epoch = datetime(1899, 12, 30)
                        vkyc_expiry_date = excel_epoch + timedelta(days=float(data.vkyc_expiry_date))
                    except (ValueError, TypeError):
                        frappe.msgprint(f'Invalid vkyc_expiry_date for reference {reference_no}: {data.vkyc_expiry_date}')
                        continue

                # Determine vkyc_status
                vkyc_status = None
                if data.vkyc_status == 'SUCCESS':
                    vkyc_status = 'Success'
                elif data.vkyc_status == 'FAILED':
                    vkyc_status = 'Failed'
                elif data.kyc_type_adobe in ['bioinperson', 'bioKYC']:
                    vkyc_status = 'Biometric'

                # Prepare the new record
                new_record_data = {
                    'doctype': 'Adobe Dump',
                    'customer_name': data.customer_name,
                    'creation_date': data.creation_date,
                    'customer_type': data.customer_type,
                    'reference_no': data.reference_no,
                    'city': data.city,
                    'promo_code': data.promo_code,
                    'lc1_code': data.lc1_code,
                    'lc2_code': data.lc2_code,
                    'decision_date': data.decision_date,
                    'decline_code': data.decline_code,
                    'decline_description': data.decline_description,
                    'bkyc_status': data.bkyc_status,
                    'bkyc_status_reason': data.bkyc_status_reason,
                    'sm_code': data.sm_code,
                    'company_name': data.company_name,
                    'product_code': data.product_code,
                    'vkyc_link': data.vkyc_link,
                    'vkyc_expiry_date': vkyc_expiry_date,
                }

                # Only add fields if conditions are met
                if vkyc_status is not None:
                    new_record_data['vkyc_status'] = vkyc_status
                
                # Update dap_final_flag
                if data.dap_final_flag == 'Yes':
                    new_record_data['dap_final_flag'] = 'Yes'
                
                # Update qde_status
                if data.qde_status == 'Ok':
                    new_record_data['qde_status'] = 'Ok'
                
                # Update dropoff_reason based on conditions
                if data.dropoff_reason in ['IN-COMPLETED APPLICATION', 'IDCOM DROPOFF']:
                    new_record_data['dropoff_reason'] = 'Incomplete'
                elif data.dropoff_reason in ['ADDRESS CHANGED', 'ADDRESS CHANGED AND IDCO']:
                    new_record_data['dropoff_reason'] = 'Address Change'
                
                # Update current_status based on conditions
                if data.current_status == 'Approved Case':
                    new_record_data['current_status'] = 'Approved'
                elif data.current_status in ['CKYCChecker', 'Risk', 'PRE-CPV', 'RCC', 'SendToECPV', 'Underwriter', 'DP']:
                    new_record_data['current_status'] = 'Bank Pending'
                elif data.current_status == 'Indexing':
                    new_record_data['current_status'] = 'KYC Pending'
                elif data.current_status in ['DAP Final', 'Decline Dump']:
                    new_record_data['current_status'] = 'Team Pending'

                new_record = frappe.get_doc(new_record_data)
                new_record.insert()
                created_count += 1
                frappe.msgprint(f'Created Adobe Dump record for {reference_no}')

    if created_count == 0:
        frappe.msgprint('No new records created. Either all already exist or no matching records found.')
    else:
        frappe.msgprint(f'Total {created_count} Adobe Dump records created.')
