import frappe
from frappe.model.document import Document

class Adobe(Document):

    def after_insert(self):
        # Get the reference of the Adobe Dump document that corresponds to the name
        adobe_dump_record = frappe.get_all('Adobe Dump', filters={'name': self.name}, fields=['name', 'reference_no', 'customer_name', 'city', 'creation_date', 'changed_value'])

        if not adobe_dump_record:
            # If the record does not exist in Adobe Dump, create a new record
            new_adobe_dump = frappe.get_doc({
                'doctype': 'Adobe Dump',
                'name': self.name,
                'reference_no': self.reference_no,
                'customer_name': self.customer_name,
                'city': self.city,
                'creation_date': self.creation_date
            })
            new_adobe_dump.insert(ignore_permissions=True)
            frappe.db.commit()
        else:
            # If the record exists, compare the fields and update if necessary
            adobe_dump_record = frappe.get_doc('Adobe Dump', adobe_dump_record[0]['name'])
            changes = []
            updated_fields = []

            # Compare fields and track changes
            if self.reference_no != adobe_dump_record.reference_no:
                changes.append(f'reference_no- {adobe_dump_record.reference_no} --> {self.reference_no}')
                updated_fields.append('reference_no')
            
            if self.customer_name != adobe_dump_record.customer_name:
                changes.append(f'customer_name- {adobe_dump_record.customer_name} --> {self.customer_name}')
                updated_fields.append('customer_name')

            if self.city != adobe_dump_record.city:
                changes.append(f'city- {adobe_dump_record.city} --> {self.city}')
                updated_fields.append('city')

            # Compare creation_date carefully (handle datetime format issues)
            if self.creation_date != adobe_dump_record.creation_date:
                changes.append(f'creation_date- {adobe_dump_record.creation_date} --> {self.creation_date}')
                updated_fields.append('creation_date')

            # Only update if there are any actual changes
            if changes:
                # Update Adobe Dump fields
                adobe_dump_record.update({
                    'reference_no': self.reference_no,
                    'customer_name': self.customer_name,
                    'city': self.city,
                    'creation_date': self.creation_date
                })

                # Append changes to the 'changed_value' field
                if adobe_dump_record.changed_value:
                    adobe_dump_record.changed_value += '\n' + '\n'.join(changes)
                else:
                    adobe_dump_record.changed_value = '\n'.join(changes)

                # Save changes in Adobe Dump
                adobe_dump_record.save(ignore_permissions=True)
                frappe.db.commit()
