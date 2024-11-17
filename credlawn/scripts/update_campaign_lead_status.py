import frappe
import time

@frappe.whitelist()
def update_status():
    lead_status_updates = frappe.db.sql("""
        SELECT name, source, lead_status, creation, reference_no 
        FROM `tabLead Status Update`
    """, as_dict=True)

    for record in lead_status_updates:
        blasting = frappe.db.sql("""
            SELECT name, lead_status, reference_no
            FROM `tabBlasting`
            WHERE name = %s
        """, (record['source']), as_dict=True)

        if blasting:
            blasting_doc = blasting[0]
            
            if blasting_doc['lead_status'] == "IP Approved":
                continue

            status_update_date = record['creation'].date()

            update_needed = False

            if blasting_doc['lead_status'] != record['lead_status']:
                update_needed = True
                frappe.db.sql("""
                    UPDATE `tabBlasting`
                    SET lead_status = %s
                    WHERE name = %s
                """, (record['lead_status'], blasting_doc['name']))

            if blasting_doc['reference_no'] != record['reference_no'] and record['reference_no']:
                update_needed = True
                frappe.db.sql("""
                    UPDATE `tabBlasting`
                    SET reference_no = %s
                    WHERE name = %s
                """, (record['reference_no'], blasting_doc['name']))

            if update_needed:
                frappe.db.sql("""
                    UPDATE `tabBlasting`
                    SET status_update_date = %s
                    WHERE name = %s
                """, (status_update_date, blasting_doc['name']))
                
            frappe.db.commit()

        time.sleep(0.1)

@frappe.whitelist()
def enqueue_update_status():
    frappe.enqueue(update_status, queue='long')
