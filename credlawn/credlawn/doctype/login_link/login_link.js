frappe.ui.form.on('Login Link', {
    onload: function(frm) {
        if (!frm.is_new()) {
            const fields = [
                'campaign_date', 'customer_name', 'mobile_no', 'lc1_code', 
                'link_type', 'data_source', 'data_source'
            ];

            fields.forEach(field => {
                frm.set_df_property(field, 'read_only', !!frm.doc[field]);
            });
        }
    }
});
