import frappe

def create_route_redirects():
    login_links = frappe.get_all('Login Link', filters={'url_status': 'Test'}, fields=['name', 'bank_link'])

    for link in login_links:
        new_redirect = frappe.new_doc('Website Route Redirect')
        latest_idx = frappe.db.get_value('Website Route Redirect', filters={}, fieldname='MAX(idx)')
        new_redirect.idx = (latest_idx or 0) + 1
        new_redirect.source = link.name
        new_redirect.target = link.bank_link
        new_redirect.redirect_http_status = 301
        new_redirect.parent = 'Website Settings'
        new_redirect.parentfield = 'route_redirects'
        new_redirect.parenttype = 'Website Settings'
        new_redirect.insert()

        frappe.db.set_value('Login Link', link.name, 'url_status', 'Approved')

    frappe.db.commit()
