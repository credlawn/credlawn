frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        set_readonly_fields(frm);
    },
    onload: function(frm) {
        set_readonly_fields(frm);
    }
});

function set_readonly_fields(frm) {
    const fields_to_check = ['employee_name', 'joining_date', 'date_of_birth', 'gender', 'department',
                                'designation', 'grade', 'branch', 'mobile_no', 'email', 'fixed_salary',
                                'account_no', 'ifsc_code', 'employment_status', 'last_working_date', 'reason_for_leaving'
                            ];
    
    fields_to_check.forEach(field => {
        if (frm.doc[field] && !frm.doc.__islocal) {
            frm.set_df_property(field, 'read_only', 1);
        }
    });
}
