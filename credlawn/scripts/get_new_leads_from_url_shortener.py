import requests
import frappe
import json

@frappe.whitelist()
def fetch_and_process_urls():
    frappe.enqueue(fetch_and_process_urls_background)

def fetch_and_process_urls_background():
    # Define headers
    tokens = ['Bearer KzskfjrAngfmbmpS', 'Bearer bTQRwBUpxAGYzvyf']  
    headers_template = {
        'Content-Type': 'application/json'
    }
    
    for token in tokens:
        headers = headers_template.copy() 
        headers['Authorization'] = token  

        response = requests.get('https://cipl.me/api/urls?limit=50000&order=date', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Step 2: Filter URLs with clicks > 0
            valid_urls = [url for url in data['data']['urls'] if url['clicks'] > 0]
            
            # Step 3: Process each valid URL
            for url in valid_urls:
                url_id = url['id']
                
                # Check if a Visitor record with the given url_id exists
                existing_doc = frappe.get_all("Visitor", filters={"url_id": url_id}, limit=1)
                
                if not existing_doc:
                    # If it doesn't exist, create a new Visitor record
                    visitor_doc = frappe.get_doc({
                        "doctype": "Visitor",
                        "url_id": url_id,
                        "short_url": url['shorturl'],
                        "long_url": url['longurl'],
                        "title": url['title'],
                        "clicks": url['clicks'],
                        "unique_clicks": url['uniqueclicks'],
                        "date": url['date'],
                        "alias": url['alias']
                    })
                    visitor_doc.insert() 

    frappe.db.commit()
