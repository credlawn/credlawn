import frappe
from frappe.utils import getdate, today, date_diff

def update_all_employee_age_and_tenure():
    # Fetch all Employee records
    employees = frappe.get_all("Employee", fields=["name", "date_of_birth", "joining_date", "last_working_date"])

    for employee_data in employees:
        employee = frappe.get_doc("Employee", employee_data.name)
        update_employee_fields(employee)

def update_employee_fields(employee):
    # Fetch necessary fields
    date_of_birth = employee.date_of_birth
    joining_date = employee.joining_date
    last_working_date = employee.last_working_date or today()

    # Update age field
    if date_of_birth:
        age_years, age_months, age_days = calculate_age(getdate(date_of_birth))
        employee.age = f"{age_years} Years {age_months} Months"
    
    # Update tenure field
    if last_working_date and joining_date:
        tenure_months, tenure_days = calculate_tenure(getdate(joining_date), getdate(last_working_date))
    else:
        tenure_months, tenure_days = calculate_tenure(getdate(joining_date), getdate(today()))
    
    employee.tenure = f"{tenure_months} Months {tenure_days} Days"

    # Save changes to the employee document
    employee.save()

def calculate_age(dob):
    today_date = getdate(today())
    years = today_date.year - dob.year
    months = today_date.month - dob.month
    days = today_date.day - dob.day

    if days < 0:
        months -= 1
        days += (dob.replace(year=dob.year + 1, month=1, day=1) - dob.replace(year=dob.year, month=dob.month, day=1)).days

    if months < 0:
        years -= 1
        months += 12

    return years, months, days

def calculate_tenure(joining_date, end_date):
    total_days = date_diff(end_date, joining_date)
    months = total_days // 30
    days = total_days % 30
    return months, days

# Schedule this function to run periodically
@frappe.whitelist()
def scheduled_employee_update():
    update_all_employee_age_and_tenure()
