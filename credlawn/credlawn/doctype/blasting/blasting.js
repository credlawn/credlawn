frappe.ui.form.on('Blasting', {
    onload: function(frm) {

        $(frm.wrapper).find('.help-box.small.text-muted').hide();
        
        if (!frm.is_new()) {
            
            const fields = ['campaign_date', 'cr_date', 'lead_type', 'campaign_type', 'customer_name', 'mobile_no', 'city', 
                'data_source', 'login_status', 'ref_no', 'app_status', 'app_status_date'];

            fields.forEach(field => {
                if (frm.doc[field]) { 
                    frm.set_df_property(field, 'read_only', 1);
                } else {
                    frm.set_df_property(field, 'read_only', 0); 
                }
            });
        }
    },

    refresh: function(frm) {
        frm.add_custom_button(__('Edit Details'), function() {
            const fieldsToEdit = ['campaign_date', 'cr_date', 'lead_type', 'campaign_type', 'customer_name', 'mobile_no', 'city', 
                'data_source', 'login_status', 'ref_no', 'app_status', 'app_status_date'];

            fieldsToEdit.forEach(function(field) {
                frm.set_df_property(field, 'read_only', 0);
                frm.refresh_field(field);
            });
        });

        
        const visibleStatuses = ["IP Approved", "VKYC", "BKYC", "Risk", "Cure Pending", "Cure Done", "Approved", "SVKYC"];
        
        if (visibleStatuses.includes(frm.doc.login_status)) {
            frm.set_df_property('bank_details_section', 'hidden', 0);
        } else {
            frm.set_df_property('bank_details_section', 'hidden', 1);
        }
    },

    login_status: function(frm) {
        const visibleStatuses = ["IP Approved", "VKYC", "BKYC", "SVKYC", "Risk", "Cure Pending", "Cure Done", "Approved"];

        if (visibleStatuses.includes(frm.doc.login_status)) {
            frm.set_df_property('bank_details_section', 'hidden', 0);
            frm.set_df_property('ref_no', 'reqd', 1);
            frm.set_df_property('app_status', 'reqd', 1);
            frm.set_df_property('app_status_date', 'reqd', 1);
        } else {
            frm.set_df_property('bank_details_section', 'hidden', 1);

        }
    }
});