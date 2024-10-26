frappe.ui.form.on('Cards', {
    file_type: function(frm) {
        // Clear the sourced_by field
        frm.set_value('sourced_by', '');

        // Set the query for sourced_by based on file_type
        if (frm.doc.file_type === 'Team') {
            frm.set_query('sourced_by', function() {
                return {
                    filters: {
                        'status': 'Active'
                    },
                    doctype: 'Employee'
                };
            });
        } else if (frm.doc.file_type === 'Vendor') {
            frm.set_query('sourced_by', function() {
                return {
                    filters: {
                        'status': 'Active'
                    },
                    doctype: 'Vendor'
                };
            });
        } else if (frm.doc.file_type === 'Campaign') {
            frm.set_query('sourced_by', function() {
                return {
                    filters: {
                        'status': 'Active'
                    },
                    doctype: 'Campaign'
                };
            });
        } else {
            frm.set_query('sourced_by', null); // Clear query if no valid file_type
        }
    }
});
