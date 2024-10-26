import string
import frappe
from frappe.model.document import Document

class LoginLink(Document):
    def before_insert(self):
        self.lc2_code = self.lc2_code or self.get_next_code(self.get_last_code())
        self.validate_mobile_no()
        self.customer_name = self.clean_customer_name()
        self.update_bank_link()
        first_part = self.customer_name.split()[0] if self.customer_name else ''
        self.metatitle = f"{first_part}- {self.data_source}- {self.mobile_no}"
        self.short_url = f"https://cipl.me/{self.lc2_code}"

    def after_insert(self):
        self.update_number_status()

    def before_save(self):
        self.update_number_status()

    def get_last_code(self):
        return frappe.db.get_value('Login Link', {}, 'lc2_code', order_by='creation desc') or 'aaaaa'

    def get_next_code(self, current_code):
        code_list = list(current_code)
        for i in reversed(range(len(code_list))):
            if code_list[i] != 'z':
                code_list[i] = string.ascii_lowercase[string.ascii_lowercase.index(code_list[i]) + 1]
                return ''.join(code_list)
            code_list[i] = 'a'
        return ''.join(code_list)

    def update_bank_link(self):
        link_details = frappe.db.get_value('Bank Links', {'link_code': self.link_type}, 
                                             ['linkpart1', 'linkpart2', 'linkpart3'], as_dict=True)
        self.bank_link = (f"{link_details.linkpart1}{self.lc1_code}{link_details.linkpart2}{self.lc2_code}{link_details.linkpart3}"
                          if link_details else '')

    def validate_mobile_no(self):
        if not (self.mobile_no and len(self.mobile_no) == 10 and self.mobile_no.isdigit()):
            frappe.throw("Mobile number must be 10 digits long.")

    def clean_customer_name(self):
        return ' '.join(self.customer_name.title().split())

    def update_number_status(self):
        if self.campaign_date:
            frappe.db.set_value('Login Link', self.name, 'number_status', "Used")
            self.reload()

def bulk_insert_login_links(login_links_data):
    batch_size = 100
    for i in range(0, len(login_links_data), batch_size):
        batch = login_links_data[i:i + batch_size]
        frappe.get_doc(batch).insert(ignore_permissions=True)
