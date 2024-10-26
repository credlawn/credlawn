import frappe
from frappe.model.document import Document
from frappe import throw, _
from frappe.utils import getdate, today, flt
from frappe.utils import nowdate
from frappe.model.meta import get_meta


class Card(Document):

  def validate(self):
    if self.pan_no:
      # Check length
      if len(self.pan_no) != 10:
        frappe.throw(_("PAN number must be 10 digits"))

      # Check format (using regular expressions)
      import re
      pattern = r"^[A-Za-z]{5}\d{4}[A-Za-z]$"
      if not re.match(pattern, self.pan_no):
        frappe.throw(_("PAN number must be in format XXXXX****X (X is alphabet, * is number)"))

      # Check for existing PAN number
      message = self.check_pan(self.pan_no)  # Call check_pan function
      if message:
        frappe.throw(message)  # Throw an exception if customer already exists

  def before_save(self):
    # Modify customer_name, pan_no and city before saving
    self.customer_name = self.customer_name.title().strip()
    self.pan_no = self.pan_no.upper().strip()
    self.city = self.city.title().strip()

  def check_pan(self, pan_no):
    """Checks if a PAN number already exists in the Card doctype.

    Args:
      pan_no (str): The PAN number entered in the form.

    Returns:
      str: A message indicating whether the PAN number exists or not.
    """

    filters = {
      "pan_no": pan_no
    }
    existing_customer = frappe.get_list("Card", filters=filters)

    if existing_customer:
      message = f"Customer already exists."
    else:
      message = "You can process this customer."

    return message
