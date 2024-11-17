import frappe

@frappe.whitelist()
def update_file_type():
    # Get all records from the Adobe doctype
    records = frappe.get_all('Adobe', fields=['name', 'duplicate_finder', 'dap_final_flag', 'promo_code'])

    # Set default file_type to "Not Set" for all records initially
    for record in records:
        frappe.db.set_value('Adobe', record['name'], 'file_type', 'Not Set')

    # Group records by duplicate_finder
    grouped_records = {}
    for record in records:
        df_value = record['duplicate_finder']
        if df_value not in grouped_records:
            grouped_records[df_value] = []
        grouped_records[df_value].append(record)

    # Iterate through each group of duplicate_finder
    for df_value, group in grouped_records.items():
        new_entry_found = False
        
        # First Check: Both fields are not None
        for record in group:
            if record['dap_final_flag'] is not None and record['promo_code'] is not None:
                frappe.db.set_value('Adobe', record['name'], 'file_type', 'New')
                new_entry_found = True
                # Mark all others as Duplicate
                for r in group:
                    if r['name'] != record['name']:
                        frappe.db.set_value('Adobe', r['name'], 'file_type', 'Duplicate')
                break  # Exit after finding the first valid record

        if not new_entry_found:
            # Second Check: Either field is not None
            for record in group:
                if record['dap_final_flag'] is not None or record['promo_code'] is not None:
                    frappe.db.set_value('Adobe', record['name'], 'file_type', 'New')
                    new_entry_found = True
                    # Mark all others as Duplicate
                    for r in group:
                        if r['name'] != record['name']:
                            frappe.db.set_value('Adobe', r['name'], 'file_type', 'Duplicate')
                    break  # Exit after finding the first valid record

        if not new_entry_found:
            # Final Check: Both fields are None
            frappe.db.set_value('Adobe', group[0]['name'], 'file_type', 'New')  # Set the first as New
            for r in group[1:]:
                frappe.db.set_value('Adobe', r['name'], 'file_type', 'Duplicate')

    frappe.msgprint("File types updated successfully.")
