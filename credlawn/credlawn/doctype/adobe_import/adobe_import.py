import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class AdobeImport(Document):
    def after_insert(self):
        self.update_fields()

    def on_update(self):
        self.update_fields()

    def update_fields(self):
        # Update decision_date
        day = self.get_final_decision_day()
        self.decision_date = self.creation_date if day is None else self.construct_date(day)
        frappe.db.set_value(self.doctype, self.name, 'decision_date', self.decision_date)

        # Update duplicate_finder
        duplicate_finder_value = f"{self.customer_name.replace(' ', '').strip()}{self.city.replace(' ', '').strip()}{self.pin_code.strip()}"
        frappe.db.set_value(self.doctype, self.name, 'duplicate_finder', duplicate_finder_value)

    def get_final_decision_day(self):
        if self.final_decision_date:
            try:
                day = int(self.final_decision_date)
                if 1 <= day <= 31:
                    return day
            except ValueError:
                frappe.throw("final_decision_date must be a valid integer.")
        return None

    def construct_date(self, day):
        current_year, current_month = getdate(nowdate()).year, getdate(nowdate()).month
        return f"{current_year}-{current_month:02d}-{day:02d}"
