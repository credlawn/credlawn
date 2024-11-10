from frappe.model.document import Document
import frappe

class Campaigndata(Document):
    def autoname(self):
        self.name = self.generate_campaign_code()

    def generate_campaign_code(self):
        existing_codes = self.get_existing_codes()
        next_code = self.get_next_code(existing_codes)
        return next_code

    def get_existing_codes(self):
        return [campaign.name for campaign in frappe.get_all('Campaigndata', fields=['name'])]

    def get_next_code(self, existing_codes):
        if not existing_codes:
            return "aaaaa"
        return self.increment_code(max(existing_codes))

    def increment_code(self, code):
        if code == "zzzzz":
            return "aaaaa"
        code_list = list(code)
        for i in reversed(range(len(code_list))):
            if code_list[i] == 'z':
                code_list[i] = 'a'
            else:
                code_list[i] = chr(ord(code_list[i]) + 1)
                return ''.join(code_list)
        return ''.join(code_list)


    def after_insert(self):
        self.bank_link = self.get_bank_link(self.login_link)
        self.source = self.name
        self.save()
        self.compare_mobile_number()
        self.update_database_dates_and_platforms()
        self.create_website_route_redirect()

    def get_bank_link(self, login_link):
        bank_links = frappe.get_all('Bank Links', filters={'name': login_link}, fields=['full_link'])
        if bank_links:
            return bank_links[0].get('full_link').replace("{}", self.name)
        else:
            return ''

    def compare_mobile_number(self):
        frappe.get_all('Database', filters={'mobile_no': self.mob_no}, fields=['name'])

    def update_database_dates_and_platforms(self):
        database_records = frappe.get_all('Database', filters={'mobile_no': self.mob_no}, fields=['name'])
        if not database_records:
            return
        database_doc = frappe.get_doc('Database', database_records[0]['name'])
        for i in range(1, 11):
            date_field = f"date_{i}"
            if not getattr(database_doc, date_field) and self.campaign_date:
                setattr(database_doc, date_field, self.campaign_date)
                break
        for i in range(1, 11):
            platform_field = f"platform_{i}"
            if not getattr(database_doc, platform_field) and self.campaign_type:
                setattr(database_doc, platform_field, self.campaign_type)
                break
        setattr(database_doc, "data_type", 'Recent')
        database_doc.save()

    def create_website_route_redirect(self):
        new_redirect = frappe.new_doc('Website Route Redirect')
        latest_idx = frappe.db.get_value('Website Route Redirect', filters={}, fieldname='MAX(idx)')
        new_redirect.idx = (latest_idx or 0) + 1
        new_redirect.source = self.name
        new_redirect.target = self.bank_link
        new_redirect.redirect_http_status = 301
        new_redirect.parent = 'Website Settings'
        new_redirect.parentfield = 'route_redirects'
        new_redirect.parenttype = 'Website Settings'
        new_redirect.insert()
        frappe.db.commit()