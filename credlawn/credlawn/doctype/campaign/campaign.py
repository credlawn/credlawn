import frappe
from frappe.model.document import Document
from frappe import _

class Campaign(Document):
    def after_insert(self):
        records = frappe.get_all('Database', filters={'data_type': self.data_type, 'data_source': self.data_source}, fields=['name', 'customer_name', 'mobile_no', 'data_source'])
        
        if not records:
            frappe.throw(_("No Data Available to Create Campaign"))

        frappe.enqueue('credlawn.credlawn.doctype.campaign.campaign.insert_campaign_data', 
            campaign_name=self.name, 
            volume=self.volume, 
            data_type=self.data_type, 
            data_source=self.data_source,  
            campaign_date=self.campaign_date, 
            campaign_type=self.campaign_type, 
            login_link=self.login_link, 
            queue="default", timeout=3000, 
            is_async=True)

    def on_trash(self):
        frappe.db.sql("""
            DELETE FROM `tabCampaigndata`
            WHERE parent = %s
        """, self.name)

def insert_campaign_data(campaign_name, volume, data_type, data_source, campaign_date, campaign_type, login_link):
    records = frappe.get_all('Database', filters={'data_type': data_type, 'data_source': data_source}, fields=['name', 'customer_name', 'mobile_no', 'data_source'])
    
    records_to_insert = records[:volume]
    successful_inserts = 0

    for record in records_to_insert:
        try:
            new_campaign_data = frappe.new_doc('Campaigndata')
            latest_idx = frappe.db.get_value('Campaigndata', filters={}, fieldname='MAX(idx)')
            new_campaign_data.idx = (latest_idx or 0) + 1
            new_campaign_data.customer_name = record.customer_name
            new_campaign_data.mobile_no = '91' + str(record.mobile_no).lstrip('0')
            new_campaign_data.mob_no = record.mobile_no
            new_campaign_data.data_source = record.data_source
            new_campaign_data.parent = campaign_name
            new_campaign_data.campaign_date = campaign_date
            new_campaign_data.login_link = login_link
            new_campaign_data.campaign_type = campaign_type
            new_campaign_data.parentfield = 'campaign_data'
            new_campaign_data.parenttype = 'Campaign'
            new_campaign_data.insert(ignore_permissions=True)

            successful_inserts += 1
        except Exception:
            pass

    frappe.db.set_value('Campaign', campaign_name, 'vol1', successful_inserts)

    frappe.db.commit()

    
