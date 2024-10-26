import requests
import frappe

@frappe.whitelist()
def fetch_visitor_record():
    frappe.enqueue(fetch_visitor_record_background)

def fetch_visitor_record_background():
    # Define headers
    tokens = ['Bearer KzskfjrAngfmbmpS', 'Bearer bTQRwBUpxAGYzvyf']  
    headers_template = {
        'Content-Type': 'application/json'
    }
    
    # Fetch all url_ids from the Visitor doctype
    visitor_records = frappe.get_all("Visitor", fields=["url_id"])

    # Iterate over each visitor record
    for record in visitor_records:
        url_id = record['url_id']
        data_found = False  # Flag to track if data was found

        # Try each token for the current url_id
        for token in tokens:
            headers = headers_template.copy() 
            headers['Authorization'] = token  

            detail_response = requests.get(f'https://cipl.me/api/url/{url_id}', headers=headers)
            
            if detail_response.status_code == 200:
                detail_data = detail_response.json()

                # Check if there is an error in the response
                if 'error' in detail_data and detail_data['error'] != 0:
                    continue  # Continue to the next token
                
                # Proceed to update the visitor record
                update_visitor_record(url_id, detail_data['data'])
                data_found = True  # Mark that data was found
                break  # Exit the token loop since we found data

        # If no data was found with both tokens, you can handle it here if needed

    frappe.db.commit() 

def update_visitor_record(url_id, url_data):
    # Check if a Visitor record with the given url_id exists
    existing_doc = frappe.get_all("Visitor", filters={"url_id": url_id}, limit=1)
    
    if existing_doc:
        # If it exists, fetch the existing document
        visitor_doc = frappe.get_doc("Visitor", existing_doc[0]['name'])

        # Track whether any fields have changed
        is_updated = False

        # Get clicks and unique_clicks from the response
        clicks = int(url_data['clicks'])
        unique_clicks = int(url_data['uniqueClicks'])

        # Update clicks and unique_clicks if they differ
        if visitor_doc.clicks != clicks:
            visitor_doc.clicks = clicks
            is_updated = True  # Mark as updated

        if visitor_doc.unique_clicks != unique_clicks:
            visitor_doc.unique_clicks = unique_clicks
            is_updated = True  # Mark as updated

        # Update alias if it is NULL or None
        if not visitor_doc.alias:
            visitor_doc.alias = url_data.get('alias')
            is_updated = True  # Mark as updated

        # Update browser if it is NULL or None
        if not visitor_doc.browser:
            top_browser = next(iter(url_data['topBrowsers'].keys()), None)
            if top_browser:
                visitor_doc.browser = top_browser
                is_updated = True  # Mark as updated

        # Update OS if it is NULL or None
        if not visitor_doc.os:
            top_os = next(iter(url_data['topOs'].keys()), None)
            if top_os:
                visitor_doc.os = top_os
                is_updated = True  # Mark as updated

        # Save the updated document if any changes were made
        if is_updated:
            visitor_doc.save()
