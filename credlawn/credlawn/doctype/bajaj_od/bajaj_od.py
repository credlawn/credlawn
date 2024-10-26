import frappe
from frappe.model.document import Document

class BajajOD(Document):
    def before_insert(self):
        self.calculate_commission_amount()
    
    def after_insert(self):
        self.after_insert_calculation()

    def on_update(self):
        self.calculate_commission_amount()
        self.after_insert_calculation()

    def calculate_commission_amount(self):
        if not self.loan_amount or not self.commission_percentage:
            frappe.throw("Please fill in Loan Amount & Commission Percentage.")
        self.commission_amount = self.loan_amount * self.commission_percentage / 100 - self.pf_deduction

    def after_insert_calculation(self):
        self.amount_receivable = self.commission_amount - self.commission_amount * 0.02
        self.gst_amount = self.commission_amount * 0.18
        self.total_amount = self.commission_amount + self.commission_amount * 0.18
        self.tds_amount = self.commission_amount * 0.05
        self.net_amount = self.commission_amount + self.commission_amount * 0.18 - self.commission_amount * 0.05
        self.balance_amount = self.net_amount - self.vendor_paid
        self.balance_amount_without_gst = self.commission_amount - self.tds_amount - self.vendor_paid
        self.net_vendor_payout = (
            (self.loan_amount * self.vendor_percentage / 100) -
            (self.loan_amount * self.vendor_percentage / 100) * (self.tds / 100) -
            (self.pf_deduction)
        ) if self.vendor_percentage and self.vendor_percentage > 0 else 0
        self.net_profit = self.amount_receivable + self.gst_amount - self.vendor_paid - self.balance_amount_without_gst
        self.vendor_amount = (self.loan_amount * self.vendor_percentage / 100) - self.pf_deduction if self.vendor_percentage and self.vendor_percentage > 0 else 0